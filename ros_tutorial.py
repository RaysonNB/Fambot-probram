#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

if __name__ == "__main__":
    rospy.init_node("ros_tutorial")
    rospy.loginfo("ros_tutorial node start!")
    
    cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    velocity = 0.5
    target_distance = 3.0
    current_distance = 0.0

    msg = Twist()
    msg.linear.x = velocity
    msg.angular.z = 0.0

    while not rospy.is_shutdown():
    
        t0 = rospy.Time.now().to_sec()
        while current_distance < target_distance:
            cmd_vel.publish(msg)
            t1 = rospy.Time.now().to_sec()
            current_distance = velocity * (t1 - t0)

        msg.linear.x = 0.0
        cmd_vel.publish(msg)

    rospy.loginfo("ros_tutorial node end!")
