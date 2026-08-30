"""Copy procedural jungle gameplay elements onto Untitled without changing lighting."""
import os
import sys

import unreal

sys.path.insert(0, os.path.dirname(__file__))

TARGET_MAP = "/Game/Untitled"
SOURCE_MAP = "/Game/BottledTide/Maps/ProceduralGeneration"
GENERATOR_CLASS_PATH = "/Game/BottledTide/Blueprints/BP_ProceduralJungleGenerator"
GROUND_MESH_PATH = "/Engine/BasicShapes/Plane.Plane"
GROUND_MATERIAL_PATH = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
FLOOR_SCALE = unreal.Vector(80.0, 80.0, 1.0)
GENERATOR_LOCATION = unreal.Vector(0.0, 0.0, 50.0)
PLAYER_START_LOCATION = unreal.Vector(0.0, -1200.0, 200.0)


def find_actor_by_label(actor_subsystem, label):
    for actor in actor_subsystem.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def remove_existing_jungle_actors(actor_subsystem):
    for actor in list(actor_subsystem.get_all_level_actors()):
        label = actor.get_actor_label()
        class_name = actor.get_class().get_name()
        if label == "JungleGround":
            actor_subsystem.destroy_actor(actor)
        elif class_name.startswith("BP_ProceduralJungleGenerator"):
            actor_subsystem.destroy_actor(actor)


def ensure_ground(actor_subsystem):
    mesh = unreal.EditorAssetLibrary.load_asset(GROUND_MESH_PATH)
    if not mesh:
        raise RuntimeError(f"Could not load ground mesh: {GROUND_MESH_PATH}")

    actor = actor_subsystem.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(0.0, 0.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label("JungleGround")
    actor.set_actor_scale3d(FLOOR_SCALE)
    static_mesh_component = actor.static_mesh_component
    static_mesh_component.set_static_mesh(mesh)
    static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
    material = unreal.EditorAssetLibrary.load_asset(GROUND_MATERIAL_PATH)
    if material:
        static_mesh_component.set_material(0, material)
    return actor


def ensure_generator(actor_subsystem):
    generator_class = unreal.EditorAssetLibrary.load_blueprint_class(GENERATOR_CLASS_PATH)
    if not generator_class:
        raise RuntimeError(f"Could not load generator class: {GENERATOR_CLASS_PATH}")

    actor = actor_subsystem.spawn_actor_from_class(
        generator_class,
        GENERATOR_LOCATION,
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label("ProceduralJungleGenerator")
    return actor


def ensure_player_start(actor_subsystem):
    for actor in actor_subsystem.get_all_level_actors():
        if isinstance(actor, unreal.PlayerStart):
            actor.set_actor_location(PLAYER_START_LOCATION, False, True)
            return actor

    return actor_subsystem.spawn_actor_from_class(
        unreal.PlayerStart,
        PLAYER_START_LOCATION,
        unreal.Rotator(0.0, 0.0, 0.0),
    )


def save_map(map_path):
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if level_subsystem.save_current_level():
        unreal.log(f"Saved map: {map_path}")
        return True

    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    saved = unreal.EditorLoadingAndSavingUtils.save_map(world, map_path)
    if saved:
        unreal.log(f"Saved map via fallback helper: {map_path}")
        return True
    raise RuntimeError(f"Failed to save map: {map_path}")


def main():
    if not unreal.EditorAssetLibrary.does_asset_exist(TARGET_MAP):
        raise RuntimeError(f"Target map not found: {TARGET_MAP}")

    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level_subsystem.load_level(TARGET_MAP)
    unreal.log(f"Loaded target map: {TARGET_MAP}")

    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    remove_existing_jungle_actors(actor_subsystem)
    ensure_ground(actor_subsystem)
    ensure_generator(actor_subsystem)
    ensure_player_start(actor_subsystem)
    save_map(TARGET_MAP)

    unreal.log(
        f"Added jungle gameplay elements to {TARGET_MAP}. "
        f"Lighting was not modified. Source layout: {SOURCE_MAP}"
    )


if __name__ == "__main__":
    main()
