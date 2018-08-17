#!/usr/bin/env python

import spade
from spade.bdi import *
from spade.Agent import *
from spade.DF import Service

def s1_method(Value):
    return {"O1":1}

def s2_method(Myoutput1):
    return {"O2":2}

def goalCompletedCB(goal):
    agent.goalCompleted = True

agent = BDIAgent("bdi@127.0.0.1","secret")
s1 = Service(name="s1", owner=agent.getAID(), inputs=["Value"],outputs=["O1"],P=["Var(Value,0,Int)"],Q=["Var(O1,1,Int)"])
s2 = Service(name="s2", owner=agent.getAID(), inputs=["O1"],outputs=["O2"],P=["Var(O1,1,Int)"],Q=["Var(O2,2,Int)"])

agent.registerService(s1,s1_method)
agent.registerService(s2,s2_method)

agent.goalCompleted = False

agent.saveFact("Value",0)

agent.setGoalCompletedCB( goalCompletedCB )

agent.addGoal( Goal("Var(O1,1,Int)") )

agent.start()

import time
counter = 0
while not agent.goalCompleted and counter < 10:
    time.sleep(1)
    counter+=1

goal = agent.goalCompleted
print goal

bel = agent.askBelieve( "Var(O1,1,Int)" )
print bel

agent.getFact("O1")


agent.stop()
sys.exit(0)