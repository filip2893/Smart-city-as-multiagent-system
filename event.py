#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spade
from spade.bdi import *
from spade.Agent import *
from spade.DF import *
from spade.Behaviour import *
from spade.AID import *
from spade.ACLMessage import ACLMessage
from datetime import datetime, timedelta
from time import sleep

class Event( Agent ):
	class proba(OneShotBehaviour):	
		def _process(self):	
			#if self.myAgent.dogadjaj['kraj'] > datetime.now():
				
				primatelj = AID.aid(name="osoba@127.0.0.1", addresses=["xmpp://osoba@127.0.0.1"])
				
				sadrzaj = self.myAgent.dogadjaj['lokacija']
				
				self.msg = ACLMessage()
				self.msg.setPerformative('inform')
				self.msg.setOntology('dogadjaj')				
				self.msg.setContent(sadrzaj)
				self.msg.addReceiver(primatelj)
				self.myAgent.send(self.msg)

				#print "dobro došli"
			#else:
				#print "svemu je kraj"
			
	def _setup( self ):
		self.dogadjaj = {}
		self.dogadjaj = self.noviDogadjaj()

		lokacija = self.dogadjaj['lokacija']
		print lokacija[0]
		print ord('a')

		p = self.proba()
		self.addBehaviour(p, None)

	def noviDogadjaj(self):
		dogadjaj = {}
		#dogadjaj['naziv'] = raw_input("Naziv:")
		#dogadjaj['tip'] = raw_input("Vrsta:")
		#dogadjaj['pocetak'] = datetime.strptime(raw_input("Datum i vrijeme početka(d.m.y. h:m):"), '%d.%m.%Y. %H:%M')
		#dogadjaj['kraj'] = datetime.strptime(raw_input("Datum i vrijeme kraja(d.m.y. h:m):"), '%d.%m.%Y. %H:%M')
		#dogadjaj['cijena'] = raw_input("Cijena:")
		dogadjaj['lokacija'] = raw_input("Lokacija(a-f)(1-6):")	
		#dogadjaj['max'] = raw_input("Max broj ljudi:")		
		return dogadjaj

if __name__ == '__main__':
	agent = Event( "event@127.0.0.1", "tajna" )
	agent.start()
	#agent._kill()