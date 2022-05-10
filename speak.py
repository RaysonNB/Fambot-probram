#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String

def callback_voice(msg):
    global s
    s = msg.text


if __name__ == "__main__":
    rospy.init_node("speak_node")
    rospy.loginfo("OK")
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    s = ""
    for i in range(len(s)):
        if ord(s[i]) >= 65 and ord(s[i]) <= 90:
            s[i] = chr(ord(s[i])+32)
    s = s.split(" ")
    t = 0
    d = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12}
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if "sleep" in s:
            pub_speaker.publish("ok, when do you get up tomorrow")
        elif "get up" in s and "at" in s:
            for k, v in d.items():
                    s = s.replace(k, str(v))
            rospy.loginfo(s)
            t = 0
            for i in range(len(s)):
                    if ord(s[i]) >= ord('0') and ord(s[i]) <= ord('9'):
                        t = t * 10 + int(s[i])
            rospy.loginfo(str(t))
            pub_speaker.publish("ok, the alarm will ring at %d"%t)
        elif "hungry" in s or ("food" in s and "eat" in s):
            pub_speaker.publish("dear owner,what would you like to eat?")
        s = ""
