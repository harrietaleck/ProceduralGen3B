"""Create the playable jungle level and place the procedural generator."""
import unreal

MAP_PATH = "/Game/BottledTide/Maps/ProceduralGeneration"
LEGACY_MAP_PATH = "/Game/BottledTide/Maps/ProceduralJungle"
OPEN_WORLD_TEMPLATE = "/Engine/Maps/Templates/OpenWorld"
GENERATOR_CLASS_PATH = "/Game/BottledTide/Blueprints/BP_ProceduralJungleGenerator"
GROUND_MESH_PATH = "/Engine/BasicShapes/Plane.Plane"
GROUND_MATERIAL_PATH = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
FLOOR_SCALE = unreal.Vector(80.0, 80.0, 1.0)

LIGHTING_ACTOR_CLASSES = (
    unreal.DirectionalLight,
    unreal.SkyLight,
    unreal.SkyAtmosphere,
    unreal.VolumetricCloud,
    unreal.ExponentialHeightFog,
    unreal.PostProcessVolume,
)


def ensure_map():
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        level_subsystem.load_level(MAP_PATH)
        unreal.log(f"Loaded existing map: {MAP_PATH}")
        return

    if unreal.EditorAssetLibrary.does_asset_exist(LEGACY_MAP_PATH):
        level_subsystem.load_level(LEGACY_MAP_PATH)
        unreal.log(f"Loaded legacy map as base: {LEGACY_MAP_PATH}")
        return

    created = level_subsystem.new_level_from_template(MAP_PATH, OPEN_WORLD_TEMPLATE)
    if not created:
        unreal.log_warning(
            f"Could not create map from {OPEN_WORLD_TEMPLATE}; creating a blank level instead."
        )
        created = level_subsystem.new_level(MAP_PATH)
    if not created:
        raise RuntimeError(f"Failed to create map: {MAP_PATH}")
    unreal.log(f"Created map from template: {MAP_PATH}")


def find_actor_by_label(actor_subsystem, label):
    for actor in actor_subsystem.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def clear_lighting_actors(actor_subsystem):
    for actor in actor_subsystem.get_all_level_actors():
        if isinstance(actor, LIGHTING_ACTOR_CLASSES):
            actor_subsystem.destroy_actor(actor)


def configure_sun(sun):
    sun_component = sun.light_component
    sun_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sun_component.set_intensity(100000.0)
    sun_component.set_light_color(unreal.LinearColor(1.0, 0.98, 0.92, 1.0))
    sun_component.set_cast_shadows(True)
    sun_component.set_editor_property("atmosphere_sun_light", True)
    sun_component.set_editor_property("atmosphere_sun_light_index", 0)
    sun.set_actor_rotation(unreal.Rotator(-50.0, -45.0, 0.0), False)


def configure_sky_light(sky_light):
    sky_component = sky_light.light_component
    sky_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sky_component.set_intensity(3.0)
    sky_component.set_editor_property(
        "source_type", unreal.SkyLightSourceType.SLS_CAPTURED_SCENE
    )
    sky_component.recapture_sky()


def configure_post_process(post_process):
    post_process.set_editor_property("unbound", True)
    settings = post_process.get_editor_property("settings")
    settings.set_editor_property("override_auto_exposure_method", True)
    settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_BASIC)
    settings.set_editor_property("override_auto_exposure_bias", True)
    settings.set_editor_property("auto_exposure_bias", 2.0)
    settings.set_editor_property("override_auto_exposure_min_brightness", True)
    settings.set_editor_property("auto_exposure_min_brightness", 1.0)
    settings.set_editor_property("override_auto_exposure_max_brightness", True)
    settings.set_editor_property("auto_exposure_max_brightness", 8.0)
    post_process.set_editor_property("settings", settings)


def ensure_default_lighting():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    clear_lighting_actors(actor_subsystem)

    sun = actor_subsystem.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(0.0, 0.0, 500.0),
        unreal.Rotator(-50.0, -45.0, 0.0),
    )
    sun.set_actor_label("Sun")
    configure_sun(sun)

    sky_atmosphere = actor_subsystem.spawn_actor_from_class(
        unreal.SkyAtmosphere,
        unreal.Vector(0.0, 0.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    sky_atmosphere.set_actor_label("SkyAtmosphere")

    sky_light = actor_subsystem.spawn_actor_from_class(
        unreal.SkyLight,
        unreal.Vector(0.0, 0.0, 600.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    sky_light.set_actor_label("SkyLight")
    configure_sky_light(sky_light)

    clouds = actor_subsystem.spawn_actor_from_class(
        unreal.VolumetricCloud,
        unreal.Vector(0.0, 0.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    clouds.set_actor_label("VolumetricCloud")

    fog = actor_subsystem.spawn_actor_from_class(
        unreal.ExponentialHeightFog,
        unreal.Vector(0.0, 0.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    fog.set_actor_label("ExponentialHeightFog")

    post_process = actor_subsystem.spawn_actor_from_class(
        unreal.PostProcessVolume,
        unreal.Vector(0.0, 0.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    post_process.set_actor_label("PostProcess")
    configure_post_process(post_process)


def ensure_ground():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in actor_subsystem.get_all_level_actors():
        if actor.get_actor_label() == "JungleGround":
            static_mesh_component = actor.static_mesh_component
            material = unreal.EditorAssetLibrary.load_asset(GROUND_MATERIAL_PATH)
            if material:
                static_mesh_component.set_material(0, material)
            return actor

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


def ensure_generator():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in actor_subsystem.get_all_level_actors():
        if actor.get_class().get_name().startswith("BP_ProceduralJungleGenerator"):
            actor.set_actor_location(unreal.Vector(0.0, 0.0, 50.0), False, True)
            actor.set_actor_label("ProceduralJungleGenerator")
            return actor

    generator_class = unreal.EditorAssetLibrary.load_blueprint_class(GENERATOR_CLASS_PATH)
    if not generator_class:
        raise RuntimeError(f"Could not load generator class: {GENERATOR_CLASS_PATH}")

    actor = actor_subsystem.spawn_actor_from_class(
        generator_class,
        unreal.Vector(0.0, 0.0, 50.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label("ProceduralJungleGenerator")
    return actor


def ensure_player_start():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in actor_subsystem.get_all_level_actors():
        if isinstance(actor, unreal.PlayerStart):
            actor.set_actor_location(unreal.Vector(0.0, -1200.0, 200.0), False, True)
            return actor

    return actor_subsystem.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(0.0, -1200.0, 200.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )


def save_map():
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    saved = level_subsystem.save_current_level()
    if saved:
        unreal.log(f"Saved map: {MAP_PATH}")
        return

    unreal.log_warning(
        f"Could not save {MAP_PATH}. Trying EditorLoadingAndSavingUtils.save_map."
    )
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    saved = unreal.EditorLoadingAndSavingUtils.save_map(world, MAP_PATH)
    if saved:
        unreal.log(f"Saved map via fallback helper: {MAP_PATH}")
        return

    # If the legacy map is locked by an open editor, write to the new day-lit map path.
    if MAP_PATH != LEGACY_MAP_PATH:
        raise RuntimeError(f"Failed to save map: {MAP_PATH}")

    unreal.log_warning(
        f"{LEGACY_MAP_PATH} is locked. Saving bright lighting to {MAP_PATH} instead."
    )
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorAssetLibrary.delete_asset(MAP_PATH)
    editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor_subsystem.get_editor_world()
    saved = unreal.EditorLoadingAndSavingUtils.save_map(world, MAP_PATH)
    if not saved:
        raise RuntimeError(
            f"Failed to save map. Close all Unreal Editor windows and run again."
        )
    unreal.log(f"Saved bright map to: {MAP_PATH}")


def setup_map(map_path):
    global MAP_PATH
    MAP_PATH = map_path
    ensure_map()
    ensure_default_lighting()
    ensure_ground()
    ensure_generator()
    ensure_player_start()
    save_map()
    unreal.log(f"Jungle level setup complete for {MAP_PATH}.")


def main():
    setup_map(MAP_PATH)
    unreal.log("Jungle map updated with bright daylight lighting.")


if __name__ == "__main__":
    main()
