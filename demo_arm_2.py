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


if __name__ == "__main__":
    rospy.init_node("ros_tutorial")
    rospy.loginfo("ros_tutorial node start!")
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    publisher_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    s=""
    publisher_speaker.publish("start")
    rospy.loginfo("ros_tutorial node start!!!!!!!!!!!!")
    t = 1.0
    ttt=3.0
    xyz_init = (0.288,0.0,0.194)
    xyz_home = (0.134,0.0,0.240)

    rospy.loginfo("ros_tutorial node start!!!!!!!!!!!!")
    while not rospy.is_shutdown():
        rospy.loginfo(s)
        rospy.Rate(20).sleep()
        if len(s)== 0:
            continue
        else:
            if  'bring' in s  or 'grab' in s or 'have' in s or 'obtain' in s or 'pick up' in s or 'pull' in s or 'receive' in s or 'take' in s or 'fetch' in s or 'bottle' in s:
                publisher_speaker.publish("I am going to get it now")
                open_gripper(t)
                time.sleep(t)
                time.sleep(2)
                publisher_speaker.publish("May I get it now?")
                rospy.loginfo(s)
            if "ok" in s or "OK" in s or "yes" in s:
                publisher_speaker.publish("get in now")
                close_gripper(t)
                time.sleep(t)
            if "come" in s and "get" in s:
                move_to(xyz_home[0],xyz_home[1],xyz_home[2],ttt)
                time.sleep(ttt)
                move_to(xyz_init[0],xyz_init[1],xyz_init[2],ttt)
                open_gripper(t)
                time.sleep(t)
                time.sleep(ttt)
                close_gripper(t)
                time.sleep(t)
                move_to(xyz_home[0],xyz_home[1],xyz_home[2],ttt)

                time.sleep(ttt)
                
                rospy.loginfo("finish grabbing!!!!")
            elif 'handsome' in s or 'person ' in s:
                 publisher_speaker.publish("I think that Justin Trudeau is very handsome.")
            elif 'zones' in s or 'zone' in s :
                 publisher_speaker.publish("Canada spans almost 10 million square km and comprises 6 time zones.")
            elif 'longest' in s:
                 publisher_speaker.publish("Yonge Street in Ontario is the longest street in the world.")
            elif 'how' in s or 'long'in s :
                 publisher_speaker.publish("Yonge street is almost 2,000 km, starting at Lake Ontario, and running north to the Minnesota border.")
            elif 'London' in s or '1915' in s or 'london' in s:
                 publisher_speaker.publish("The bear cub was named Winnipeg. It inspired the stories of Winnie-the-Pooh.")
            s =""
            
            
        
            
            
