<project>
You are helping me develop a student game project called "Bottled Tide".

The game is being developed in Unreal Engine.

IMPORTANT:
Do not redesign the game's core concept without discussing it first.
Do not replace working systems unnecessarily.
Build incrementally and keep the project stable after every change.

The project is based on the theme:

"END WHERE YOU STARTED"

The central design idea is:

The player leaves their ship, travels into a dangerous procedurally generated jungle/island environment to collect bottle-power relic fragments, and must eventually return to the ship.

The ending/homecoming remains constant.
The journey changes.

The procedural generation therefore exists primarily to make each run feel different and replayable rather than to randomly change the game's objective.
</project>


<game_concept>

GAME TITLE:
Bottled Tide

SETTING:
The player begins at their ship, "The Horizon's Debt", and travels inland into the Isle of Marrow Canopy.

The jungle should feel:
- dense
- wild
- slightly unpredictable
- mysterious
- dangerous
- different on repeated playthroughs

The player should not simply memorise one fixed corridor.

The game should communicate the theme through gameplay:

START:
Ship / The Horizon's Debt

        ↓

PROCEDURALLY GENERATED JOURNEY

        ↓

Jungle / Isle of Marrow Canopy

        ↓

Find relic / bottle-power fragments

        ↓

Navigate back through the changing environment

        ↓

END:
Return to The Horizon's Debt

The important design rule is:

THE DESTINATION STAYS THE SAME.
THE JOURNEY CHANGES.

Do not make the ending itself random.
Randomise the environment, encounters, routes, object placement and visual composition instead.
</game_concept>


<current_prototype>

The existing procedural prototype is called:

BP_ProceduralJungleGenerator

The current system:

1. Runs at BeginPlay.
2. Creates a 10×10 grid.
3. Uses grid-cell partitioning.
4. Places environmental objects within cells.
5. Uses jittered positioning.
6. Randomises mesh selection.
7. Randomises rotation.
8. Randomises scale.
9. Spawns trees.
10. Spawns a boulder variant.
11. Spawns BP_Collectible relic fragments.
12. Prevents overlaps structurally because each cell can contain at most one spawned object.
13. Produces a different layout on separate playthroughs.

The current prototype has already been tested through three separate Simulate-In-Editor runs, and each run produced a different layout.

DO NOT throw away this existing approach unless there is a clear technical reason.

Improve it rather than unnecessarily replacing it.
</current_prototype>


<technical_direction>

Use Unreal Engine Blueprints unless there is a strong reason to use C++.

The procedural system should remain understandable to a student developer.

Prioritise:
- reliability
- readability
- performance
- easy debugging
- controllable randomness
- reusable systems
- clear Blueprint organisation

Avoid unnecessarily complicated systems.

The procedural generation should happen at runtime or in a way that supports repeated generation.

The system should expose important variables in the Blueprint Details panel where practical.

Useful configurable variables should include:

Grid Size
Cell Size
Spawn Chance
Tree Spawn Chance
Boulder Spawn Chance
Collectible Spawn Chance
Minimum/Maximum Scale
Rotation Range
Position Jitter
Random Seed

The goal is controlled randomness rather than completely uncontrolled randomness.
</technical_direction>


<gameplay_requirements>

Turn the procedural prototype into an actual GAME rather than merely a procedural environment demonstration.

The player needs:

1. A clear starting point at the ship.
2. A reason to leave the ship.
3. A procedurally generated jungle to explore.
4. Collectible relic/bottle-power fragments.
5. Environmental obstacles.
6. A reason to navigate through the environment.
7. A clear return journey.
8. A win condition based on returning to the ship after completing the objective.

The gameplay loop should be:

START AT SHIP
→ ENTER JUNGLE
→ EXPLORE
→ FIND/COLLECT REQUIRED FRAGMENTS
→ SURVIVE/NAVIGATE
→ RETURN TO SHIP
→ COMPLETE RUN

The procedural generation should make the exploration portion different each time.

Do not make the game feel like a walking simulator.

The player should have meaningful interaction with the environment and a clear gameplay objective.
</gameplay_requirements>


<procedural_generation>

Improve the current procedural system while keeping its basic grid philosophy.

The generator should be able to:

- generate different tree arrangements
- generate different boulder arrangements
- generate different collectible positions
- randomise environmental scale
- randomise environmental rotation
- randomise position within each grid cell
- maintain minimum spacing
- prevent impossible navigation
- maintain a playable route
- avoid blocking important gameplay areas
- create visually varied density

IMPORTANT:

Randomness must not destroy playability.

Do NOT allow procedural generation to:
- block the player spawn
- block the ship
- completely surround collectibles with impossible geometry
- create an impassable wall
- place objects directly inside critical gameplay locations
- create impossible return routes

Use designated safe zones where necessary.

Consider dividing the environment into:

SAFE / START AREA
↓
TRANSITION AREA
↓
PROCEDURAL EXPLORATION AREA
↓
OBJECTIVE AREA
↓
RETURN ROUTE

The exact implementation can be discussed before making major structural changes.
</procedural_generation>


<collectibles>

BP_Collectible represents the relic fragment.

Improve the collectible system so that it feels like an actual gameplay mechanic.

Each collectible should:

- be clearly visible
- have a recognisable visual identity
- be interactable
- disappear/be collected when picked up
- update the player's collection count
- provide feedback when collected
- contribute toward the objective

Create a simple objective system such as:

Fragments Collected: 0 / REQUIRED

When the required number has been collected:

OBJECTIVE COMPLETE

RETURN TO THE SHIP

The UI should communicate this clearly.
</collectibles>


<return_to_ship>

The return journey is extremely important because of the theme.

Do NOT simply teleport the player back to the ship.

The player should physically navigate back.

The environment may be procedurally different from another run, but the ship remains the fixed destination.

When the player reaches the ship after completing the objective:

Trigger the end-of-run sequence.

This should communicate:

"You made it back."

The end condition should reinforce:

"End Where You Started."
</return_to_ship>


<difficulty>

The original concept includes difficulty tiers:

Corsair
Captain
Legend

If the existing project supports these tiers, integrate them into procedural difficulty.

For example:

CORSAIR:
- lower environmental density
- easier navigation
- fewer hazards
- fewer required fragments

CAPTAIN:
- increased density
- more hazards
- more exploration required

LEGEND:
- higher environmental density
- more challenging navigation
- greater risk
- more demanding objective

Do not implement arbitrary difficulty changes just for the sake of having three modes.

Each difficulty should affect actual gameplay.
</difficulty>


<player_experience>

The player should always understand:

WHERE AM I?

WHAT AM I LOOKING FOR?

HOW MANY HAVE I COLLECTED?

WHERE DO I NEED TO GO?

HAVE I COMPLETED MY OBJECTIVE?

HOW DO I GET BACK?

The UI should remain minimal and atmospheric rather than covering the screen with information.

Suggested HUD:

Fragments: 2 / 5

Objective:
Collect the remaining relic fragments.

After completion:

OBJECTIVE COMPLETE
Return to The Horizon's Debt.
</player_experience>


<visual_direction>

The jungle should feel like an island canopy environment.

Use the existing environmental assets where possible.

The visual composition should have:

- layered vegetation
- variation in tree scale
- varied rotation
- open spaces
- dense areas
- boulders
- collectible landmarks
- natural-looking irregularity

Avoid making the environment look like a perfectly uniform grid.

The grid is a technical constraint.
The player should perceive an organic jungle.

Use jitter and controlled randomness to hide the underlying grid structure.
</visual_direction>


<blueprint_architecture>

Keep the Blueprint architecture modular.

Suggested systems:

BP_ProceduralJungleGenerator
    ↓
Generates environment

BP_Collectible
    ↓
Handles relic interaction

BP_Player
    ↓
Movement and interaction

BP_GameManager
    ↓
Tracks game state/objective

BP_Ship / BP_ReturnZone
    ↓
Handles successful return

BP_GameHUD
    ↓
Displays objective and progress

Do not create unnecessary Blueprints.

Reuse existing project systems wherever possible.
</blueprint_architecture>


<important_blueprint_principles>

When editing or creating Blueprints:

- verify exact Unreal node names before proposing them
- do not invent nodes
- check pin types
- check execution flow
- explain where each node connects
- avoid unnecessary Tick events
- prefer event-driven logic
- use functions/macros where they improve readability
- comment complicated procedural logic
- expose useful variables as editable
- compile after major changes
- test in Play-In-Editor

If a node does not exist, stop and find the correct Unreal equivalent rather than guessing.

The existing prototype previously encountered problems involving incorrect node assumptions and Static Mesh references.

Therefore, verify node availability and pin types carefully.
</important_blueprint_principles>


<testing>

Testing is part of the development process.

After each major change:

1. Compile the relevant Blueprint.
2. Run Play-In-Editor.
3. Check for errors.
4. Test the player spawn.
5. Test procedural generation.
6. Test collectible spawning.
7. Test collecting fragments.
8. Test the objective counter.
9. Test the return-to-ship condition.
10. Test a second playthrough.
11. Confirm that the environment changes.
12. Confirm that the game remains playable.

Test at least three independent procedural runs.

Record:

RUN 1
- layout
- collectibles
- obstacles
- gameplay result

RUN 2
- layout
- collectibles
- obstacles
- gameplay result

RUN 3
- layout
- collectibles
- obstacles
- gameplay result

The purpose is to demonstrate that procedural generation creates genuine variation while maintaining a playable experience.
</testing>


<academic_requirements>

This is a student game-development project.

Keep the implementation defensible academically.

When suggesting technical decisions, explain:

WHAT was changed
WHY it was changed
HOW it works
HOW it supports the game concept
HOW it was tested
WHAT limitation remains

The project should demonstrate that procedural generation is not simply randomness.

The central technical learning should be:

"Procedural generation is controlled randomness within designed constraints."

The grid provides the constraint.
Randomisation provides variation.
Gameplay rules provide purpose.
The fixed ship provides thematic consistency.

This relationship should be visible in the final implementation.
</academic_requirements>


<claude_workflow>

Before changing anything:

1. Inspect the existing project structure.
2. Identify existing Blueprints.
3. Identify existing player systems.
4. Identify existing procedural-generation systems.
5. Identify existing collectible systems.
6. Identify existing maps/levels.
7. Identify existing UI.
8. Determine what already works.
9. Do not rebuild working systems unnecessarily.

Then provide me with:

A. CURRENT PROJECT AUDIT
B. WHAT ALREADY WORKS
C. WHAT IS MISSING
D. PROPOSED ARCHITECTURE
E. IMPLEMENTATION PLAN

Only after that should implementation begin.

Work in small, testable stages.

After every stage, tell me:

- what was changed
- which Blueprint/file was changed
- why
- how to test it
- what I should expect to see

Do not silently make large architectural changes.
</claude_workflow>


<source_of_truth>

The attached project document is the primary source of truth for the existing Bottled Tide prototype.

Respect the terminology used in that document:

Bottled Tide
The Horizon's Debt
Isle of Marrow Canopy
BP_ProceduralJungleGenerator
BP_Collectible
relic fragment
Corsair
Captain
Legend
End Where You Started

Do not invent contradictory lore.

If something is not specified, identify it as an open design decision instead of pretending it is already established.
</source_of_truth>


<final_goal>

The final result should no longer feel like:

"Here is a procedural jungle demonstration."

It should feel like:

"A small, complete, playable Bottled Tide game in which the player leaves their ship, explores a procedurally generated jungle, collects the required relic fragments, and physically returns to the same ship to complete the run."

The procedural system should support the GAMEPLAY rather than become the entire game.

The player should experience the theme through the mechanics:

THE JOURNEY CHANGES.
THE HOME IS CONSTANT.

Start by auditing the existing project before making changes.
</final_goal>
