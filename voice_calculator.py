#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String

def callback_voice(msg):
    global s

    s = msg.text

def callback_calculator(num2):
    a = 0
    b = 0
    ans = 0
    num = ""
    for i in range(len(num2)):
        if num2[i] != "A" or num2[i] != "B":
            print(num2[i])
            num += num2[i]
    num = num.strip().split(" ")
    print(num)
  #  for i in range(len(num)):
   #     if ord(num[i]) >= 65 and ord(num[i]) <= 90:
    #        num[i] = chr(ord(num[i])+32)
    if len(num)==3:
        k = 0
    else:
        k = 1
    d = {"one":1,"One":1,"two":2,"to":2,"Two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"line":9,"ten":10,"eleven":11,"twelve":12}
    if len(num) < 3:
        rospy.loginfo("error len(num) < 3")
    else:
        print(num[k] in d, num[k+2] in d)
        if num[k] in d and num[k+2] in d:
            a = d[num[k]]
            b = d[num[k+2]]
            print(a,b)
        else:
            a = int(num[k])
            b = int(num[k])
        if num[k+1]=="plus" or num[k+1]=="bus":
            rospy.loginfo("ok")
            ans = a+b
        elif num[k+1] == "minus":
            ans = a-b
        elif num[k+1] == "times":
            ans = a*b
        elif num[k+1] == "into":
            ans = a/b
        rospy.loginfo('Ans: {}'.format(ans))
        return str(ans)
    return "somthing wrong"

if __name__ == "__main__":
    rospy.init_node("voice_calculator")
    rospy.loginfo("start")
    s = ""
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if "calculate" in s:
            rospy.loginfo("calculate")
            pub_speaker.publish("OK, what can I help you to calculate")
            s = ""
            while True:
                if len(s) > 1:
                    pub_speaker.publish(callback_calculator(s))
                    break
                else:
                    s=""
        else:
            rospy.loginfo("nothing: %s" % s)

