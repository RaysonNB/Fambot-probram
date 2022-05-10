#!/usr/bin/env python
import rospy
from demo3 import RobotChassis

if __name__ == "__main__":
    rospy.init_node("demo2")
    rospy.loginfo("demo2 started!")
    chassis = RobotChassis()
    P = [
        (0.31, 0.07 ,0.0),
        (0.59, 2.53, 0.18)
    ]
    while True:
        chassis.move_to(P[1][0], P[1][1], P[1][2])
        while not rospy.is_shutdown():
            rospy.Rate(20).sleep()
            if chassis.status_code == 3:
                break 
        chassis.move_to(P[0][0], P[0][1], P[0][2])
        while not rospy.is_shutdown():
            rospy.Rate(20).sleep() 
            if chassis.status_code == 3:
                break
	chassis.shutdown()
	rospy.loginfo("END")
