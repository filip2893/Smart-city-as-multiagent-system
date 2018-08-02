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
import operator
"""
agent = BDIAgent("novi@127.0.0.1","tajna")
#agent.setDebugToScreen()
agent.configureKB("SWI", None, "/usr/bin/swipl")
agent.addBelieve( 'a(b,c)' )	
agent.addBelieve( 'a(c,d)' )
bel = agent.askBelieve( 'a(b,c)' )
print bel

def ucitajZnanje(datoteka):
	znanje = set()
	with open(datoteka, 'r') as f:
		for red in f:
			red = red.strip()
			znanje.add(red[:-1])
	return znanje

znanje = ucitajZnanje('proba.pl')
for z in znanje:
	print z
	agent.addBelieve( z )	 

#x = 'a(d)'
#agent.addBelieve( x )
bel = agent.askBelieve( 'p(X,Y)' )
print bel
agent.start()
agent._kill()
"""

ops = {"+": operator.add,
	   "-": operator.sub}

class Vjezba( BDIAgent ):		
	class usluga1(Service):
		inputs = {}
		outputs = {}
		def run(self):
			print "Pokrecem uslugu 1"
			self.addBelieve('a(c)')

	class usluga2(Service):
		inputs = {}
		outputs = {}
		def run(self):
			print "Pokrecem uslugu 2"
			self.addBelieve('a(d)')

	class odaberi(Behaviour):		
		def onStart(self):
			ispravno = False
			self.myAgent.lokacija = None
			while ispravno == False:
				pass
				self.myAgent.lokacija = raw_input("Vaša lokacija(a-e)(1-5):")		
				loc = 'lokacija(%s)' % (self.myAgent.lokacija)		
				ispravno = self.myAgent.askBelieve(loc)
				if ispravno == False:
					print 'NEISPRAVAN UNOS'

			loc = 'osoba_lokacija( %s )' % (self.myAgent.lokacija)
			self.myAgent.addBelieve(loc)

	class porukeDogadjaja(EventBehaviour):		
		def _process(self):
			self.msg = None
			self.msg = self._receive(True)
			self.dogadjaj = None
			#sleep(1)
			if self.msg:
				print self.msg.content
				#self.dogadjaj = self.msg.content
				#self.izracunajUdaljenost()
			else:
				print "poruka nije dobivena"

	class porukeTramvaj(EventBehaviour):		
		def _process(self):
			self.msg = None
			self.msg = self._receive(True)
			self.dogadjaj = None
			#sleep(1)
			if self.msg:
				print self.msg.content
				#self.dogadjaj = self.msg.content
				#self.izracunajUdaljenost()
			else:
				print "poruka nije dobivena"
			#trajanjeSlovo = ord(self.myAgent.lokacija[0] - self.myAgent.dogadjaj[0])
			#if self.myAgent.dogadjaj != None:
			#	print "trajanjeSlovo"
			
	def _setup( self ):
		p1 = self.odaberi() 
		self.addBehaviour(p1,None)		

		self.configureKB("SWI", None, "/usr/bin/swipl")		
		self.znanje = self.ucitajZnanje('lokacija.pl')
		for z in self.znanje:
			#print z
			self.addBelieve( z )
		bel = self.askBelieve( 'tramvaj_relacija(a1,d4)' )
		print bel

		template = ACLTemplate()
		template.setOntology('dogadjaj')
		dt = MessageTemplate(template)		

		p2 = self.porukeDogadjaja() 
		self.addBehaviour(p2,dt)

		template = ACLTemplate()
		template.setOntology('tramvaj')
		tt = MessageTemplate(template)

		p4 = self.porukeTramvaj()		
		self.addBehaviour(p4,tt)

		self.putDoLokacije('c3', 'd1')				

	def ucitajZnanje(self,datoteka):
		znanje = []
		with open(datoteka, 'r') as f:
			for red in f:
				red = red.strip()				
				znanje.append(red[:-1])
		return znanje

	def putDoLokacije(self, od, do):
		#x = od
		y = od
		op_oznaka = ops["-"]
		op_index = ops["-"]

		oznaka = op_oznaka( ord(od[0]), ord(do[0]) )		
		index = op_index( int(od[1]),int(do[1]) )	

		if(oznaka <= 0) and (index <= 0):#desno dolje
			op_oznaka = ops["+"]
			op_index = ops["+"]
		elif(oznaka > 0) and (index < 0):#lijevo dolje
			op_index = ops["+"]
		elif(oznaka < 0) and (index > 0):#desno gore
			op_oznaka = ops["+"]

		print op_oznaka(0,1)
		print op_index(0,1)	

		oznaka = abs(oznaka)
		index = abs(index)
		udaljenost1 = (oznaka + index) * 8
		print 'Udaljenost pješice: %s'% (udaljenost1)

		udaljenost2 = 0
		
		pom = int(y[1])

		while y[0] != do[0]:
			if y[1] == do[1]:
				break
			y = int(ord(y[0]))
			y = op_oznaka(y, 1)
			y = str(unichr(y))
			pom = op_index(pom, 1) 
			y = y + str(pom)
			print y
			sleep(1)
			udaljenost2 += 10			

		oznaka = abs(int(ord(y[0]) - ord(do[0])))
		index = abs( int(y[1]) - int(do[1]) )
		udaljenost2 += (oznaka + index) * 8

		udaljenost = None

		if (udaljenost1 < udaljenost2) or (udaljenost2 == 0):
			udaljenost = udaljenost1
		else: udaljenost = udaljenost2

		print 'Udaljenost pješice: %s'% (udaljenost) 
		 	 
		
		#while y[0] != 'c':
		#	y = int(ord(y[0]) + 1)
		#	y = str(unichr(y)) + '1'
		#	print '(x,y) = (' + x + ', ' + y + ')'
		#	#self.addBelieve()
		#	x = y		
		#	sleep(1)

	
"""
	def planiraj(self):
		self.plans = []
		self.goals = []
		s1 = Service(name="s1", owner=self.getAID(), inputs = {}, outputs = {}, P=expr('a(b)'), Q=expr('a(c)'))#self.usluga1(P=expr('a(b)'), Q=expr('a(c)'))
		self.registerService(s1)
		s2 = self.usluga2(P=expr('a(c)'), Q=expr('a(d)'))
		self.registerService(s1, self.usluga1)
		self.addPlan(P=expr('a(b)'), Q=expr('a(d)'), services=["s1","s2"])	 
		self.addGoal(Goal(expr('a(d)')))           
"""
	

if __name__ == '__main__':
	agent = Vjezba( "osoba@127.0.0.1", "tajna" )
	#agent.setDebugToScreen()
	agent.start()
	#agent._kill()