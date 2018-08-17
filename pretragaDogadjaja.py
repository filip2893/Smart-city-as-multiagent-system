#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spade

agent = spade.Agent.Agent("trazi@127.0.0.1","tajna")
agent.start()
s = spade.DF.ServiceDescription()
rezultat = agent.searchService( s )
for i in rezultat:
		print i
agent._kill()