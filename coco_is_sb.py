#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String
from demo3 import RobotChassis

def callback_voice(msg):
    global s
    s = msg.text
if __name__ == "__main__":
    rospy.init
    rospy.loginfo("5_4 start!")
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    chassis=RobotChassis
    s=""
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        for i in range(len(s)):
            if ord(s[i]) >= 65 and ord(s[i]) <= 90:
                s[i] = chr(ord(s[i])+32)
        s = s.split(" ")
        if "john" in s:
            pub_speaker.publish("ok")
            chassis.move_to(-0.50,4.55,0.0)
            s=""


