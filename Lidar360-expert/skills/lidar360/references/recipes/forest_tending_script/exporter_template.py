from __future__ import annotations

from forest_tending_sdk import (
    ForestTendingOperationRecordExporter,
    RecordContext,
    SheetData,
    TreeFields,
)


class CustomOperationRecordExporter(ForestTendingOperationRecordExporter):
    def build_overview_sheet(
        self,
        ctx: RecordContext,
        sheet_config: dict,
        index: int,
    ) -> SheetData:
        sheet = SheetData(f"Overview{index}", [], [], [18, 18])
        sheet.rows.append(["Metric", "Value"])
        sheet.rows.append(["Harvest Count", self.resolve_value(ctx, None, "plan.harvestCount")])
        sheet.rows.append(["Harvest Percent", self.resolve_value(ctx, None, "plan.harvestPercent")])
        return sheet

    def build_tree_sheets(
        self,
        ctx: RecordContext,
        sheet_config: dict,
        start_index: int,
    ) -> list[SheetData]:
        sheet = SheetData(f"Trees{start_index}", [], [], [12, 20, 14, 14])
        sheet.rows.append(["Tree ID", "Position", "Decision", "DBH"])
        stand = ctx.stand
        trees = list(stand.all_trees) if stand is not None and not isinstance(stand, dict) else []
        for tree in trees:
            sheet.rows.append(
                [
                    tree.tree_id,
                    tree.xy,
                    getattr(tree.decision, "name", str(tree.decision)),
                    tree.number(TreeFields.DBH, 0.0),
                ]
            )
        return [sheet]


if __name__ == "__main__":
    raise SystemExit(CustomOperationRecordExporter().main())
