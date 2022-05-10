#!/usr/bin/env python
import rospy
from open_manipulator_msgs.srv import SetKinematicsPose, SetKinematicsPoseRequest
import time

def move_to(x,y,z,t):
    service_name = "/goal_task_space_path_position_only"
    rospy.wait_for_service(service_name)

    try:
        service = rospy.ServiceProxy(service_name, SetKinematicsPose)

        request = SetKinematicsPoseRequest()
        request.end_effector_name = "gripper"
        request.kinematics_pose.pose.position.x = x
        request.kinematics_pose.pose.position.y = y
        request.kinematics_pose.pose.position.z = z
        request.path_time = t

        response = service(request)
        return response
    except Exception as e:
        rospy.loginfo("%s" % e)
        return False

if __name__ == "__main__":
    rospy.init_node("ros_tutorial")
    rospy.loginfo("ros_tutorial node start")

    xyz_init = (0.287, 0.0, 0.196)
    xyz_home = (0.134, 0.0, 0.240)
    t = 3.0

    rospy.loginfo("Goto home pose!")
    move_to(xyz_home[0], xyz_home[1], xyz_home[2],t)
    time.sleep(t)

    rospy.loginfo("Goto init pose!")
    move_to(xyz_init[0],xyz_init[1],xyz_init[2],t)
    time.sleep(t)

    rospy.loginfo("Goto home pose!")
    move_to(xyz_home[0], xyz_home[1], xyz_home[2],t)
    time.sleep(t)

    rospy.loginfo("ros_tutorial node end! ")



            
