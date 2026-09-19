# ICE Task 3 - Perlin Noise

> "Can you create a procedurally generated world where the enemy leaves its spawn point and
> eventually finds its way back to where it started?"

**Answer: yes.** The world changes with the seed. The home position never does.

```
PERLIN NOISE -> TERRAIN HEIGHT -> SEEDED VARIATION -> PROCEDURAL PATH
             -> STEEP TERRAIN AVOIDANCE -> LOOP BACK TO START
```

This is a separate prototype. It shares nothing with the Bottled Tide game.

## Where it lives

| Item | Location |
|---|---|
| Blueprint | `Content/BottledTide/ICE3/BP_PerlinNoiseTerrain` |
| Materials | `Content/BottledTide/ICE3/M_ICE3_Terrain`, `M_ICE3_Path`, `M_ICE3_Home` |
| Level | the shared game level, actor `ICE3_PerlinNoiseTerrain`, placed far from the jungle and ship (floating at z = 6000, y = 9000) |
| Commented script | `Docs/Blueprints/BP_PerlinNoiseTerrain.bp.txt` |
| Screenshots | `Docs/ICE3/evidence/seed_1001.png`, `seed_2026.png`, `seed_7777.png` |

## How to use it

1. Select the actor `ICE3_PerlinNoiseTerrain` in the level.
2. In the Details panel change **Seed**. The terrain and route rebuild straight away (no need to
   press Play). Each rebuild takes about half a second.
3. Other settings in the same panel: **Map Size**, **Cell Size**, **Noise Scale**,
   **Height Multiplier**, **Max Slope Degrees**.
4. For a top-down screenshot, look straight down at the actor from about 3,000 cm above it,
   with +X pointing up the screen. The seed and result are printed above the map.

## How it works

| Step | What happens | Where |
|---|---|---|
| 1. Noise | Every grid point is sampled with Unreal's Perlin noise (Geometry Script "Compute Perlin Noise"), two layers: broad hills plus finer bumps at half strength. The **Seed** is the noise's random seed. | `GenerateHeights` |
| 2. Height | Noise (about -1..1) x **Height Multiplier** = height in cm. Colours show height: blue-green lowlands, green, brown hills, pale peaks. | `BuildTerrainMesh`, `HeightColor` |
| 3. Home | One cell on the map edge (column 0, middle row) is HOME. It is the same cell for every seed. A tall pink beacon and pad mark it. | `BuildLoop`, `PlaceHome` |
| 4. Waypoints | Three waypoints are aimed at fixed regions (north, far east, south), nudged by the seed, then snapped to the flattest nearby cell. | `PickWaypoint` |
| 5. Path | Each leg is found with Dijkstra's shortest-path algorithm. A step is **forbidden** if its slope exceeds **Max Slope Degrees**; steeper-but-allowed steps cost more, so routes prefer flat ground. | `FindLeg` |
| 6. Loop | Route: HOME -> north -> east -> south -> HOME. After the outward legs, the ground around them is blocked so the return legs must use different ground. | `BuildLoop`, `BlockAroundPath` |
| 7. Fallback | If a seed has no loop at the set slope, the limit is relaxed by 6 degrees at a time (at most 3 times) and reported. It was never needed for the three seeds below. | `Rebuild` |

## Seed testing (evidence)

Every number below was recomputed independently from the generated data, not read from the
Blueprint's own report. Settings: Map Size 32, Cell Size 100, Noise Scale 0.11, Height Multiplier
450, Max Slope 30 degrees.

| | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|
| **Seed** | 1001 | 2026 | 7777 |
| Screenshot | `evidence/seed_1001.png` | `evidence/seed_2026.png` | `evidence/seed_7777.png` |
| Height range | -289.5 to 377.7 cm | -329.9 to 270.3 cm | -316.7 to 287.7 cm |
| Height signature (a checksum of all 1024 heights) | 95304.4 | -65835.7 | -90447.5 |
| HOME cell (column, row) | 0, 16 | 0, 16 | 0, 16 |
| Route starts at HOME | yes | yes | yes |
| Route ends at HOME | yes | yes | yes |
| Route cells | 67 | 76 | 66 |
| Route length | 82.5 m | 92.2 m | 78.7 m |
| Steepest step used | 29.2 deg | 29.2 deg | 25.5 deg |
| Slope limit | 30 deg | 30 deg | 30 deg |
| Steps that are not neighbours | 0 | 0 | 0 |
| Return cells touching the outward trip | 4 of 33 | 5 of 37 | 6 of 34 |
| Loop result | OK | OK | OK |

Reading the table:

- **Terrain changes with the seed.** The height range and the checksum differ for every seed.
- **Home stays the same.** Column 0, row 16 in all three.
- **The route is a loop.** It leaves HOME, reaches column 26 to 28 (the far side), and returns
  to HOME. Only 4 to 6 return cells sit next to the outward trip, and those are near HOME and the
  far waypoint where the two trips must meet.
- **No impossible terrain.** The steepest step used is 25.5 to 29.2 degrees, always under 30.

## Assessment criteria

| Criterion | Evidence |
|---|---|
| Terrain changes with the seed | Three different height ranges and checksums; three different screenshots |
| Terrain looks naturally varied | Hills, valleys and ridges in the screenshots; two noise layers |
| Path loops back to the starting area | Starts and ends on the HOME cell in all three runs |
| Path avoids impossible terrain | Steepest step 25.5 to 29.2 degrees against a 30 degree limit; steeper steps are refused outright |
| Usable in a tower-defence game | See below |

## Tower-defence relevance

- **Enemy route.** The path is an ordered list of grid cells (`PathCells`). An enemy could walk
  it cell by cell, and it ends back at the spawn.
- **Different maps per seed.** Terrain and route both change with the seed.
- **Terrain affects the route.** The search refuses steep steps and prefers flat ground, so hills
  bend the route.
- **Tower placement later.** The height array (`Heights`) and the route cells are both available.
  Cells beside the route on flat ground would be natural tower sites.

## Limitations

- The Perlin noise comes from Geometry Script's "Compute Perlin Noise" node, because Blueprints
  have no 2D Perlin node. It is Unreal's own Perlin implementation, but not the C++ function
  `FMath::PerlinNoise2D` by name.
- Each rebuild takes about half a second, which is noticeable when typing a new seed.
- The route is one cell wide and follows grid cells, so it has small stair-steps.
- Enemy movement, tower placement and a game loop are not implemented: only the terrain and path.
- The three screenshots are from the editor viewport, not from a packaged game.
