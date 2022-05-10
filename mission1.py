#!/usr/bin/env python
import rospy
from mr_voice.msg import Voice
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist

def callback_voice(msg):
    global voice
    voice = msg

def callback_imu(msg):
    global imu
    imu = msg

def imu2yaw(data):
    x = data.orientation.x
    y = data.orientation.y
    z = data.orientation.z
    w = data.orientation.w
    roll, pitch, yaw = euler_from_quaternion([x, y, z, w])
    return yaw

def calc_target(yaw, direction):
    pi = 3.14
    a = direction * pi / 180
    b = yaw
    if b < 0: b += 2 * pi
    t = a + b
    if t > 2 * pi: t -= 2 * pi
    if t > pi: t -= 2 * pi
    return t
    
if __name__ == "__main__":
    rospy.init_node("mission1")
    rospy.loginfo("mission1 started!")

    # 1. voice 
    # 2. imu
    # 3. control

    voice = None
    rospy.Subscriber("/voice/text", Voice, callback_voice)

    imu = None
    rospy.Subscriber("/imu/data", Imu, callback_imu)

    msg_cmd_vel = Twist()
    pub_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    while not rospy.is_shutdown():
        rospy.Rate(20).sleep()
        if imu is None: continue

        yaw = imu2yaw(imu)
        rospy.loginfo("%.4f" % yaw)

        if voice is not None:
            rospy.loginfo("%s(%d)" % (voice.text, voice.direction))

            target = calc_target(yaw, voice.direction)
            rospy.loginfo("target: %.4f" % target)

            msg_cmd_vel.linear.x = 0
            msg_cmd_vel.angular.z = 0.5
            while abs(target - yaw) > 0.2:
                rospy.Rate(20).sleep()
                yaw = imu2yaw(imu)
                pub_cmd_vel.publish(msg_cmd_vel)
            msg_cmd_vel.linear.x = 0
            msg_cmd_vel.angular.z = 0.0
            pub_cmd_vel.publish(msg_cmd_vel)

            voice = None

        














