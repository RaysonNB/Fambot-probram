#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


def callback_voice(msg):
    global s
    s = msg.text

def callback_imu(msg):
    global w
    w = msg.orientation.w
def callback_Image(msg):
    global frame
    frame = CvBridge().imgmsg_to_cv2(msg,"bgr8")

if __name__ == "__main__":
    rospy.init_node("speak_node")
    rospy.loginfo("ros_tutorial node start!")
    frame= None
    topic_name="/camera/rgb/image_raw"
    rospy.Subscriber(topic_name, Image, callback_Image)
    rospy.wait_for_message(topic_name,Image)
    rospy.loginfo("OK")
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_Image)
    rospy.Subscriber("/imu/data", Imu, callback_imu)
    pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.sleep(1)
    msg_cmd_vel = Twist()
    w = 0
    while abs(w) < 0.9:
        rospy.Rate(20).sleep()
        msg_cmd_vel.linear.x = 0.0
        msg_cmd_vel.angular.z = 1.0
        pub_cmd_vel.publish(msg_cmd_vel)
    msg_cmd_vel.linear.x = 0.0
    msg_cmd_vel.angular.z = 0.0
    pub_cmd_vel.publish(msg_cmd_vel)
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if frame is None: continue
        cv2.imshow("frame",frame)

        key_code = cv2.waitKey(1)
        if key_code in [ord('q'),27]:
            break
    cv2.destroyAllWindows()
'''
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    s = ""
    for i in range(len(s)):
        if ord(s[i]) >= 65 and ord(s[i]) <= 90:
            s[i] = chr(ord(s[i])+32)
    s = s.split(" ")
    t = 0
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if "photo" in s:
            pub_speaker.publish("ok")
            chassis = RobotChassis()
	chassis.shutdown()
	rospy.loginfo("END")
        s = ""
'''

