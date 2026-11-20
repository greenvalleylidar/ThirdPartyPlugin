# LiDAR360 plugin 1.2.0

LiDAR360 激光雷达点云处理助手，覆盖点云分类、地形建模、林业分析及完整作业流程指导。

## 环境与更新

- 使用 Windows；宿主必须允许执行本地 Windows 命令。
- 单独安装并启动 LiDAR360，开启其 MCP 服务。
- CLI 位于 `skills/lidar360/scripts/mcp-tool.exe`，按实际安装目录定位，不使用固定缓存版本路径。
- 使用宿主支持的本地插件更新流程加载 1.2.0，然后开启新会话。源码修改或下载 ZIP 不会自动更新已安装副本。
- 本包不自动注册旧 MCP 连接；LiDAR360 自身的 MCP 服务仍须开启。

## 调用流程

运行包内 `mcp-tool.exe detect_mcp`，取得服务地址；后续每条命令显式传入 `-url`。先查询目标工具的实时 schema，按其定义构造 JSON 参数，再用 `call_tool` 串行执行。详细语法见 `skills/lidar360/references/profiles/mcp_tool_usage.md`。

只读查询示例：先切换到实际安装的插件根目录。

```powershell
$cli = (Resolve-Path -LiteralPath './skills/lidar360/scripts/mcp-tool.exe').Path
$addressLines = @(& $cli detect_mcp)
$detectExit = $LASTEXITCODE
$serviceUrl = ($addressLines -join "`n").Trim()
if ($detectExit -ne 0 -or $serviceUrl -notmatch '^https?://\S+$') {
    throw '未探测到唯一有效服务地址，请检查 LiDAR360 MCP 服务。'
}
& $cli -url $serviceUrl get_tool_schema 'platform-list_loaded_layers'
$schemaExit = $LASTEXITCODE
if ($schemaExit -ne 0) { throw '查询实时 schema 失败。' }
```

含引号的 JSON 在不同 PowerShell 版本下可能需要不同传参方式，应先用只读调用验证。不要从文档示例猜测业务参数，运行时 schema 才是执行依据。

检查进程退出码、MCP 的 `isError` 和业务返回：优先读取 `structuredContent`，缺失时再解析 `content` 中的业务 JSON。非零业务 `code` 即失败，缺少成功证据不能报告成功；处理任务还须检查输出结果。

## 验证范围与已知问题

交付目录附有文件检查及 CLI 只读验证记录，以记录中的实际结果为准。宿主重新安装后的加载、真实对话、跨机器和多实例行为仍待验证，不以 CLI 成功代替宿主端到端验收。

