#!/usr/bin/env python
import rospy
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
import time


def set_gripper(angle, t):
    service_name = "/goal_tool_control"
    rospy.wait_for_service(service_name)
    
    try:
        service = rospy.ServiceProxy(service_name, SetJointPosition)
        
        request = SetJointPositionRequest()
        request.joint_position.joint_name = ["gripper"]
        request.joint_position.position = [angle]
        request.path_time = t
        
        response = service(request)
        return response
    except Exception as e:
        rospy.loginfo("%s" % e)
        return False

def open_gripper(t):
    return set_gripper(0.01, t)

def close_gripper(t):
    return set_gripper(-0.01, t)


if __name__ == "__main__":
    rospy.init_node("ros_tutorial")
    rospy.loginfo("ros_tutorial node start!")
    
    t = 1.0
    
    set_gripper(0.0, t)
    time.sleep(t)
    
    open_gripper(t)
    time.sleep(t)
    
    close_gripper(t)
    time.sleep(t)
    
    rospy.loginfo("ros_tutorial node end!")
