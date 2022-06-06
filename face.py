#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge 
import cv2
from openvino_models import FaceDetection, FaceReidentification
import numpy as np

def callBack_image(msg):
    global _image
    _image = CvBridge().imgmsg_to_cv2(msg,"bgr8")

#def checkFace():
if __name__ == "__main__":
    rospy.init_node("demo")
    rospy.loginfo("demo start!")

    rospy.Subscriber("/camera/rgb/image_raw",Image,callBack_image)
    _image = rospy.wait_for_message("/camera/rgb/image_raw", Image)

    path_openvino = "/home/pcms/models/openvino/"
    dnn_face = FaceDetection(path_openvino)
    dnn_faceid = FaceReidentification(path_openvino)
    vec_names = ["Thomas", "William", "Rayson"]
    vec_dicts = {}
    for name in vec_names:
        vec_dicts[name] = np.loadtxt("/home/pcms/catkin_ws/src/beginner_tutorials/%s.txt" % name)
    
    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        frame = _image.copy()

        faces = dnn_face.forward(frame)
        for face in faces:
            x1,y1,x2,y2 = face
            

            img = frame[y1:y2,x1:x2,:]
            cv2.imshow("img",img)
            vec = dnn_faceid.forward(img)

            who = "Unknown"
            for k, v in vec_dicts.items():
                dist = dnn_faceid.compare(vec, v)
                if dist < 0.4:
                    who = k
                    break
            #print(who)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame, who, (x1+5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            #print(dnn_faceid.compare(vec,vec_Thomas))
            #if cv2.waitKey(1) in [32]:
            #   print("Save face id.")
            #   np.savetxt("/home/pcms/catkin_ws/src/beginner_tutorials/Rayson.txt",vec)


        cv2.imshow("frame",frame)
        key_code = cv2.waitKey(1)
        if key_code in [27,ord('q')]:
            break


    rospy.loginfo("demo end")
