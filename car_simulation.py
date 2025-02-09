#!/usr/bin/env python3
import sys

# ---------------------------------------------------------------------------
# Domain classes
# ---------------------------------------------------------------------------

class Field:
    """
    Represents the simulation field.
    Coordinates start at (0,0) and valid positions are 0 <= x < width and 0 <= y < height.
    (For example, if the field dimensions are 10 x 10, valid positions are from (0,0) to (9,9).)
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height


class Car:
    """
    Represents a car in the simulation.
    Stores the current state and the original configuration.
    """
    left_turn = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
    right_turn = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
    move_delta = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

    def __init__(self, name: str, x: int, y: int, direction: str, commands: str):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.direction = direction.upper()
        self.commands = commands.upper()
        self.pointer = 0  # next command to process

        # Collision information (if a collision occurs)
        self.collided = False
        self.collision_step = None
        self.collision_position = None
        self.collision_partners = set()

        # Store initial configuration for reporting later
        self.initial_x = int(x)
        self.initial_y = int(y)
        self.initial_direction = direction.upper()
        self.initial_commands = commands.upper()

    def process_next_command(self, field: Field) -> None:
        """
        Process the next command from the car's command string.
        If the command is F and the move would be out-of-bounds, the move is ignored.
        Rotations (L and R) always succeed.
        """
        if self.collided or self.pointer >= len(self.commands):
            return  # nothing to do

        command = self.commands[self.pointer]
        self.pointer += 1

        if command == 'L':
            self.direction = Car.left_turn[self.direction]
        elif command == 'R':
            self.direction = Car.right_turn[self.direction]
        elif command == 'F':
            dx, dy = Car.move_delta[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            if field.in_bounds(new_x, new_y):
                self.x = new_x
                self.y = new_y
            # If the move would be out-of-bounds, ignore the command.
        # (Any unrecognized command is ignored, though input is validated beforehand.)

# ---------------------------------------------------------------------------
# Simulation class
# ---------------------------------------------------------------------------

class Simulation:
    """
    Represents the simulation that contains the field and the cars.
    The simulation is run step by step, processing one command for each car per step.
    """
    def __init__(self, field: Field):
        self.field = field
        self.cars = []  # list of Car objects

    def add_car(self, car: Car) -> None:
        self.cars.append(car)

    def run(self) -> None:
        """
        Run the simulation step by step.
        At each simulation step, each car (that has not collided and still has commands)
        processes one command (in the order the cars were added). After each move,
        the simulation checks if any two (or more) cars are in the same position.
        If a collision is detected, the involved cars are marked as collided and
        stop processing any further commands.
        """
        step = 1
        # Continue until no non-collided car has any remaining commands.
        while any(car for car in self.cars if not car.collided and car.pointer < len(car.commands)):
            # Process one command for each car (in the order they were added)
            for car in self.cars:
                if not car.collided and car.pointer < len(car.commands):
                    car.process_next_command(self.field)
                    # After the move, check collision with all other non-collided cars.
                    for other in self.cars:
                        if other is not car and not other.collided:
                            if (car.x, car.y) == (other.x, other.y):
                                # Mark both cars as collided.
                                car.collided = True
                                other.collided = True
                                car.collision_step = step
                                other.collision_step = step
                                car.collision_position = (car.x, car.y)
                                other.collision_position = (other.x, other.y)
                                car.collision_partners.add(other.name)
                                other.collision_partners.add(car.name)
                                # Once a collision is detected for a car, no further checking is needed.
                                break
            step += 1

# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------

def interactive_menu():
    """
    Runs the interactive command-line interface for the simulation.
    """
    while True:
        print("\nWelcome to Auto Driving Car Simulation!")
        field = None
        # Get field dimensions from user.
        while field is None:
            user_input = input("Please enter the width and height of the simulation field in x y format:\n").strip()
            try:
                parts = user_input.split()
                if len(parts) != 2:
                    raise ValueError("Invalid input. Please enter two integers separated by a space.")
                width, height = int(parts[0]), int(parts[1])
                if width <= 0 or height <= 0:
                    raise ValueError("Width and height must be positive integers.")
                field = Field(width, height)
            except Exception as e:
                print(f"Error: {e}")

        print(f"You have created a field of {field.width} x {field.height}.")

        simulation = Simulation(field)

        # Loop for adding cars or running simulation.
        while True:
            print("\nPlease choose from the following options:")
            print("[1] Add a car to field")
            print("[2] Run simulation")
            option = input().strip()
            if option == '1':
                # Add a car.
                name = input("Please enter the name of the car:\n").strip()
                if any(car.name == name for car in simulation.cars):
                    print("Error: Car name must be unique. Please try again.")
                    continue

                pos_input = input(f"Please enter initial position of car {name} in x y Direction format:\n").strip()
                try:
                    parts = pos_input.split()
                    if len(parts) != 3:
                        raise ValueError("Invalid format. Expected: x y Direction")
                    x, y = int(parts[0]), int(parts[1])
                    direction = parts[2].upper()
                    if direction not in ['N', 'S', 'E', 'W']:
                        raise ValueError("Direction must be one of N, S, E, W.")
                    if not field.in_bounds(x, y):
                        raise ValueError("Initial position is out of the field bounds.")
                except Exception as e:
                    print(f"Error: {e}")
                    continue

                commands = input(f"Please enter the commands for car {name}:\n").strip().upper()
                if not commands or not all(c in "LRF" for c in commands):
                    print("Error: Commands must only contain the letters L, R, and F.")
                    continue

                car = Car(name, x, y, direction, commands)
                simulation.add_car(car)

                print("\nYour current list of cars are:")
                for car in simulation.cars:
                    print(f"- {car.name}, ({car.initial_x},{car.initial_y}) {car.initial_direction}, {car.initial_commands}")
            elif option == '2':
                # Run simulation.
                print("\nYour current list of cars are:")
                for car in simulation.cars:
                    print(f"- {car.name}, ({car.initial_x},{car.initial_y}) {car.initial_direction}, {car.initial_commands}")
                simulation.run()
                print("\nAfter simulation, the result is:")
                for car in simulation.cars:
                    if car.collided:
                        # List collision partners (if more than one, join by comma).
                        partners = ", ".join(sorted(car.collision_partners))
                        pos = car.collision_position
                        print(f"- {car.name}, collides with {partners} at ({pos[0]},{pos[1]}) at step {car.collision_step}")
                    else:
                        print(f"- {car.name}, ({car.x},{car.y}) {car.direction}")

                # Post-simulation menu.
                print("\nPlease choose from the following options:")
                print("[1] Start over")
                print("[2] Exit")
                post_option = input().strip()
                if post_option == '1':
                    break  # Start over: break out to outer loop to reinitialize everything.
                elif post_option == '2':
                    print("Thank you for running the simulation. Goodbye!")
                    return
                else:
                    print("Invalid option. Exiting.")
                    return
            else:
                print("Invalid option. Please try again.")

# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

import unittest

class TestSimulation(unittest.TestCase):
    def test_single_car_no_collision(self):
        """Scenario 1: A single car runs its commands without collision."""
        field = Field(10, 10)
        sim = Simulation(field)
        # Car A starting at (1,2) facing North with commands "FFRFFFFRRL"
        carA = Car("A", 1, 2, "N", "FFRFFFFRRL")
        sim.add_car(carA)
        sim.run()
        # Expected final state: (5,4) facing South, no collision.
        self.assertFalse(carA.collided)
        self.assertEqual((carA.x, carA.y), (5, 4))
        self.assertEqual(carA.direction, "S")

    def test_two_cars_collision(self):
        """Scenario 2: Two cars collide.
        
        Car A: starts at (1,2) facing N with commands "FFRFFFFRRL"
        Car B: starts at (7,8) facing W with commands "FFLFFFFFFF"
        Expected collision at step 7 at (5,4).
        """
        field = Field(10, 10)
        sim = Simulation(field)
        carA = Car("A", 1, 2, "N", "FFRFFFFRRL")
        carB = Car("B", 7, 8, "W", "FFLFFFFFFF")
        sim.add_car(carA)
        sim.add_car(carB)
        sim.run()

        self.assertTrue(carA.collided)
        self.assertTrue(carB.collided)
        self.assertEqual(carA.collision_step, 7)
        self.assertEqual(carB.collision_step, 7)
        self.assertEqual(carA.collision_position, (5, 4))
        self.assertEqual(carB.collision_position, (5, 4))
        self.assertIn("B", carA.collision_partners)
        self.assertIn("A", carB.collision_partners)

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    interactive_menu()

if __name__ == '__main__':
    # If the user passes '--test' as an argument, run the unit tests.
    if '--test' in sys.argv:
        # Remove the '--test' argument before running unittest.main()
        sys.argv.remove('--test')
        unittest.main()
    else:
        main()
