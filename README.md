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