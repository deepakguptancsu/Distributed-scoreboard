#!/usr/bin/python

import kazoo
import pickle
from kazoo.client import KazooClient
import atexit, time
from sets import Set
import random
import operator
import sys

import logging
logging.basicConfig()

class watcher:
    def __init__(self, hostName, displayListSize):
        self.host = hostName
        self.maxDisplaySize = displayListSize
        self.zk = KazooClient(hosts = self.host)
        self.zk.start()
        self.zk.DataWatch("/gameData/recentScores", self.displayScores)
        self.zk.DataWatch("/gameData/activeUsers", self.displayScores)
        atexit.register(self.cleanup)

    def displayScores(self, var1, var2):
        self.displayRecentScores()
        self.displayHighestScores()
    
    def activeUserList(self):
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/activeUsers"):
            self.zk.create(path="/gameData/activeUsers", value=pickle.dumps([]))
        activeUsersZkObj, _ = self.zk.get(path="/gameData/activeUsers")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        return activeUsersObj

    def displayRecentScores(self):
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/recentScores"):
            self.zk.create(path="/gameData/recentScores", value=pickle.dumps([]))
        activeUsersZkObj, _ = self.zk.get(path="/gameData/recentScores")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        print "\nMost recent scores"
        print "------------------"
        activeUsersList = self.activeUserList()
        if len(activeUsersObj) > self.maxDisplaySize:
            activeUsersObj = activeUsersObj[len(activeUsersObj)-self.maxDisplaySize:len(activeUsersObj)]
        for recentScore in activeUsersObj:
            outputStr = "%s \t\t %d" % (recentScore[0], recentScore[1])
            if recentScore[0] in activeUsersList:
                outputStr += " **"
            print outputStr

    def displayHighestScores(self):
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/maxScores"):
            self.zk.create(path="/gameData/maxScores", value=pickle.dumps([]))
        activeUsersZkObj, _ = self.zk.get(path="/gameData/maxScores")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        print "\nHighest scores"
        print "------------------"
        activeUsersList = self.activeUserList()
        if len(activeUsersObj) > self.maxDisplaySize:
            activeUsersObj = activeUsersObj[0:self.maxDisplaySize]
        for highestScore in activeUsersObj:
            outputStr = "%s \t %d" % (highestScore[0], highestScore[1])
            if highestScore[0] in activeUsersList:
                outputStr += " **"
            print outputStr

    def cleanup(self):
        self.zk.stop()

if len(sys.argv) != 3:
    print "Please enter appropriate number of command line arguments"
    print "usage is: python watcher.py <serverIpAddress:port> <listSize>"
    exit()

try:
    if int(sys.argv[2]) > 25:
        print "display list size cannot be greater than 25"
        exit()
except ValueError:
    print "Please enter a valid integer number"
    exit()

if int(sys.argv[2]) < 1:
    print "Please enter listSize value greater than 0"
    exit()

watcherObj = watcher(sys.argv[1], int(sys.argv[2]))
while True:
    pass
