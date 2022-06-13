#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String
def say(g):
    publisher_speaker.publish(g)
    rospy.sleep(1)
def callback_voice(msg):
    global s
    s = msg.text
def answer(text, aaa):
    for d in aaa:
        res_AND = True
        for keys in d["K"]:
            res_OR = False
            for key in keys:
                if key[0] == "!":
                    res_OR = res_OR or key[1:] not in text
                else:
                    res_OR = res_OR or key in text
            res_AND = res_OR and res_AND
        if res_AND:
            return d["A"]
    return ""


def load_data(f_n):
    data = []
    f = open(f_n, "r")
    lines = [x.strip().lower() for x in f.readlines()]
    status = "N"
    for i in range(len(lines)):
        if len(lines[i]) == 0:
            data.append({"Q": "", "A": "", "K": []})
            status = "Q"
        elif status == "Q":
            data[-1]["Q"] = lines[i]
            status = "A"
        elif status == "A":
            data[-1]["A"] = lines[i]
            status = "K"
        elif status == "K":
            keys = [x.strip() for x in lines[i].split(",")]
            data[-1]["K"].append(keys)
    f.close()
    return data

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
if __name__ == "__main__":
    rospy.init_node("speak_node")
    rospy.loginfo("speak_node started!")
    data = load_data("wh.txt")
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    publisher_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    s=""
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        ab=answer(s, data)
        if len(s)== 0:
            continue
        elif "*" in ab:
            open_gripper(t)
        else:
            say(ab)
            rospy.loginfo(s)
            s=""
