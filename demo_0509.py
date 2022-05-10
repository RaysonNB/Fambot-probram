#!/usr/bin/env python
import rospy
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
from open_manipulator_msgs.srv import SetKinematicsPose, SetKinematicsPoseRequest
import time
from mr_voice.msg import Voice
from std_msgs.msg import String

def callback_voice(msg):
    global s
    s = msg.text

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

def say(g):
    publisher_speaker.publish(g)
if __name__ == "__main__":
    rospy.init_node("ros_tutorial")
    rospy.loginfo("ros_tutorial node start!")

    s = ""
    rospy.Subscriber("/voice/text", Voice, callback_voice)

    publisher_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    time.sleep(0.5)
    publisher_speaker.publish("start")

    xyz_init = (0.288,0.0,0.194)
    xyz_home = (0.134,0.0,0.240)
    open_gripper(1.0)
    move_to(xyz_home[0], xyz_home[1], xyz_home[2], 3.0)

    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if s == "": continue

        if "open" in s:
            open_gripper(1.0)
            say("open")
        elif "close" in s:
            close_gripper(1.0)
            say("close")
        elif "help" in s:
            move_to(xyz_init[0], xyz_init[1], xyz_init[2], 3.0)
        elif "OK" in s:
            move_to(xyz_home[0], xyz_home[1], xyz_home[2], 3.0)
        else:
            rospy.loginfo("Unknown: %s" % s)

        s = ""

