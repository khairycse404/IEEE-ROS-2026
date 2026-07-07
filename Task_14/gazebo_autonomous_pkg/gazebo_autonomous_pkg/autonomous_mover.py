#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class AutonomousMover(Node):

    def __init__(self):
        super().__init__("autonomous_mover")

        self.pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer = self.create_timer(0.02, self.update)

        # -----------------------------
        # Robot Speeds
        # -----------------------------
        self.linear_speed = 0.35      # m/s
        self.angular_speed = 0.8      # rad/s

        # -----------------------------
        # Navigation Path
        # (Motion Type, Value)
        # F = Forward in meters
        # L = Turn Left in degrees
        # R = Turn Right in degrees
        # -----------------------------
        self.path = [
            ("F", 3.5),   # Move forward to the first corner
            ("L", 90),    # Turn left to face upwards
            ("F", 2.0),   # Move up the first vertical corridor
            ("R", 80),    # Turn right to face the long top corridor
            ("F", 6.0),   # Move across the top corridor
            ("R", 90),    # Turn right to face downwards
            ("F", 4.0),   # Move down the rightmost corridor
            ("R", 90),    # Turn right to face inwards to the goal
            ("F", 2.5),   # Move forward to the final spot
            ("R", 360)
        ]

        self.step = 0
        
        # Delay to ensure Gazebo is fully loaded before sending commands
        self.get_logger().info("Waiting for Gazebo to load... (7 seconds delay)")
        time.sleep(7.0) 
        
        self.start_time = time.time()
        self.get_logger().info("Autonomous Maze Solver Started")

    def update(self):

        if self.step >= len(self.path):
            self.pub.publish(Twist())
            return

        motion, value = self.path[self.step]
        elapsed = time.time() - self.start_time
        cmd = Twist()

        # =====================
        # Forward Motion
        # =====================
        if motion == "F":
            required_time = value / self.linear_speed
            if elapsed < required_time:
                cmd.linear.x = self.linear_speed
            else:
                self.next_step()

        # =====================
        # Turn Left
        # =====================
        elif motion == "L":
            required_angle = math.radians(value)
            required_time = required_angle / self.angular_speed
            if elapsed < required_time:
                cmd.angular.z = self.angular_speed
            else:
                self.next_step()

        # =====================
        # Turn Right
        # =====================
        elif motion == "R":
            required_angle = math.radians(value)
            required_time = required_angle / self.angular_speed
            if elapsed < required_time:
                cmd.angular.z = -self.angular_speed
            else:
                self.next_step()

        self.pub.publish(cmd)

    def next_step(self):
        # Stop the robot briefly between steps
        self.pub.publish(Twist())

        self.step += 1
        self.start_time = time.time()

        if self.step < len(self.path):
            self.get_logger().info(
                f"Step {self.step + 1}/{len(self.path)} : {self.path[self.step]}"
            )
        else:
            self.get_logger().info("Maze Finished Successfully!")


def main(args=None):
    rclpy.init(args=args)
    node = AutonomousMover()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # Ensure the robot stops upon exit
    node.pub.publish(Twist())
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()