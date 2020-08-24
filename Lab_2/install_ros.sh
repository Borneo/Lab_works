#!bin/bash

function instl_ros (){

sudo add-apt-repository restricted
sudo add-apt-repository universe
sudo add-apt-repository multiverse

sudo apt-get update

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt install ros-melodic-desktop-full

echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential

sudo apt install python-rosdep
sudo apt install python-roslaunch

#sudo apt --fix-broken install

sudo rosdep init
rosdep update

} 

cd 
instl_ros
