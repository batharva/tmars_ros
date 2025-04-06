import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.get_logger().info("Teleop Keyboard Node Started. Use W/A/S/D to move, Q to quit")
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.run()
    
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def run(self):
        twist = Twist()
        while rclpy.ok():
            key = self.get_key().lower()
            if key == 'w':
                twist.linear.x = 0.5
                twist.linear.y = 0.0
                twist.angular.z = 0.0
            elif key == 'x':
                twist.linear.x = -0.5
                twist.linear.y = 0.0
                twist.angular.z = 0.0
            elif key == 'a':
                # twist.linear.x = 0.25
                # twist.linear.y = 0.5
                twist.angular.z = 0.5
            elif key == 'd':
                # twist.linear.x = 0.25
                # twist.linear.y = -0.5
                twist.angular.z = -0.5
            elif key == 'q':
                self.get_logger().info("Stopping...")
                break
            else:
                twist.linear.x = 0.0
                twist.linear.y = 0.0
                twist.angular.z = 0.0  # No rotation
            self.cmd_vel_pub.publish(twist)
        
        self.stop()
    
    def stop(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        self.destroy_node()
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = TeleopKeyboard()
    
if __name__ == '__main__':
    main()
