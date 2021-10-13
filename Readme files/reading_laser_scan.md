# Example 1: Reading Laser Scan

**Goal**: Subscribe to `/micromouse/laser/scan` rostopic and print laser values.


## Code

`node_reading_laser.py`

```python
#! /usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan


def clbk_laser(msg):
    # 720 / 10 = 72
    regions = [
        min(min(msg.ranges[0:71]), 10),
        min(min(msg.ranges[72:143]), 10),
        min(min(msg.ranges[144:215]), 10),
        min(min(msg.ranges[216:287]), 10),
        min(min(msg.ranges[288:359]), 10),
        min(min(msg.ranges[360:431]), 10),
        min(min(msg.ranges[432:503]), 10),
        min(min(msg.ranges[504:575]), 10),
        min(min(msg.ranges[576:647]), 10),
        min(min(msg.ranges[648:719]), 10)
    ]
    rospy.loginfo(regions)


def main():
    rospy.init_node('reading_laser')

    sub = rospy.Subscriber('/micromouse/laser/scan', LaserScan, clbk_laser)

    rospy.spin()


if __name__ == '__main__':
    main()
    
```

<center><a href="node_reading_laser.py" download><button>Download</button></a></center>

---