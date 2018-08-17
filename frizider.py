#!/usr/bin/env python

import spade
from spade.bdi import *
from spade.Agent import *
from spade.DF import *
from spade.Behaviour import *
from spade.AID import *
from time import sleep

class Frizider( BDIAgent ):
    class naruci( Service ):
        inputs = {}
        outputs = {}
        def run( self ):
            print 'Narucujem: ', self.Q.args[ 0 ]
            self.myAgent.removeBelieve( self.P )
            self.addBelieve( self.Q )

    class reakcija( EventBehaviour ):
        def _process( self ):
            self.msg = None
            self.msg = self._receive( True, 10 )
            if self.msg:
                text = self.msg.content
                for i in text.split( ',' ):
                    b = expr( 'Sadrzim( %s, x )' % i.upper() ) 
                    kol = self.myAgent.askBelieve( b )[ expr( 'x' ) ].op
                    b = expr( 'Sadrzim( %s, %d )' % ( i.upper(), kol ) )
                    self.myAgent.removeBelieve( b )
                    b = expr( 'Sadrzim( %s, %d )' % ( i.upper(), kol - 1 ) ) 
                    self.myAgent.addBelieve( b )
                    if kol - 1 == 0:
                        self.myAgent.planirajNabavu()

    class status( Behaviour ):
        def _process( self ):
            self.myAgent.selectIntentions()
            print 'Trenutni sadrzaj: '
            for i in self.myAgent.kb.ask_generator( expr( 'Sadrzim( x, k )' ) ):
                print i[ expr( 'x' ) ], i[ expr( 'k' ) ]
            sleep( 3 )

    def _setup( self ):
        template = ACLTemplate()
        template.setOntology( "frizider" )
        t = MessageTemplate( template )
        
        self.addBehaviour( self.reakcija(), t )
        self.addBehaviour( self.status() )
        self.sadrzaj = { 'MESO':1, 'MLIJEKO':2, 'JOGURT':3, 'MASLAC':1, 'PARADAJZ':5 }
        for sastojak, kolicina in self.sadrzaj.items():
            self.addBelieve( expr( 'Sadrzim( %s, 0 )' % ( sastojak ) ) )
        self.planirajNabavu()

    def planirajNabavu( self ):
        self.plans = []
        self.goals = []
        for sastojak, kolicina in self.sadrzaj.items():
            plan = Plan( P=expr( 'Sadrzim( %s, 0 )' % sastojak ), Q=expr( 'Sadrzim( %s, %d )' % ( sastojak, kolicina ) ) )
            s = self.naruci( P=expr( 'Sadrzim( %s, 0 )' % sastojak ), Q=expr( 'Sadrzim( %s, %d )' % ( sastojak, kolicina ) ) )
            plan.appendService( s )
            self.addPlan( plan )
            g = Goal( expr( 'Sadrzim( %s, %d )' % ( sastojak, kolicina ) ) )
            self.addGoal( g )
        

if __name__ == '__main__':
    f = Frizider( "frizider@127.0.0.1", "tajna" )
    f.start()