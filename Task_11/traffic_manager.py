#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32


class TrafficManager(Node):

    def __init__(self):
        super().__init__("traffic_manager")

        self.safety_zone = 2.0
        self.robots = {}
        self.subscribed_topics = set()

        self.create_timer(1.0, self.discover_robots)
        self.create_timer(1.0, self.check_traffic)

    def discover_robots(self):
        topics = self.get_topic_names_and_types()

        for topic_name, _ in topics:

            if topic_name in self.subscribed_topics:
                continue
            parts = topic_name.split("/")
            if len(parts) < 3:
                continue

            robot_name = parts[1]
            topic_type = parts[2]

            if topic_type == "pose":
                self.create_robot(robot_name)

                self.create_subscription(
                    Pose2D,
                    topic_name,
                    lambda msg, name=robot_name: self.pose_callback(msg, name),
                    10
                )

                self.subscribed_topics.add(topic_name)
                self.get_logger().info(f"Subscribed to {topic_name}")

            elif topic_type == "priority":
                self.create_robot(robot_name)

                self.create_subscription(
                    Int32,
                    topic_name,
                    lambda msg, name=robot_name: self.priority_callback(msg, name),
                    10
                )

                self.subscribed_topics.add(topic_name)
                self.get_logger().info(f"Subscribed to {topic_name}")

    def create_robot(self, robot_name):
        if robot_name not in self.robots:
            self.robots[robot_name] = {
                "x": None,
                "y": None,
                "priority": None
            }

    def pose_callback(self, msg, robot_name):
        self.robots[robot_name]["x"] = msg.x
        self.robots[robot_name]["y"] = msg.y

    def priority_callback(self, msg, robot_name):
        self.robots[robot_name]["priority"] = msg.data

    def check_traffic(self):
        robot_names = list(self.robots.keys())

        for i in range(len(robot_names)):
            for j in range(i + 1, len(robot_names)):

                r1 = robot_names[i]
                r2 = robot_names[j]

                data1 = self.robots[r1]
                data2 = self.robots[r2]
                if None in data1.values() or None in data2.values():
                    continue

                distance = math.sqrt(
                    (data2["x"] - data1["x"]) ** 2 +
                    (data2["y"] - data1["y"]) ** 2
                )

                if distance >= self.safety_zone:
                    self.get_logger().info(
                        f"[CLEAR] {r1} and {r2} safe | distance={distance:.2f}"
                    )

                elif data1["priority"] < data2["priority"]:
                    self.get_logger().warn(
                        f"[DANGER] {r1} should yield to {r2} | distance={distance:.2f}"
                    )

                elif data2["priority"] < data1["priority"]:
                    self.get_logger().warn(
                        f"[DANGER] {r2} should yield to {r1} | distance={distance:.2f}"
                    )
                    
                else:
                    self.get_logger().warn(
                        f"[DANGER] {r1} and {r2} are close with same priority | distance={distance:.2f}"
                    )


def main(args=None):
    rclpy.init(args=args)

    node = TrafficManager()
    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()