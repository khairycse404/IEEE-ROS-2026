from copy import deepcopy
import random

from grid import Grid
from fleet import Fleet
from simulation import Simulation
from AStar_MazeSolver import Pathfinding

FLEET_FILE = "fleet.json"

def load_fleet():
    fleet = Fleet()
    fleet.load_from_json(FLEET_FILE)
    return fleet

def display_drones(fleet):
    print("\n--- DRONES ---")
    for i, drone in enumerate(fleet.drones):
        print(f"{i + 1}) Drone {drone.id} | Battery: {drone.battery:.2f}% | Position: {drone.position} | Capacity: {drone.capacity}")

def display_packages(fleet):
    print("\n--- PACKAGES ---")
    for i, package in enumerate(fleet.packages):
        print(f"{i + 1}) Package {package.package_id} | Weight: {package.weight}kg | Destination: {package.destination}")

def best_performance(fleet):
    best = fleet.best_performance()
    if best is None:
        print("\nNo drones available.")
        return
    print("\n--- BEST PERFORMANCE ---")
    print(f"Drone {best.id} | Battery: {best.battery:.2f}% | Position: {best.position}")

def generate_maze_map(grid, start, destination):
    """
    NEW: Generates a more structured, maze-like environment
    instead of random disconnected blocks.
    """
    pf = Pathfinding()

    while True:
        grid.no_fly_zones.clear()
        zones = []

        # Create structured maze walls
        for row in range(grid.height):
            for col in range(grid.width):
                position = (row, col)
                if position == start or position == destination:
                    continue
                
                # Create grid lines with gaps
                if row % 2 == 0 or col % 2 == 0:
                    # 65% chance to place a wall, creating paths and dead ends
                    if random.random() < 0.65:
                        zones.append(position)

        grid.add_no_fly_cluster(zones)

        # Ensure start and dest are clear
        grid.remove_no_fly_zone(start)
        grid.remove_no_fly_zone(destination)

        path = pf.a_star(start, destination, grid)
        if path is not None:
            break

def main():
    fleet = load_fleet()
    selected_drone = None
    selected_package = None

    while True:
        print("\n========== AEROPATH ==========")
        print("1) Select Drone")
        print("2) Select Package")
        print("3) Start Single Simulation")
        print("4) Best Performance Check")
        print("5) Charge All Drones")
        print("6) Simulate All Drones (Sequential Maze)")
        print("7) Exit")

        choice = input("\nChoose option: ")

        if choice == "1":
            display_drones(fleet)
            try:
                index = int(input("\nSelect drone number: ")) - 1
                selected_drone = deepcopy(fleet.drones[index])
                # Save index to update original later
                selected_drone._original_index = index 
                print(f"\nSelected Drone {selected_drone.id}")
            except:
                print("\nInvalid selection.")

        elif choice == "2":
            display_packages(fleet)
            try:
                index = int(input("\nSelect package number: ")) - 1
                selected_package = deepcopy(fleet.packages[index])
                selected_package.delivered = False
                
                selected_package.assign_to = lambda drone_id: setattr(selected_package, "assigned_drone", drone_id)
                selected_package.mark_delivered = lambda: setattr(selected_package, "delivered", True)
                selected_package.is_delivered = False
                
                print(f"\nSelected Package {selected_package.package_id}")
            except:
                print("\nInvalid selection.")

        elif choice == "3":
            if selected_drone is None or selected_package is None:
                print("\nPlease select both a drone and a package first.")
                continue

            grid = Grid(20, 20)
            generate_maze_map(grid, start=selected_drone.position, destination=selected_package.destination)

            sim_fleet = Fleet()
            sim_fleet.add_drone(selected_drone)
            sim_fleet.add_package(selected_package)

            sim = Simulation(fleet=sim_fleet, grid=grid, time_step=0.2)
            sim.run()

            # --- NEW: Persist battery usage back to the main fleet ---
            orig_idx = selected_drone._original_index
            fleet.drones[orig_idx].battery = sim_fleet.drones[0].battery
            fleet.drones[orig_idx].position = sim_fleet.drones[0].position
            fleet.save_to_json(FLEET_FILE)
            print("\nFleet updated and saved.")

        elif choice == "4":
            best_performance(fleet)

        elif choice == "5":
            # --- NEW: Charge all drones ---
            for drone in fleet.drones:
                drone.battery = 100.0
            fleet.save_to_json(FLEET_FILE)
            print("\n[SUCCESS] All drones have been charged to 100%.")

        elif choice == "6":
            # --- NEW: Simulate All Drones Sequentially ---
            print("\nStarting Sequential Simulation for All Drones...")
            
            for i, drone in enumerate(fleet.drones):
                if drone.battery < 10.0:
                    print(f"\nSkipping Drone {drone.id} (Low Battery).")
                    continue
                
                # Pick a package (modulo ensures we wrap around if fewer packages than drones)
                pkg_index = i % len(fleet.packages)
                current_pkg = deepcopy(fleet.packages[pkg_index])
                current_pkg.delivered = False
                current_pkg.mark_delivered = lambda p=current_pkg: setattr(p, "is_delivered", True)
                
                grid = Grid(20, 20)
                generate_maze_map(grid, start=drone.position, destination=current_pkg.destination)

                sim_fleet = Fleet()
                sim_drone = deepcopy(drone)
                sim_fleet.add_drone(sim_drone)
                sim_fleet.add_package(current_pkg)

                print(f"\n--- Running Simulation for Drone {drone.id} ---")
                # Run with auto_close=True and faster time_step
                sim = Simulation(fleet=sim_fleet, grid=grid, time_step=0.05)
                sim.run(auto_close=True) 

                # Persist state
                drone.battery = sim_fleet.drones[0].battery
                drone.position = sim_fleet.drones[0].position
            
            fleet.save_to_json(FLEET_FILE)
            print("\n[FINISHED] All sequential simulations completed and data saved.")

        elif choice == "7":
            print("\nExiting AeroPath...")
            break
        else:
            print("\nInvalid option.")

if __name__ == "__main__":
    main()