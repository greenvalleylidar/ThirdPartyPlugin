"""Read-only smoke test of the installed official gateway; no plugin edits."""
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parent / 'official-gateway-test'
ROOT.mkdir(exist_ok=True)
INSTALL = Path('D:/GreenValley Suite/LiDAR360/10.0.0.2/Agent/gvagent')
URL = 'http://127.8.9.10:30000/mcp'
env = os.environ.copy()
env['MCP_URL'] = URL
exe = str(Path(__file__).resolve().parents[1] / 'package' / 'skills' / 'lidar360' / 'scripts' / 'mcp-tool.exe')
schema_run = subprocess.run([exe, 'get_tool_schema', 'platform-get_project_context'], env=env, capture_output=True, timeout=10)
schema = None
if schema_run.returncode == 0:
    for encoding in ['utf-8', 'gb18030']:
        try:
            schema = json.loads(schema_run.stdout.decode(encoding))
            break
        except (UnicodeError, ValueError):
            pass
report = {'schema_exit_code': schema_run.returncode, 'schema': schema, 'responses': []}
args = [str(INSTALL / 'bundled/gvagent-runtime.exe'), 'mcp-gateway', '--software', 'lidar360', '--mcp-name', 'lidar360', '--mcp-url', URL, '--mcp-binding-mode', 'disabled', '--data-dir', str(ROOT / 'data')]
env['PI_CONFIG_DIR'] = str(INSTALL / 'bundled/config')
messages = queue.Queue()
stderr_path = ROOT / 'stderr.log'
with stderr_path.open('wb') as err:
    process = subprocess.Popen(args, cwd=INSTALL, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
    def reader():
        for line in process.stdout:
            messages.put(line)
        messages.put(None)
    threading.Thread(target=reader, daemon=True).start()
    def send(message):
        process.stdin.write((json.dumps(message) + '\n').encode())
        process.stdin.flush()
    def request(identifier, method, params):
        send({'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params})
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            line = messages.get(timeout=max(.1, deadline - time.monotonic()))
            if line is None:
                raise RuntimeError('Gateway stdout closed; exit=' + str(process.poll()))
            try:
                result = json.loads(line)
            except ValueError:
                continue
            if result.get('id') == identifier:
                report['responses'].append({'method': method, 'params': params, 'response': result})
                print(json.dumps(result, ensure_ascii=True), flush=True)
                return result
        raise TimeoutError(method)
    try:
        request(1, 'initialize', {'protocolVersion': '2025-03-26', 'capabilities': {}, 'clientInfo': {'name': 'gateway-readonly-smoke-test', 'version': '1.0'}})
        send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        request(2, 'tools/list', {})
        request(3, 'tools/call', {'name': 'mcp_gateway_status', 'arguments': {}})
        request(4, 'tools/call', {'name': 'mcp_gateway_list_targets', 'arguments': {}})
        if schema and schema.get('name') == 'platform-get_project_context' and not schema['inputSchema'].get('required'):
            request(5, 'tools/call', {'name': 'mcp_proxy', 'arguments': {'server_name': 'lidar360', 'tool_name': 'platform-get_project_context', 'params': {}}})
        else:
            report['query_skipped'] = 'Runtime schema was not obtained or has required parameters.'
    except Exception as exc:
        report['error'] = repr(exc)
        print('TEST_ERROR', repr(exc), flush=True)
    finally:
        process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=5)
        report['gateway_exit_code'] = process.returncode
(ROOT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('REPORT', ROOT / 'report.json', flush=True)
