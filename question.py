#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String

def callback_voice(msg):
    global s
    s = msg.text

if __name__ == "__main__":
    rospy.init_node("speak_node")
    rospy.loginfo("speak_node started!")

    rospy.Subscriber("/voice/text", Voice, callback_voice)
    publisher_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    s=""
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if len(s)== 0:
            continue
        else:
           #for i in range(len(s)):
            #    if ord(s[i]) >= 65 and ord(s[i]) <= 90:
             #       s[i] = chr(ord(s[i])+32)
            if 'handsome' in s or 'person ' in s:
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

