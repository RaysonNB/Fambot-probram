#!/usr/bin/env python
import rospy
from robot_vision_msgs.msg import BoundingBoxes
from robot_vision_msgs.msg import BoundingBox


def callback_yolo(msg):
    global boxes
    boxes = msg.bounding_boxes


if __name__ == "__main__":
    rospy.init_node("yolo_demo")
    rospy.loginfo("yolo_demo node started!")

    boxes = None
    rospy.Subscriber("/yolo_ros/bounding_boxes", BoundingBoxes, callback_yolo)
    #rospy.wait_for_message("/yolo_ros/bounding_boxes")

    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if boxes is not None:
            cnt = 0
            for box in boxes:
                if box.Class == "person":
                    cnt += 1
            rospy.loginfo("Person: %d" % cnt)

