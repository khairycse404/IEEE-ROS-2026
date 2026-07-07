# Task 14: Autonomous Maze Solver

This project demonstrates an autonomous TurtleBot3 navigating a custom Gazebo world using ROS 2 Jazzy and Gazebo Harmonic.

## 1. Simulation Setup
- **World:** A custom maze designed in SDF format.
- **Robot:** TurtleBot3 (Waffle model).
- **Control:** Open-loop control via a custom Python node (`autonomous_mover.py`) publishing to `/cmd_vel`.

## 2. Launching the Simulation
To run the full simulation, use the following command in your terminal:

```bash
ros2 launch gazebo_autonomous_pkg gazebo_autonomous.launch.py