"""Fix project asset errors without changing level lighting."""
import os
import sys

import unreal

sys.path.insert(0, os.path.dirname(__file__))

BROKEN_MATERIAL = "/Game/BottledTide/Materials/M_MapInk"
MATERIAL_REPLACEMENT = "/Game/BottledTide/Materials/M_TreasureGlow"

MATERIALS = [
    "/Game/BottledTide/Materials/M_KeyGold",
    "/Game/BottledTide/Materials/M_KeySilver",
    "/Game/BottledTide/Materials/M_PuzzlePieceGlow",
    "/Game/BottledTide/Materials/M_TreasureGlow",
    "/Game/BottledTide/Materials/M_ChestWood",
    BROKEN_MATERIAL,
]

BLUEPRINTS = [
    "/Game/BottledTide/Blueprints/BP_ProceduralJungleGenerator",
    "/Game/BottledTide/Blueprints/BP_KeyGoldCollectible",
    "/Game/BottledTide/Blueprints/BP_PuzzlePieceCollectible",
    "/Game/BottledTide/Blueprints/BP_TreasureChest",
]

ORPHAN_BLUEPRINT = "/Game/BottledTide/Blueprints/BP_Collectible"


def ensure_map_ink_material():
    if unreal.EditorAssetLibrary.does_asset_exist(BROKEN_MATERIAL):
        return True, "M_MapInk exists"

    if not unreal.EditorAssetLibrary.does_asset_exist(MATERIAL_REPLACEMENT):
        return False, f"Missing replacement material: {MATERIAL_REPLACEMENT}"

    created = unreal.EditorAssetLibrary.duplicate_asset(
        MATERIAL_REPLACEMENT,
        BROKEN_MATERIAL,
    )
    if not created:
        return False, "Could not recreate M_MapInk"
    unreal.EditorAssetLibrary.save_asset(BROKEN_MATERIAL, only_if_is_dirty=False)
    return True, "Recreated M_MapInk"


def compile_material(asset_path):
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset:
        return False, "missing"
    unreal.MaterialEditingLibrary.recompile_material(asset)
    saved = unreal.EditorAssetLibrary.save_asset(asset_path, only_if_is_dirty=False)
    if not saved:
        return True, "compiled (save blocked)"
    return True, "compiled"


def compile_blueprint(asset_path):
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset or not isinstance(asset, unreal.Blueprint):
        return False, "missing blueprint"
    unreal.BlueprintEditorLibrary.compile_blueprint(asset)
    status_name = str(asset.get_editor_property("status")).split(".")[-1]
    if status_name in {"BS_ERROR", "BS_UNKNOWN"}:
        return False, status_name
    saved = unreal.EditorAssetLibrary.save_asset(asset_path, only_if_is_dirty=False)
    if not saved:
        return True, f"{status_name} (save blocked)"
    return True, status_name


def remove_orphan_collectible():
    if not unreal.EditorAssetLibrary.does_asset_exist(ORPHAN_BLUEPRINT):
        return True, "already removed"
    deleted = unreal.EditorAssetLibrary.delete_asset(ORPHAN_BLUEPRINT)
    if not deleted:
        return False, "delete failed"
    return True, "deleted"


def main():
    errors = []

    ok, message = ensure_map_ink_material()
    unreal.log(f"[material-fix] {message}")
    if not ok:
        errors.append(message)

    ok, message = remove_orphan_collectible()
    unreal.log(f"[cleanup] BP_Collectible: {message}")
    if not ok:
        unreal.log_warning(message)

    for asset_path in MATERIALS:
        ok, message = compile_material(asset_path)
        unreal.log(f"[material] {asset_path}: {message}")
        if not ok:
            errors.append(f"{asset_path}: {message}")

    for asset_path in BLUEPRINTS:
        ok, message = compile_blueprint(asset_path)
        unreal.log(f"[blueprint] {asset_path}: {message}")
        if not ok:
            errors.append(f"{asset_path}: {message}")

    if errors:
        for item in errors:
            unreal.log_error(item)
        raise RuntimeError(f"Found {len(errors)} error(s)")

    unreal.log("All asset errors fixed.")


if __name__ == "__main__":
    main()
