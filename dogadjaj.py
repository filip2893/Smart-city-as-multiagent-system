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

class Dogadjaj( BDIAgent ):
	class noviDogadjaj(Behaviour):	
		def _process(self):
			ispravno = False
			
			self.myAgent.dogadjaj = {}
			self.myAgent.dogadjaj['naziv'] = raw_input("Naziv:")
			self.myAgent.dogadjaj['tip'] = raw_input("Vrsta:")
			self.myAgent.dogadjaj['pocetak'] = datetime.strptime(raw_input("Datum i vrijeme početka(d.m.y. h:m):"), '%d.%m.%Y. %H:%M')
			self.myAgent.dogadjaj['kraj'] = datetime.strptime(raw_input("Datum i vrijeme kraja(d.m.y. h:m):"), '%d.%m.%Y. %H:%M')
			self.myAgent.dogadjaj['cijena'] = raw_input("Cijena:")
			while ispravno == False:
				self.myAgent.dogadjaj['lokacija'] = raw_input("Lokacija:")
				loc = 'lokacija(%s)' % ( self.myAgent.dogadjaj['lokacija'] )		
				ispravno = self.myAgent.askBelieve(loc)
				if ispravno == False:
					print 'DOZVOLJENI UNOS (a-e)(1-5)'

			if self.myAgent.dogadjaj['kraj'] > datetime.now():
				primatelj = AID.aid(name="infopult@127.0.0.1", addresses=["xmpp://infopult@127.0.0.1"])			
				
				sadrzaj = "naziv=%s"%(self.myAgent.dogadjaj['naziv'])
				sadrzaj += "\ntip=%s"%(self.myAgent.dogadjaj['tip'])
				sadrzaj += "\npocetak=%s"%(self.myAgent.dogadjaj['pocetak'])
				sadrzaj += "\nkraj=%s"%(self.myAgent.dogadjaj['kraj'])
				sadrzaj += "\ncijena=%s"%(self.myAgent.dogadjaj['cijena'])
				sadrzaj += "\nlokacija=%s\n"%(self.myAgent.dogadjaj['lokacija'])

				self.msg = ACLMessage()
				self.msg.setPerformative('inform')
				self.msg.setOntology('dogadjaj')				
				self.msg.setContent(sadrzaj)
				self.msg.addReceiver(primatelj)
				self.myAgent.send(self.msg)
				print "\nDogadjaj uspjesno dodan\n"
			
			else:
				print"\nDogadjaj je zavrsio\n"
			
	def _setup( self ):
		self.configureKB("SWI", None, "/usr/bin/swipl")		
		self.znanje = self.ucitajZnanje('lokacija.pl')
		for z in self.znanje:
			self.addBelieve( z )

		p = self.noviDogadjaj()
		self.addBehaviour(p, None)

	def ucitajZnanje(self,datoteka):
		znanje = []
		with open(datoteka, 'r') as f:
			for red in f:
				red = red.strip()				
				znanje.append(red[:-1])
		return znanje

if __name__ == '__main__':
	agent = Dogadjaj( "dogadjaj@127.0.0.1", "tajna" )
	agent.start()
	#agent._kill()