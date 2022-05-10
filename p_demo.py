#!/usr/bin/env python
import rospy
from robot_vision_msgs.msg import BoundingBoxes
from robot_vision_msgs.msg import BoundingBox
from std_msgs.msg import String

def yolo_callback(msg):
    global boxes
    boxes = msg.bounding_boxes
    
if __name__ == "__main__":
    rospy.init_node("turtlezai")
    rospy.loginfo("The programme is started!")
    boxes = None
    rospy.Subscriber("/yolo_ros/bounding_boxes",BoundingBoxes,yolo_callback)
    b = 0
    pub_speaker = rospy.Publisher("/speaker/say", String, queue_size=10)
    
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if boxes is not None:
            p = 0
            for box in boxes:
                if box.Class == "person":
                    p+=1
                    
            if b != p:
                rospy.loginfo("person: %d" % p)
                pub_speaker.publish("there are %d people" % p)
                rospy.sleep(1)
            b = p
