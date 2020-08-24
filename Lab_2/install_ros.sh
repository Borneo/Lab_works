#!bin/bash

function instl_ros (){

sudo add-apt-repository restricted
sudo add-apt-repository universe
sudo add-apt-repository multiverse

sudo apt-get update

#Добавим репозиторий с нужными нам пакетами ros
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
#Добавим ключ для доступа
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
#Устанавливаем пакет мелодик
sudo apt install ros-melodic-desktop-full

#Добавляем в оболочку путь к директории ROS
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
#Сделаем команды ROS доступными выполнив source из .bashrc
source ~/.bashrc

#Установим необходимые пакеты
sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential

sudo apt install python-rosdep
sudo apt install python-roslaunch

#Инициализируем rosdep
sudo rosdep init
rosdep update

# building the core ROS packages
#Создадим рабочее постранство catkin workspace
mkdir ~/ros_catkin_ws
cd ~/ros_catkin_ws

rosinstall_generator desktop --rosdistro melodic --deps --tar > melodic-desktop.rosinstall
mkdir src
sudo apt-get install python3-vcstool
vcs import src < melodic-desktop.rosinstall

#Для получения всех зависимых пакетов
rosdep install --from-paths src --ignore-src --rosdistro melodic -y
#Сборка пакетов 
./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release

#Обновление рабочей среды
mv -i melodic-desktop-full.rosinstall melodic-desktop-full.rosinstall.old
rosinstall_generator desktop_full --rosdistro melodic --deps --tar > melodic-desktop-full.rosinstall
diff -u melodic-desktop-full.rosinstall melodic-desktop-full.rosinstall.old
vcs import src < melodic-desktop-full.rosinstall
#пересобираем рабочее окружение
./src/catkin/bin/catkin_make_isolated --install
source ~/ros_catkin_ws/install_isolated/setup.bash
} 

cd 
instl_ros
#запускаем ROS
roscore
