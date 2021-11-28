# __THE MICROMOUSE PROJECT__
Micromouse competitions originated in Japan in the late 1970s, and soon spread to the rest of the world. 
A micromouse is a small, but fast bot that can find its way from the start position of a 16x16 wooden maze to its center, unaided, in a matter of seconds. The mouse will have to keep track of where it is, discover walls as it explores the maze, map out the maze and then find the shortest possible path to its centre.
The micromouse is allowed 7 minutes and 7 dry runs to map the maze, find the path to the centre, memorise the path and then make the fastest possible run to the centre. The mouse which reaches the centre in the shortest time wins! :smiley:

## Table of Contents
* [About the Project](#about-the-project)
  * [Tech Stack](#tech-stack)
  * [File Structure](#file-structure)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Execution](#execution)
* [Theory and Approach](#theory-and-approach)
* [Results and Demo](#results-and-demo)
* [Future Work](#future-work)
* [Contributors](#contributors)
* [Acknowledgements and Resources](#acknowledgements-and-resources)
* [License](#license)

## About the project
![Screenshot from 2021-10-24 11-43-34.png](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/assets/Screenshot%20from%202021-10-24%2011-43-34.png)

![Screenshot from 2021-10-24 11-43-54.png](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/assets/Screenshot%20from%202021-10-24%2011-43-54.png)




#### AIM
Our aim is to make the micromouse capable of reaching the centre of the given maze in the shortest possible time using maze solving algorithms. As of now, I have implemented the left follow algorithm on it. The right follow algorithm is similar but the opposite. The micromouse bot also somewhat requires PID tuning to stay in the centre of the path.

### Tech Stack
- [ROS Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu)
- [Gazebo 11](http://gazebosim.org/)
- [Python 3](https://www.python.org/downloads/)

### File Structure
```
 ┣ 📂.git
 ┣ 📂assets
 ┃ ┣ 📜Micromouse Problem Statement.pdf                               
 ┃ ┣ 📜README.md
 ┃ ┣ 📜ROS-Learning-resources.md
 ┃ ┣ 📜Screencast from 24-10-21 03 29 56 PM IST.mp4
 ┃ ┣ 📜Screencast from 24-10-21 03 35 50 PM IST.mp4
 ┃ ┣ 📜Screencast from 24-10-21 03 38 05 PM IST.mp4
 ┃ ┣ 📜Screencast from 24-10-21 03 39 31 PM IST.mp4
 ┃ ┣ 📜Screencast from 24-10-21 03 47 10 PM IST.mp4
 ┃ ┣ 📜Screencast_from_24-10-21_03_29_56_PM_IST_SparkVideo.gif
 ┃ ┣ 📜Screencast_from_24-10-21_03_35_50_PM_IST_SparkVideo.gif
 ┃ ┣ 📜Screencast_from_24-10-21_03_38_05_PM_IST_SparkVideo.gif
 ┃ ┣ 📜Screencast_from_24-10-21_03_39_31_PM_IST_SparkVideo.gif
 ┃ ┣ 📜Screencast_from_24-10-21_03_47_10_PM_IST_SparkVideo.gif
 ┃ ┣ 📜Screenshot from 2021-10-24 11-43-34.png
 ┃ ┣ 📜Screenshot from 2021-10-24 11-43-54.png
 ┃ ┣ 📜Screenshot from 2021-10-24 11-44-06.png
 ┃ ┗ 📜Screenshot from 2021-10-24 11-44-55.png
 ┣ 📂config
 ┃ ┗ 📜pos_control.yaml
 ┣ 📂launch
 ┃ ┣ 📜final.launch
 ┃ ┣ 📜gazebo.launch
 ┃ ┗ 📜rviz.launch
 ┣ 📂rviz
 ┃ ┣ 📜rviz_config.rviz
 ┃ ┗ 📜rviz_scan_config.rviz
 ┣ 📂scripts
 ┃ ┣ 📂Algorithms
 ┃ ┃ ┣ 📜bot.py
 ┃ ┃ ┣ 📜node_left_follow.py
 ┃ ┃ ┗ 📜read_laser.py
 ┃ ┗ 📂legacy
 ┃ ┃ ┣ 📜cmd_vel_robot.py
 ┃ ┃ ┣ 📜node_follow_wall.py
 ┃ ┃ ┣ 📜node_go_to_point.py
 ┃ ┃ ┣ 📜node_maze_runner.py
 ┃ ┃ ┣ 📜node_obstacle_avoidance.py
 ┃ ┃ ┣ 📜node_reading_laser.py
 ┃ ┃ ┣ 📜position_controller.py
 ┃ ┃ ┗ 📜velocity_controller.py
 ┣ 📂urdf
 ┃ ┗ 📜micromouse_robot.urdf
 ┣ 📂world
 ┃ ┣ 📜arena.world
 ┃ ┗ 📜my_arena.world
 ┣ 📜.gitignore
 ┣ 📜CMakeLists.txt
 ┣ 📜Micromouse Problem Statement.pdf
 ┣ 📜package.xml
 ┗ 📜readme.md
 ```
 
## Getting Started

### Prerequisites
    1. ROS Noetic
    2. Gazebo Version: 11.0
    3. RViz (not compulsory)

* You can find the video demonstration link for installtion of ROS Noetic  [here](https://www.youtube.com/watch?v=ZA7u2XPmnlo) and the website link for the same [here](http://wiki.ros.org/noetic/Installation/Ubuntu).
* The link to install Gazebo for Ubuntu is provided [here](http://gazebosim.org/tutorials?tut=install_ubuntu). You can find the instructions to install different versions of Gazebo in the link provided above but using Gazebo 11.0 is recommended for ROS Noetic.
* The link to install RViz on Ubuntu is provided [here](https://zoomadmin.com/HowToInstall/UbuntuPackage/rviz).

### Installation

```sh
git clone https://github.com/KalyaniKasar1/Micromouse-Eklavya.git
```
Add this folder in the src directory of your catkin workspace
Create the src folder if it doesn't already exist by
```sh
mkdir src
```
Initialise the project with
```sh
catkin_make
source /opt/ros/noetic/setup.bash      #run this and the command below everytime
source ~/catkin_ws/devel/setup.bash     you need to launch nodes 
```

### Execution
Open two terminal windows and run the following commands
- Terminal 1
```sh
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
roslaunch pkg_techfest_imc gazebo.launch
```
- Terminal 2
```sh
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
rosrun pkg_techfest_imc node_left_follow.py
```

## Theory and Approach
* I had already obtained the urdf model of the micromouse and the model of the maze, which had to be  spawned in Gazebo. So I didn’t need to design them on my own.
* Starting with the basics, the robot needs to move forward (maximum permitted speed is 0.4 m/s) and take left, right or U turns as per it needs. So for these `msg.linear.x` and `msg.angular.z` velocities are published to the cmd_vel topic of the bot in the form of `geometry_msgs/Twist` messages. 
* Next, it needs to read and take in its surroundings in order to perceive what movements it has to make. For this, there is a laser scanner at the front of the bot that sends out 360 beams in an area spanning -90 to +90 degrees in front of it. Each degree of the region in front of the bot has 2 beams. These beams hit the walls of the maze and get reflected back to the bot; they are received by a receiver which can then perceive the distance at which the beam got reflected. Thus, 360 different values are obtained by the receiver in the form of `sensor_msgs/LaserScan` messages, which are then published to the `/my_mm_robot/laser/scan` topic; Here, `msg.ranges[ : ]` returns a list of values of the distance detected by each beam in the range selected by list slicing. The 0th beam is the rightmost beam, while the 359th beam is the leftmost, and all the beams released from the front of the micromouse (lets call it mmc, shall we?).
* For determination of rotation, yaw of the mmc is obtained from its quaternion values, which in turn are obtained from the `/odom` topic in the form of Odometry messages from a callback function. These values are then converted to the Euler angles of yaw, roll and pitch, using a function from `tf.transformations` called `euler_from_quaternion`. Rotation of the mmc is done using the obtained yaw values, as given in the code inside `bot.py`, instead of using `time`, since it is very unreliable. :confused:
```
def clbk_odom(self,msg):
		orientation_q = msg.pose.pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(_, _, self.yaw) = euler_from_quaternion (orientation_list)  #yaw=0.0 is north direction
    
	def rotate(self,targ):  
		kp=0.95  # kp will control the speed of rotation and increase the precision of turns 
		print("Rotating to yaw %5.2f..." %targ)
		while True :
			target_rad = targ * math.pi/180
			self.msg1.angular.z = kp * (target_rad-self.yaw)  #angular velocity published to the bot is proportional to the difference between its current and target values
			#print("Velocity: ", self.msg1.angular.z )
			self.msg1.linear.x = 0
			yaw_deg = (self.yaw*180/math.pi)  # yaw value in degrees
			if (round(yaw_deg) != targ) :
				self.pub.publish(self.msg1)
				#print("target=%5.2f current:%5.2f" %(targ,yaw_deg))
			else :    
				print("Robot successfully turned!")
				self.msg1.linear.x = 0
				self.msg1.angular.z = 0
				self.pub.publish(self.msg1)
				break
		pass 
```
* Various algorithms like left or right follow rule, flood-fill, DFS, BFS, Djikstra’s algorithm or A * algorithm, etc can be used. For now, I have implemented the basic left follow algorithm to solve the maze.
* PID too needs to be used to keep the bot at the centre of the path and so that it doesn’t collide with the walls gradually, make unnecessary turns & increase the time taken to solve the maze, or get stuck in a loop of collisions.

## Results and Demo
Initial position of micromouse in the maze :
![Screenshot from 2021-10-24 11-44-06.png](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/assets/Screenshot%20from%202021-10-24%2011-44-06.png)

Clips of micromouse when it's finding its way across the maze (using left follow rule):

https://user-images.githubusercontent.com/82906801/138678394-f690bd37-aa28-47af-905f-3e6478ae43f2.mp4

https://user-images.githubusercontent.com/82906801/138678441-d94f2ec3-b20e-4921-a819-7660af13ce92.mp4

https://user-images.githubusercontent.com/82906801/138678506-2ebe6455-c000-4e4e-961d-40abc93d84a7.mp4

https://user-images.githubusercontent.com/82906801/138678521-1ee71b9e-d742-4c2d-87e6-ca389d971233.mp4

https://user-images.githubusercontent.com/82906801/138678528-f9bc81cb-02b8-40a2-8544-f401436a2008.mp4


## Future Work
- [ ] Write a code for PID to make sure the bot remains a the centre of the path
- [ ] Implement other algorithms
- [ ] Work on making it remember the correct turns to be taken at every junction/node so that one final run can be made out of the 7 allowed in which it travels to the centre with the shortest possible path, by storing a text in text file.
- [ ] Replace delay everywhere with other conditions
- [ ] Make a final.launch such that all the necessary ROS nodes, RViz and Gazebo Simulation to solve the maze can be launched at once. 
- [ ] Learn about gzmaze so that a maze of any desired structure can be generated
- [ ] Make it cut through zigzag turns and take non-90 degree turns so as to decrease the time taken for the final run
- [ ] Help the bot detect dead ends from afar

## Contributors
* [Kalyani Kasar](https://github.com/KalyaniKasar1)

## Acknowledgements and Resources
* [SRA Vjti](https://www.sravjti.in/) Eklavya 2021<br/>
* Special thanks to my mentors [Gautam Agrawal](https://github.com/gautam-dev-maker), [Anushree Sabnis](https://github.com/MOLOCH-dev) and [Prathamesh Tagore](https://github.com/meshtag).<br/>
* https://github.com/hashmis79/Micromouse

## License
The [license](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/LICENSE) used for this project.
