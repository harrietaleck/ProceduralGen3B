"""Compile and save BottledTide blueprint assets."""
import unreal

ASSETS = [
    "/Game/BottledTide/Blueprints/BP_ProceduralJungleGenerator",
    "/Game/BottledTide/Blueprints/BP_KeyGoldCollectible",
    "/Game/BottledTide/Blueprints/BP_PuzzlePieceCollectible",
    "/Game/BottledTide/Blueprints/BP_TreasureChest",
]


def main():
    for asset_path in ASSETS:
        unreal.log(f"Compiling {asset_path}")
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        if not asset:
            raise RuntimeError(f"Missing blueprint: {asset_path}")
        unreal.BlueprintEditorLibrary.compile_blueprint(asset)
        status = asset.get_editor_property("status")
        status_name = str(status).split(".")[-1]
        if status_name in {"BS_ERROR", "BS_UNKNOWN"}:
            raise RuntimeError(f"Compile failed for {asset_path}: {status_name}")
        saved = unreal.EditorAssetLibrary.save_asset(asset_path, only_if_is_dirty=False)
        if not saved:
            raise RuntimeError(
                f"Could not save {asset_path}. Close Unreal Editor and run again."
            )
        unreal.log(f"OK {asset_path} ({status_name})")
    unreal.log("Blueprint compile/save pass complete.")


if __name__ == "__main__":
    main()
