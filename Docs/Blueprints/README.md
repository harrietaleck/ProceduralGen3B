# Blueprint logic (commented source)

Blueprint graphs are stored in binary `.uasset` files, so they cannot carry line
comments themselves. Each file in this folder is the readable, commented script
of one Blueprint, written in the S-expression graph format the graphs were built
from. Lines starting with `;` are comments.

| File | Blueprint |
|---|---|
| `BP_ProceduralJungleGenerator.bp.txt` | Grid-based jungle generator, seed, rules, route check, difficulty |
| `BP_Collectible.bp.txt` | Relic fragment pickup |
| `BP_GameManager.bp.txt` | Objective counter, HUD owner, run end |
| `BP_GameHUD.bp.txt` | Fragment counter, objective line, tier, end screen |
| `BP_Player.bp.txt` | First-person walking and looking, no combat |
| `BP_ReturnZone.bp.txt` | Trigger volume around the ship |

## Design in one paragraph

Procedural generation is controlled randomness within designed constraints.
The grid is the constraint (one object per cell), randomness gives variation
(seeded jitter, rotation, scale, mesh choice), and the gameplay rules give it
purpose (a planned route, safe zones, exactly N fragments). The ship and return
zone are placed by hand and never generated: the destination stays the same,
the journey changes.
