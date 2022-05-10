#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from std_msgs.msg import String
from demo3 import RobotChassis
from robot_vision_msgs.msg import BoundingBoxes
from robot_vision_msgs.msg import BoundingBox
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
import cv2
from cv_bridge import CvBridge

def callback_voice(msg):
    global s
    s = msg.text
def callback_yolo(msg):
    global boxes
    boxes = msg.bounding_boxes
def callback_Image(msg):
    global frame
    frame = CvBridge().imgmsg_to_cv2(msg,"bgr8")
def callback_imu(msg):
    global w
    w = msg.orientation.w
if __name__ == "__main__":
    rospy.init_node("3_24")
    frame=None
    boxes = None
    rospy.loginfo("3_24 start!")
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    rospy.Subscriber("/imu/data", Imu, callback_imu)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    chassis = RobotChassis()
    pub_cmd_vel=rospy.Publisher("/cmd_vel",Twist,queue_size=10)
    rospy.Subscriber("/yolo_ros/bounding_boxes",BoundingBoxes,callback_yolo)
    rospy.Subscriber("/camera/rgb/image_raw",Image,callback_Image)
    
    s=""
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if len(s)== 0:
            continue
        else:
            if "hi" in s:

                pub_speaker.publish("ok")
                chassis.move_to(-0.2,3.6,-0.0)
                while not rospy.is_shutdown():
                    rospy.Rate(20).sleep()
                    if chassis.status_code == 3: break
                pub_speaker.publish("I arrived")

                msg_cmd_vel = Twist()
                while True:
                    rospy.Rate(20).sleep()
                    msg_cmd_vel.linear.x = 0.0
                    msg_cmd_vel.angular.z = 1.0
                    pub_cmd_vel.publish(msg_cmd_vel)
                    if frame is None: continue
                    cv2.imshow("frame", frame)
                    if boxes is not None:
                        found = False
                        for box in boxes:
                            rospy.loginfo(box.Class)
                            if box.Class == "person":
                                found = True
                                pub_speaker.publish("I find a person")
                                break  
                        if found: 
                            sv=0.75
                            while sv >= 0:
                                msg_cmd_vel.linear.x = 0.0
                                msg_cmd_vel.angular.z = sv
                                pub_cmd_vel.publish(msg_cmd_vel)
                                sv -= 0.25                     
                            break
                
                s=""
    rospy.loginfo("END")
    cv2.destroyAllWindows()


