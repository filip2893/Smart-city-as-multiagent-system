#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spade
from spade.bdi import *
from spade.Agent import *
from spade.DF import *
from spade.Behaviour import *
from spade.AID import *
from spade.ACLMessage import ACLMessage
from time import sleep

class AgentTramvaj(Agent):
	class PocetnoStajaliste(OneShotBehaviour):
		def _process( self ):
			print self.myAgent.stajaliste._actualState
			sleep( 1 )
			self.myAgent.brojac = self.myAgent.brojac + 1
			if self.myAgent.kraj == True:
				self._exitcode = self.myAgent.PRIJELAZ_U_ZAVRSNO
			elif self.myAgent.brojac < 5:
				self._exitcode = self.myAgent.PRIJELAZ_PRETPOSTAVLJENI
			elif self.myAgent.kraj == False:
				self.myAgent.brojac = 0
				self.myAgent.povratak = 0
				self._exitcode = self.myAgent.PRIJELAZ_POCETNO_U_DRUGO
				

	class DrugoStajaliste(OneShotBehaviour):
		def _process(self):
			print "" + self.myAgent.stajaliste._actualState
			sleep( 1 )
			self.myAgent.brojac = self.myAgent.brojac + 1
			if self.myAgent.kraj == True:
				self._exitcode = self.myAgent.PRIJELAZ_U_ZAVRSNO
			elif self.myAgent.brojac < 5:
				self._exitcode = self.myAgent.PRIJELAZ_PRETPOSTAVLJENI			
			elif self.myAgent.povratak == 0:
				self.myAgent.brojac = 0				
				self._exitcode = self.myAgent.PRIJELAZ_DRUGO_U_TRECE
			elif self.myAgent.povratak == 1:
				self.myAgent.brojac = 0
				self._exitcode = self.myAgent.PRIJELAZ_DRUGO_U_POCETNO

	class TreceStajaliste(OneShotBehaviour):
		def _process(self):
			print self.myAgent.stajaliste._actualState
			sleep( 1 )	
			self.myAgent.brojac = self.myAgent.brojac + 1
			if self.myAgent.kraj == True:
				self._exitcode = self.myAgent.PRIJELAZ_U_ZAVRSNO
			elif self.myAgent.brojac < 5:
				self._exitcode = self.myAgent.PRIJELAZ_PRETPOSTAVLJENI		
			elif self.myAgent.povratak == 0:
				self.myAgent.brojac = 0				
				self._exitcode = self.myAgent.PRIJELAZ_TRECE_U_CETVRTO
			elif self.myAgent.povratak == 1:
				self.myAgent.brojac = 0
				self._exitcode = self.myAgent.PRIJELAZ_TRECE_U_DRUGO

	class CetvrtoStajaliste(OneShotBehaviour):
		def _process(self):
			print self.myAgent.stajaliste._actualState
			sleep( 1 )		
			self.myAgent.brojac = self.myAgent.brojac + 1
			if self.myAgent.kraj == True:
				self._exitcode = self.myAgent.PRIJELAZ_U_ZAVRSNO
			elif self.myAgent.brojac < 5:
				self._exitcode = self.myAgent.PRIJELAZ_PRETPOSTAVLJENI	
			elif self.myAgent.povratak == 0:
				self.myAgent.brojac = 0				
				self._exitcode = self.myAgent.PRIJELAZ_CETVRTO_U_PETO
			elif self.myAgent.povratak == 1:
				self.myAgent.brojac = 0
				self._exitcode = self.myAgent.PRIJELAZ_CETVRTO_U_TRECE


	class PetoStajaliste(OneShotBehaviour):
		def _process(self):
			print self.myAgent.stajaliste._actualState
			sleep( 1 )	
			self.myAgent.brojac = self.myAgent.brojac + 1
			if self.myAgent.kraj == True:
				self._exitcode = self.myAgent.PRIJELAZ_U_ZAVRSNO
			elif self.myAgent.brojac < 5:
				self._exitcode = self.myAgent.PRIJELAZ_PRETPOSTAVLJENI	
			elif self.myAgent.povratak == 0:
				self.myAgent.brojac = 0		
				self.myAgent.povratak = 1
				self._exitcode = self.myAgent.PRIJELAZ_PETO_U_CETVRTO

	class ZavrsnoStajaliste(OneShotBehaviour):
		def _process(self):
			print 'kraj'
			self.myAgent._kill()

	class porukeInfoPult(EventBehaviour):		
		def _process(self):
			self.msg = None
			self.msg = self._receive(True)
			if self.msg:
				if self.msg.content == 'N':
					self.myAgent.kraj = True
				else:
					primatelj = AID.aid(name="infopult@127.0.0.1", addresses=["xmpp://infopult@127.0.0.1"])				
					sadrzaj = '%s,%s'% ( self.myAgent.stajaliste._actualState, self.myAgent.povratak )					
					self.msg = ACLMessage()
					self.msg.setPerformative('inform')
					self.msg.setOntology('tramvaj')				
					self.msg.setContent(sadrzaj)
					self.msg.addReceiver(primatelj)
					self.myAgent.send(self.msg)
			else:
				print "poruka nije dobivena"
			

	def _setup(self):
		self.brojac = 0
		self.povratak = 0
		self.kraj = False

		self.POCETNO_STAJALISTE = 'c1'
		self.DRUGO_STAJALISTE = 'c2'
		self.TRECE_STAJALISTE = 'c3'
		self.CETVRTO_STAJALISTE = 'c4'
		self.PETO_STAJALISTE = 'c5'
		self.ZAVRSNO_STAJALISTE = 7

		self.PRIJELAZ_PRETPOSTAVLJENI = 0
		self.PRIJELAZ_POCETNO_U_DRUGO = 10
		self.PRIJELAZ_DRUGO_U_TRECE = 20
		self.PRIJELAZ_TRECE_U_CETVRTO = 30
		self.PRIJELAZ_CETVRTO_U_PETO = 40
		self.PRIJELAZ_PETO_U_CETVRTO = 50
		self.PRIJELAZ_CETVRTO_U_TRECE = 60
		self.PRIJELAZ_TRECE_U_DRUGO = 70
		self.PRIJELAZ_DRUGO_U_POCETNO = 80

		self.PRIJELAZ_U_ZAVRSNO = 90

		p = spade.Behaviour.FSMBehaviour()

		p.registerFirstState( self.PocetnoStajaliste(), self.POCETNO_STAJALISTE )
		p.registerState( self.DrugoStajaliste(), self.DRUGO_STAJALISTE )
		p.registerState( self.TreceStajaliste(), self.TRECE_STAJALISTE )
		p.registerState( self.CetvrtoStajaliste(), self.CETVRTO_STAJALISTE )
		p.registerState( self.PetoStajaliste(), self.PETO_STAJALISTE )
		p.registerLastState( self.ZavrsnoStajaliste(), self.ZAVRSNO_STAJALISTE )

		p.registerTransition( self.POCETNO_STAJALISTE, self.DRUGO_STAJALISTE, self.PRIJELAZ_POCETNO_U_DRUGO )			
		p.registerTransition( self.DRUGO_STAJALISTE, self.TRECE_STAJALISTE, self.PRIJELAZ_DRUGO_U_TRECE )			
		p.registerTransition( self.TRECE_STAJALISTE, self.CETVRTO_STAJALISTE, self.PRIJELAZ_TRECE_U_CETVRTO )			
		p.registerTransition( self.CETVRTO_STAJALISTE, self.PETO_STAJALISTE, self.PRIJELAZ_CETVRTO_U_PETO )			
		
		p.registerTransition( self.PETO_STAJALISTE, self.CETVRTO_STAJALISTE, self.PRIJELAZ_PETO_U_CETVRTO )			
		p.registerTransition( self.CETVRTO_STAJALISTE, self.TRECE_STAJALISTE, self.PRIJELAZ_CETVRTO_U_TRECE )			
		p.registerTransition( self.TRECE_STAJALISTE, self.DRUGO_STAJALISTE, self.PRIJELAZ_TRECE_U_DRUGO )			
		p.registerTransition( self.DRUGO_STAJALISTE, self.POCETNO_STAJALISTE, self.PRIJELAZ_DRUGO_U_POCETNO )

		p.registerTransition( self.POCETNO_STAJALISTE, self.POCETNO_STAJALISTE, self.PRIJELAZ_PRETPOSTAVLJENI )			
		p.registerTransition( self.DRUGO_STAJALISTE, self.DRUGO_STAJALISTE, self.PRIJELAZ_PRETPOSTAVLJENI )
		p.registerTransition( self.TRECE_STAJALISTE, self.TRECE_STAJALISTE, self.PRIJELAZ_PRETPOSTAVLJENI )
		p.registerTransition( self.CETVRTO_STAJALISTE, self.CETVRTO_STAJALISTE, self.PRIJELAZ_PRETPOSTAVLJENI )
		p.registerTransition( self.PETO_STAJALISTE, self.PETO_STAJALISTE, self.PRIJELAZ_PRETPOSTAVLJENI )

		p.registerTransition( self.POCETNO_STAJALISTE, self.ZAVRSNO_STAJALISTE, self.PRIJELAZ_U_ZAVRSNO )
		p.registerTransition( self.DRUGO_STAJALISTE, self.ZAVRSNO_STAJALISTE, self.PRIJELAZ_U_ZAVRSNO )
		p.registerTransition( self.TRECE_STAJALISTE, self.ZAVRSNO_STAJALISTE, self.PRIJELAZ_U_ZAVRSNO )
		p.registerTransition( self.CETVRTO_STAJALISTE, self.ZAVRSNO_STAJALISTE, self.PRIJELAZ_U_ZAVRSNO )
		p.registerTransition( self.PETO_STAJALISTE, self.ZAVRSNO_STAJALISTE, self.PRIJELAZ_U_ZAVRSNO )			
		
		self.addBehaviour(p, None)
		self.stajaliste = p			

		template = ACLTemplate()
		template.setOntology('infopult')
		ipt = MessageTemplate(template)

		p3 = self.porukeInfoPult()
		self.addBehaviour(p3, ipt)




if __name__ == '__main__':
	agent = AgentTramvaj( "tramvaj@127.0.0.1", "tajna" )
	#agent.setDebugToScreen()
	agent.start()
	#agent._kill()