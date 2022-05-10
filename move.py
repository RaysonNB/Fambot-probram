#!/usr/bin/env python
import rospy
from demo3 import RobotChassis
from mr_voice.msg import Voice
from std_msgs.msg import String

def callback_voice(msg):
    global s
    s = msg.text

if __name__ == "__main__":
    rospy.init_node("move_node")
    rospy.loginfo("OK!")
    chassis = RobotChassis()
    P = [
        (0.31, 0.07 ,0.0),
        (0.59, 2.53, 0.18),
        (0.27,0.153,0.111)
    ]
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    s = ""
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if ("take" in s and "break" in s) or "sleep" in s:
            pub_speaker.publish("ok, I will wake you up after I walk for a devotion")
            s = ""
            chassis.move_to(P[1][0], P[1][1], P[1][2])
            while not rospy.is_shutdown():
                rospy.Rate(20).sleep()
                if chassis.status_code == 3: break
            chassis.move_to(P[0][0], P[0][1], P[0][2])
            while not rospy.is_shutdown():
                rospy.Rate(20).sleep()
                if chassis.status_code == 3: break
            chassis.move_to(P[2][0],P[2][1],P[2][2])
            pub_speaker.publish("dear owner, it's time to wake up")
    rospy.loginfo("END")
