#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32


class Fleet(Node): 
    def __init__(self):
        super().__init__("fleet_emulator") 
        self.declare_parameter("x", 0.0)
        self.declare_parameter("y", 0.0)
        self.declare_parameter("theta", 0.0)
        self.declare_parameter("priority", 1)
        

        self.x = self.get_parameter("x").value
        self.y = self.get_parameter("y").value
        self.theta = self.get_parameter("theta").value
        self.priority = self.get_parameter("priority").value    

        self.pose_publisher_ = self.create_publisher(Pose2D, "pose", 10)
        self.priority_publisher_ = self.create_publisher(Int32, "priority", 10)
        self.timer_ = self.create_timer(0.1, self.publish_data)

    def publish_data(self):
        pose_msg = Pose2D()
        pose_msg.x = self.x
        pose_msg.y = self.y
        pose_msg.theta = self.theta

        priority_msg = Int32()
        priority_msg.data = self.priority

        self.pose_publisher_.publish(pose_msg)
        self.priority_publisher_.publish(priority_msg)

        self.get_logger().info(f"Position: ({self.x}, {self.y}) & Priority: {self.priority}")
    



def main(args=None):
    rclpy.init(args=args)
    node = Fleet() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()