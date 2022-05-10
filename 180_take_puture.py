#!/usr/bin/env python
import rospy
from robot_vision_msgs.msg import BoundingBoxes
from robot_vision_msgs.msg import BoundingBox
from mr_voice.msg import Voice
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
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

def callback_yolo(msg):
    global boxes
    boxes = msg.bounding_boxes


if __name__ == "__main__":
    rospy.init_node("speak_node")
    rospy.loginfo("ros_tutorial node start!")

    frame= None
    boxes = None
    w = 0
    s = ""

    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_Image)
    rospy.Subscriber("/voice/text", Voice, callback_voice)
    rospy.Subscriber("/imu/data", Imu, callback_imu)
    rospy.Subscriber("/yolo_ros/bounding_boxes", BoundingBoxes, callback_yolo)
    
    pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)

    rospy.sleep(1)

    msg_cmd_vel = Twist()
    while abs(w) < 0.9:
        rospy.Rate(20).sleep()
        msg_cmd_vel.linear.x = 0.0
        msg_cmd_vel.angular.z = 1.0
        pub_cmd_vel.publish(msg_cmd_vel)
    msg_cmd_vel.linear.x = 0.0
    msg_cmd_vel.angular.z = 0.0
    pub_cmd_vel.publish(msg_cmd_vel)

    while True:
        rospy.Rate(27).sleep()
        if frame is None: continue
        cv2.imshow("frame",frame)

        key_code = cv2.waitKey(1)
        if key_code in [ord('q'), 27]:
            break
        if boxes is not None:
            cnt = 0
            for box in boxes:
                if box.Class == "person":
                    cnt += 1
            pub_speaker.publish("there are " + str(cnt) + " people")
            cv2.waitKey(0)
            break
    
    rospy.loginfo("END")
    cv2.destroyAllWindows()

