#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64


def servo_cmd(servo_val, flag):
    pub = rospy.Publisher('/simple_model/base_to_second_joint_position_controller/command', Float64, queue_size=40)
    pub2 = rospy.Publisher('/simple_model/base_to_first_joint_position_controller/command', Float64, queue_size=40)
    rospy.init_node('servo_cmd', anonymous=True)
    rate = rospy.Rate(50) # 40hz
    while not rospy.is_shutdown():
        pub.publish(0.2)
        pub2.publish(0.2)
        rate.sleep()
servo_val = 0.0
flag = 0.0
if __name__ == '__main__':
    try:
        servo_cmd(servo_val, flag)
    except rospy.ROSInterruptException:
        pass
