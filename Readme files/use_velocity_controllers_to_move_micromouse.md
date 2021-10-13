# Example 3: Use Velocity Controller to move Micromouse

**Goal**: Control each micromouse wheel separately by publishing on each topic.

## Code

`velocity_controller.py`

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64


def servo_cmd(servo_val, flag):
    pub = rospy.Publisher(
        '/micromouse/left_wheel_joint_velocity_controller/command', Float64, queue_size=40)
    pub2 = rospy.Publisher(
        '/micromouse/right_wheel_joint_velocity_controller/command', Float64, queue_size=40)
    rospy.init_node('servo_cmd', anonymous=True)
    rate = rospy.Rate(50)  # 50hz
    while not rospy.is_shutdown():
        pub.publish(5.0)
        pub2.publish(5.0)
        rate.sleep()


servo_val = 0.0
flag = 0.0
if __name__ == '__main__':
    try:
        servo_cmd(servo_val, flag)
    except rospy.ROSInterruptException:
        pass

```

<center><a href="velocity_controller.py" download><button>Download</button></a></center>

<br/>

> **Note 1**: Load the yaml file `velocity_controller.yaml` in config directory first.

> **Note 2**: Use ROS_CONTROL Package provided by ROS. Just read the file and `micromouse_bot.gazebo` and uncomment the plugin and use `velocity_controller.py` for further references.

---