# Auto Driving Car Simulation

This program simulates one or more autonomous cars moving on a rectangular field.
Cars can be added with an initial position, direction, and a command string consisting of:

    - L: turn left (90 degrees)

    - R: turn right (90 degrees)

    - F: move forward one grid cell

If a car tries to move outside the field, the command is ignored.
When multiple cars are simulated concurrently (processing one command per car in each "step"),
if two (or more) cars end up in the same cell in a given step, they are considered to have collided.
Once a car collides it stops processing further commands.

Author: Louis

Date: 2025-02-08

Usage:
To run the simulation interactively:

    $ python car_simulation.py

To run the tests:

    $ python car_simulation.py --test


## Assumptions
1. Input Formats:

The field dimensions, car initial positions, and commands are entered in a strict space-separated format (e.g., "10 10" for the field, "1 2 N" for a car's position, and a command string like "FFRFFFFRRL").
The car's initial direction is expected to be one of N, S, E, or W (case-insensitive).
The command string for each car is expected to contain only the letters L, R, and F (again, case-insensitive).


2. Command Execution:

When a car receives a forward (F) command, it will only move if the resulting position is within the bounds of the field. Otherwise, the command is silently ignored.
Rotational commands (L and R) are always executed successfully.
Each car processes its commands one step at a time in the order the cars were added. That is, at each simulation step, every car (that has commands remaining and has not collided) processes one command.


3. Collision Handling:

If two or more cars end up on the same grid cell during the same simulation step, they are considered to have collided.
Once a car has collided, it stops processing any further commands.
The simulation marks both (or all) involved cars as collided and records the collision step, collision position, and the names of collision partners.


## Areas for Improvement / Gaps Identified
1. Enhanced Collision Detection:

Chain Collisions: The current logic stops processing commands for cars once they have collided. In a more advanced simulation, we might want to handle "chain collisions" where an active car could collide with a car that had collided in a previous step (or where multiple collisions occur in one simulation step in more complex patterns).

Multiple Car Collision Reporting: If more than two cars collide at the same position, we might want to provide a clearer, aggregated collision report.


2. Input Validation and User Experience:

Robust Parsing: While basic validation is present, additional error checking and input sanitization could improve robustness (for example, handling extra whitespace or unexpected input formats).

User Feedback: More detailed user messages or instructions might be added to help guide users if they enter incorrect input.


3. Code Structure and Modularity:

Separation of Concerns: While the current implementation separates the CLI, simulation logic, and tests within a single file for simplicity, a production-grade application would ideally separate these concerns into distinct modules or packages.

Logging: Implementing a logging framework instead of using print statements would be beneficial for debugging and production monitoring.


4. Testing and Extensibility:

Broader Test Coverage: Additional unit tests covering more edge cases, such as invalid inputs or boundary conditions (e.g., cars starting at the edge of the field), could be added.