from __future__ import annotations

import math
from typing import Any

from forest_tending_sdk import ForestTendingHook, HookInput, HookOutput, TreeFields


def number(tree: Any, field: Any, default: float = 0.0) -> float:
    value = tree.number(field, float("nan"))
    return default if math.isnan(value) else value


def target_score(tree: Any) -> float:
    """Score with existing tree attributes; no duplicate fields or parameters."""
    dbh = number(tree, TreeFields.DBH)
    height = number(tree, TreeFields.TREE_HEIGHT)
    crown_ratio = number(tree, TreeFields.CROWN_HEIGHT_RATIO, 0.5)
    straightness = number(tree, TreeFields.STRAIGHTNESS, 0.7)
    return round((0.35 * dbh) + (0.25 * height) + (20.0 * crown_ratio) + (20.0 * straightness), 4)


class MyForestTendingHook(ForestTendingHook):
    # Keep both lists empty unless the script creates a new exposed field or
    # needs a genuinely user-tunable setting with no existing SDK/C++ equivalent.
    fields = []
    parameters = []

    def attribute(self, ctx: HookInput) -> HookOutput:
        return HookOutput.attribute_result("No dynamic attributes are generated.")

    def select_targets(self, ctx: HookInput) -> HookOutput:
        out = HookOutput.target_selection_result("C++ target candidates retained and ranked.")
        tree_by_id = {tree.tree_id: tree for tree in ctx.trees if tree.tree_id > 0}

        candidates = [
            tree_by_id[candidate.tree_id]
            for candidate in ctx.target_candidates
            if candidate.tree_id in tree_by_id
        ]
        candidates.sort(key=lambda tree: (target_score(tree), tree.tree_id), reverse=True)

        for priority, tree in enumerate(candidates):
            out.add_target(
                tree.tree_id,
                mandatory=False,
                priority=priority,
                score=target_score(tree),
                reason="Ranked from C++ target candidates using built-in tree fields.",
                tags=["target_candidate"],
            )
        return out

    def select_harvest(self, ctx: HookInput) -> HookOutput:
        out = HookOutput.harvest_selection_result("C++ harvest candidates ranked.")
        tree_by_id = {tree.tree_id: tree for tree in ctx.trees if tree.tree_id > 0}
        target_ids = set(ctx.target_tree_ids)

        candidates = [
            tree_by_id[candidate.tree_id]
            for candidate in ctx.harvest_candidates
            if candidate.tree_id in tree_by_id and candidate.tree_id not in target_ids
        ]
        candidates.sort(key=lambda tree: (target_score(tree), tree.tree_id))

        for priority, tree in enumerate(candidates):
            out.add_harvest_candidate(
                tree.tree_id,
                priority=priority,
                score=-target_score(tree),
                reason="Lower-quality C++ harvest candidate ranked earlier by Python.",
                tags=["harvest_candidate"],
            )

        # Do not duplicate harvest intensity, basal-area, crown-closure, or
        # canopy-gap controls here. C++ applies those built-in controls.
        return out

    def validate(self, ctx: HookInput) -> HookOutput:
        return HookOutput.validation_result("Final plan checked after built-in C++ controls.")


if __name__ == "__main__":
    raise SystemExit(MyForestTendingHook().main())
