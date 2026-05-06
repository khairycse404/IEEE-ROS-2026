import time
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from AStar_MazeSolver import Pathfinding

LOW_BATTERY_THRESHOLD = 10.0

class Simulation:

    def __init__(self, fleet, grid, time_step=0.3):
        self.fleet = fleet
        self.grid = grid
        self.time_step = time_step
        self.running = False

    def calculate_battery_usage(self, distance, payload_weight):
        gravity = 9.81
        base_cost = distance * 0.5
        payload_cost = payload_weight * gravity * 0.02
        return base_cost + payload_cost

    def move_drone_along_path(self, drone, package, path, ax):
        for step in path[1:]:
            
            if drone.battery < LOW_BATTERY_THRESHOLD:
                print(f"\n[URGENT] Drone {drone.id} battery below 10% ({drone.battery:.1f}%)! Returning to base.")
                drone.return_to_base()
                self.render(ax)
                plt.pause(self.time_step)
                return  

            old_position = drone.position
            drone.move(step)

            dx = step[0] - old_position[0]
            dy = step[1] - old_position[1]

            distance = math.sqrt(dx**2 + dy**2)

            usage = self.calculate_battery_usage(distance, package.weight)
            drone.consume_battery(usage)

            print(f"Drone {drone.id} -> {step} | Battery: {drone.battery:.1f}%")
            
            self.render(ax)
            plt.pause(self.time_step)

        package.mark_delivered()
        print(f"\nPackage {package.package_id} delivered.")

    def start_simulation(self, auto_close=False):
        self.running = True
        pf = Pathfinding()

        plt.ion()
        fig, ax = plt.subplots(figsize=(9, 9))
        
        self.render(ax)
        plt.pause(1)

        for package in self.fleet.packages:
            assigned_drone = self.fleet.drones[0]

            path = pf.a_star(assigned_drone.position, package.destination, self.grid)

            if path is None:
                print("\nNo path found.")
                continue

            self.move_drone_along_path(assigned_drone, package, path, ax)

        if auto_close:
            plt.pause(1.5)
            plt.close(fig)
        else:
            plt.ioff()
            plt.show()

    def render(self, ax):
        ax.clear()

        ax.set_xlim(-0.5, self.grid.width + 0.5)
        ax.set_ylim(-0.5, self.grid.height + 0.5)
        ax.set_xticks(range(self.grid.width + 1))
        ax.set_yticks(range(self.grid.height + 1))
        ax.grid(True)
        ax.set_title("AeroPath Simulation")
        ax.set_aspect("equal")

        for (row, col) in self.grid.no_fly_zones:
            square = patches.Rectangle((col, row), 1, 1, facecolor="black", edgecolor="black", linewidth=1)
            ax.add_patch(square)

        for package in self.fleet.packages:
            if not getattr(package, "is_delivered", False):
                dx = package.destination[1]
                dy = package.destination[0]
                target = patches.Rectangle((dx, dy), 1, 1, facecolor="green", edgecolor="green", linewidth=2)
                ax.add_patch(target)

        for drone in self.fleet.drones:
            x = drone.position[1] + 0.5
            y = drone.position[0] + 0.5

            base = patches.Circle((0.5, 0.5), 0.3, facecolor="gray", alpha=0.5)
            ax.add_patch(base)

            ax.plot(x, y, "bo", markersize=10)
            ax.text(x + 0.3, y, f"D{drone.id}", fontsize=10, fontweight="bold")
            ax.text(x + 0.3, y + 0.3, f"{drone.battery:.0f}%", fontsize=8)

        ax.invert_yaxis()
        plt.draw()
        plt.pause(0.01)

    def run(self, auto_close=False):
        self.start_simulation(auto_close)
