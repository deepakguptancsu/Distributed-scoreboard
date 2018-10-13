#!/bin/bash
echo "****** Setting up Environment "
echo "###### Updating apt-get #############"
sudo apt-get update
echo "###### Updating Done #########################"
echo "###### Installing python2.7 #############"
sudo apt-get -f install
sudo apt-get install python2.7
echo "###### python2.7 Installation Done #########################"
echo "###### Installing pip #############"
sudo apt-get install python-pip
echo "###### pip Installation Done #########################"
echo "###### Installing kazoo #############"
sudo python -m pip install kazoo
echo "###### Kazoo Installation Done #########################"
echo "###### Copying binaries #############"
sudo cp -pf watcher.py /usr/bin/watcher
sudo cp -pf player.py /usr/bin/player
echo "###### Done #########################"
echo "***** ALL DONE ! *************"
#alias player='python2.7 player.py'
#alias watcher='python2.7 watcher.py'
