# __MICROMOUSE PROJECT__
A micromouse is a small sized, fast bot that can solve a 16x16 in a short period. 

## Table of Contents
* [About the Project](#about-the-project)
  * [Tech Stack](#tech-stack)
  * [File Structure](#file-structure)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Configuration](#configuration)
* [Usage](#usage)
* [Theory and Approach](#theory-and-approach)
* [Results and Demo](#results-and-demo)
* [Future Work](#future-work)
* [Troubleshooting](#troubleshooting)
* [Contributors](#contributors)
* [Acknowledgements and Resources](#acknowledgements-and-resources)
* [License](#license)

## About the project
![Screenshot from 2021-10-24 11-43-34.png](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/assets/Screenshot%20from%202021-10-24%2011-43-34.png)
![Screenshot from 2021-10-24 11-43-54.png](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/assets/Screenshot%20from%202021-10-24%2011-43-54.png)

##### AIM
To make the micromouse bot capable of reaching the centre of the given maze in the shortest possible time using maze solving algorithms. As of now, I have almost implemented the left follow algorithm on it. The right follow algorithm  is similar but the opposite. The micromouse bot also somewhat requires PID tuning to stay in the centre of the path. 

### Tech Stack
- [ROS Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu)
- [Gazebo 9](http://gazebosim.org/)
- [Python 3](https://www.python.org/downloads/)

### File Structure
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
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┗ 📜bot.cpython-38.pyc
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
 
## Getting Started

### Prerequisites
    1. ROS Noetic
    2. Gazebo Version: 9.0
    3. RViz (not compulsory)

* You can find the video demonstration link for installtion of ROS Noetic  [here](https://www.youtube.com/watch?v=ZA7u2XPmnlo) and the website link for the same [here](http://wiki.ros.org/noetic/Installation/Ubuntu).
* The link to install Gazebo for Ubuntu is provided [here](http://gazebosim.org/tutorials?tut=install_ubuntu). You can find the instructions to install different versions of Gazebo in the link provided above but using Gazebo 9.0 is recommeded for ROS Noetic.
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

## Results and Demo
Initial position of micromouse in the maze :
![Screenshot from 2021-10-24 11-44-06.png](https://github.com/KalyaniKasar1/Micromouse-Eklavya/blob/main/assets/Screenshot%20from%202021-10-24%2011-44-06.png)

Clips of micromouse when it's finding its way across the maze (using left follow rule):




https://user-images.githubusercontent.com/82902712/138563488-c9e4268a-3700-4b34-b2bd-1795de4a06f7.mp4






## Future Work
- [] Write a code for PID to make sure the bot remains a the centre of the path
- [] Implement other algorithms
- [] Work on making it remember the correct turns to be taken at every junction/node so that one final run can be made out of the 7 allowed in which it travels to the centre with the shortest possible path, by storing a text in text file.



## Contributors
* [Kalyani Kasar](https://github.com/KalyaniKasar1)

