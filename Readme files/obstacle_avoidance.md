# Example 6: Obstacle Avoidance

**Goal**: To run the micromouse in a maze with obstacle avoidance.

## Code

`node_obstacle_avoidance.py`

```python
#! /usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None


def clbk_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[0:71]), 10),
        'fright': min(min(msg.ranges[72:143]), 10),
        'front':  min(min(msg.ranges[144:215]), 10),
        'fleft':  min(min(msg.ranges[216:287]), 10),
        'left':   min(min(msg.ranges[288:359]), 10)
    }

    take_action(regions)


def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    d = 0.15

    if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        linear_x = 0.6
        angular_z = 0
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0.3
        angular_z = 0
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)


def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/micromouse/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/micromouse/laser/scan', LaserScan, clbk_laser)

    rospy.spin()


if __name__ == '__main__':
    main()

```

<center><a href="node_obstacle_avoidance.py" download><button>Download</button></a></center>

---