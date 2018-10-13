# Distributed-scoreboard

## Introduction
Many players can connect to any of the server in the zookeeper ensemble and post scores, while watcher displays the top scores posted and current online players. Current online players are * marked. Player can stop posting the scores and leave by executing Ctrl+c.
The project is implemented in Python using Kazoo on Zookeeper.

## For setting up environment - execute
make

## program can be started by using

player serverIpAddress:port playerName

            OR          

player serverIpAddress:port playerName count delay score

watcher serverIpAddress:port listSize
