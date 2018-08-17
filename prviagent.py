#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spade
from spade.bdi import *
from spade.Agent import *

agent = BDIAgent("novi@127.0.0.1","tajna")
#agent.setDebugToScreen()
agent.configureKB("SWI", None, "/usr/bin/swipl")
agent.addBelieve( 'a(b)' )	
agent.addBelieve( 'a(c)' )

bel = agent.askBelieve( 'a(b)' )
print bel

agent.start()
agent._kill()

