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

class player:
    def __init__(self, hostAddr, playerName):
        self.host = hostAddr
        self.playerName = playerName
        self.maxDisplaySize = 5
        self.zk = KazooClient(hosts = self.host)
        self.userAlreadyExist = False
        self.zk.start()
        atexit.register(self.cleanup)

    def addPlayer(self):
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/activeUsers"):
            self.zk.create(path="/gameData/activeUsers", value=pickle.dumps([]))
        
        activeUsersZkObj, _ = self.zk.get(path="/gameData/activeUsers")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        
        for x in activeUsersObj:
            if x == self.playerName:
                self.userAlreadyExist = True
                print "user already exists. Exiting the program"
                exit()
        
        activeUsersObj = activeUsersObj + [self.playerName]
        self.zk.set(path="/gameData/activeUsers", value=pickle.dumps(activeUsersObj))

        #for debugging
        '''        
        activeUsersZkObj, _ = self.zk.get(path="/gameData/activeUsers")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        print activeUsersObj
        '''
        #end of debugging

    def deletePlayer(self):
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/activeUsers"):
            self.zk.create(path="/gameData/activeUsers", value=pickle.dumps([]))
        
        activeUsersZkObj, _ = self.zk.get(path="/gameData/activeUsers")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        activeUsersObj.remove(self.playerName)
        self.zk.set(path="/gameData/activeUsers", value=pickle.dumps(activeUsersObj))

        #for debugging
        '''
        activeUsersZkObj, _ = self.zk.get(path="/gameData/activeUsers")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        print activeUsersObj
        '''
        #end of debugging

    def pushScore(self, score):
        #adding score in recentScores list
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/recentScores"):
            self.zk.create(path="/gameData/recentScores", value=pickle.dumps([]))
        activeUsersZkObj, _ = self.zk.get(path="/gameData/recentScores")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        activeUsersObj.append([self.playerName, score])
        if len(activeUsersObj) > self.maxDisplaySize:
            activeUsersObj.pop(0)
        self.zk.set(path="/gameData/recentScores", value=pickle.dumps(activeUsersObj))

        #for debugging
        '''
        activeUsersZkObj, _ = self.zk.get(path="/gameData/recentScores")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        print activeUsersObj
        '''
        #end of debugging

        #adding score in maxScores list
        self.zk.ensure_path(path="/gameData")
        if not self.zk.exists(path="/gameData/maxScores"):
            self.zk.create(path="/gameData/maxScores", value=pickle.dumps([]))
        activeUsersZkObj, _ = self.zk.get(path="/gameData/maxScores")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        activeUsersObj.append([self.playerName, score])

        #sorting the list
        activeUsersObj = sorted(activeUsersObj, key=operator.itemgetter(1), reverse=True)

        #removing an item if list size exceeds than the threshold size
        if len(activeUsersObj) > self.maxDisplaySize:
            activeUsersObj.pop()
        self.zk.set(path="/gameData/maxScores", value=pickle.dumps(activeUsersObj))

        #for debugging
        '''
        activeUsersZkObj, _ = self.zk.get(path="/gameData/maxScores")
        activeUsersObj = pickle.loads(activeUsersZkObj)
        print activeUsersObj
        '''
        #end of debugging

    def cleanup(self):
        if not self.userAlreadyExist:
            self.deletePlayer()
        self.zk.stop()

if len(sys.argv) == 3:
    playerObj = player(sys.argv[1], sys.argv[2])
    playerObj.addPlayer()
    score = raw_input("Please enter the score\n")
    try:
        score = int(score)
    except ValueError:
        print "Please enter a valid integer number"
        exit()
    if score < 0:
        print "Please enter a non-negative integer number"
        exit()

    print "player %s adding score = %d" % (sys.argv[2],score)
    playerObj.pushScore(score)
elif len(sys.argv) == 6:
    hostAddr = sys.argv[1]
    playerName = sys.argv[2]
    try:
        count = int(sys.argv[3])
        u_delay = int(sys.argv[4])
        u_score = int(sys.argv[5])
    except ValueError:
        print "Please enter a valid integer number"
        exit()
    if count<0 or u_delay<0 or u_score<0:
        print "Please enter non-negative values"
        exit()
    playerObj = player(sys.argv[1], sys.argv[2])
    playerObj.addPlayer()
    for _ in xrange(0,count):
        score = int(random.normalvariate(mu=u_score, sigma=u_score/3))
        delay = int(random.normalvariate(mu=u_delay, sigma=u_delay/3))
        print "player %s adding score = %d" % (sys.argv[2],score)
        playerObj.pushScore(score)
        print "sleeping for %d seconds" % delay
        time.sleep(delay)
else:
    print "Please enter appropriate number of command line arguments"
    print "usage is: python player.py <serverIpAddress:port> <playerName>"
    print "OR: python player.py <serverIpAddress:port> <playerName> <count> <delay> <score>"
    exit()




