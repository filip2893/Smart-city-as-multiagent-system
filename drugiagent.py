#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spade
import time

class DrugiAgent( spade.Agent.Agent ):
    class Ponasanje( spade.Behaviour.Behaviour ):
        def onStart( self ):
            print "Pokrećem svoje ponašanje..."
            self.counter = 0

        def _process( self ):
            print "Brojač:", self.counter
            self.counter = self.counter + 1
            time.sleep( 1 )

    def _setup( self ):
        print "Drugi agent: krećem u akciju!"
        p = self.Ponasanje()
        self.addBehaviour( p, None )

if __name__ == "__main__":
    a = DrugiAgent( "drugiagent@127.0.0.1", "tajna")
    a.start()