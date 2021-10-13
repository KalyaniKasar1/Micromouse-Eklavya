# Example 5: Maze Runner

**Goal**: To run the micromouse in a maze.

## Code

`node_maze_runner.py`

```python
#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

# Global Variables
sensor_l, sensor_c, sensor_r = 0, 0, 0
pub = 0


def clbk_laser(msg):
    global sensor_l, sensor_c, sensor_r
    # 720 / 10 = 72
    regions = [
        round(100*min(min(msg.ranges[0:71]), 100)),
        round(100*min(min(msg.ranges[72:143]), 100)),
        round(100*min(min(msg.ranges[144:215]), 100)),
        round(100*min(min(msg.ranges[216:287]), 100)),
        round(100*min(min(msg.ranges[288:359]), 100)),
        round(100*min(min(msg.ranges[360:431]), 100)),
        round(100*min(min(msg.ranges[432:503]), 100)),
        round(100*min(min(msg.ranges[504:575]), 100)),
        round(100*min(min(msg.ranges[576:647]), 100)),
        round(100*min(min(msg.ranges[648:719]), 100))
    ]
    # rospy.loginfo(regions)
    print("l: {} \t c: {} \t r: {}".format(regions[4], regions[2], regions[0]))

    sensor_l = regions[4]
    sensor_c = regions[2]
    sensor_r = regions[0]

    # print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r))


def motion_go_straight():
    global pub
    msg = Twist()
    msg.linear.x = 0.5
    pub.publish(msg)


def motion_stop():
    global pub
    msg = Twist()
    msg.linear.x = 0.0
    pub.publish(msg)


def main():

    global sensor_l, sensor_c, sensor_r
    global pub

    msg = Twist()

    rospy.init_node('node_maze_runner')

    sub = rospy.Subscriber('/micromouse/laser/scan', LaserScan, clbk_laser)
    pub = rospy.Publisher('/micromouse/cmd_vel', Twist, queue_size=1)

    # pub.publish(msg)

    # rospy.spin()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        print("l: {} \t c: {} \t r: {}".format(sensor_l, sensor_c, sensor_r))
        if(sensor_c > 9):
            motion_go_straight()
        else:
            motion_stop()

        rate.sleep()


if __name__ == '__main__':
    main()

```

<center><a href="node_maze_runner.py" download><button>Download</button></a></center>

---