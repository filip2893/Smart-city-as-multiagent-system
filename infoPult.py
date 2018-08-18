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
from datetime import datetime, timedelta
import operator
import sys

ops = {"+": operator.add,
	   "-": operator.sub}

class infoPult( BDIAgent ):
	class glavno(Behaviour):			
		def _process(self):	
			print '\nIZBORNIK'
			print '--------'
			print 'nesreca tramvaj[N/n]'
			print 'karta[0]'
			print 'dogadjaji[1]'
			print 'put do lokacije[2]'
			print '------------------'
			self.izbor = raw_input("\nVas odabir: ")

			if self.izbor == 'N' or self.izbor == 'n':
				self.myAgent.nesreca = True
				primatelj = AID.aid(name="tramvaj@127.0.0.1", addresses=["xmpp://tramvaj@127.0.0.1"])					
				sadrzaj = 'N'					
				self.msg = ACLMessage()
				self.msg.setPerformative('inform')
				self.msg.setOntology('infopult')				
				self.msg.setContent(sadrzaj)
				self.msg.addReceiver(primatelj)
				self.myAgent.send(self.msg)		
 
			elif self.izbor == '0':
				self.myAgent.ucitajDatoteku("karta.txt")
				print "\nVAŠA LOKACIJA: %s"%( self.myAgent.infoPultLokacija )

			elif self.izbor == '1':
				self.myAgent.ucitajDatoteku("dogadjaji.txt")

			elif self.izbor == '2':				
				ispravno = False
				lokacija = None
				while ispravno == False:
					pass
					lokacija = raw_input("\nZeljena lokacija: ")		
					loc = 'lokacija(%s)' % (lokacija)		
					ispravno = self.myAgent.askBelieve(loc)
					if ispravno == False:
						print 'DOZVOLJENI UNOS (a-e)(1-5)'

				primatelj = AID.aid(name="tramvaj@127.0.0.1", addresses=["xmpp://tramvaj@127.0.0.1"])
					
				sadrzaj = 'daj_lokaciju_tramvaja'
					
				self.msg = ACLMessage()
				self.msg.setPerformative('inform')
				self.msg.setOntology('infopult')				
				self.msg.setContent(sadrzaj)
				self.msg.addReceiver(primatelj)
				self.myAgent.send(self.msg)

				self.myAgent.lokacija = lokacija
					#loc = 'zeljena_lokacija( %s )' % (self.myAgent.lokacija)
					#self.myAgent.addBelieve(loc)			

				uTramvaju = abs(int(self.myAgent.infoPultLokacija[1]) - int(self.myAgent.lokacija[1]))

				self.pjesiceUkupnoTrajanje = self.myAgent.putDoLokacije( self.myAgent.infoPultLokacija, self.myAgent.lokacija )
				self.dolazak = datetime.now() + timedelta( minutes = self.pjesiceUkupnoTrajanje )	

				print '\nUPUTE DO LOKACIJE: %s <PJESICE>'% ( self.myAgent.lokacija )
				print '-------------------------------'
				print 'Do dogadjaja je pjesice jos: [%s min]'% (self.pjesiceUkupnoTrajanje)	
				print 'DOLAZAK: %s:%s '% (self.dolazak.hour, self.dolazak.minute)
				
				if uTramvaju > 0 and self.myAgent.nesreca == False:
					self.odTramvaj = 'c' + self.myAgent.infoPultLokacija[1]			
					self.doTramvaj = 'c' + self.myAgent.lokacija[1]
					self.polazakTramvaja = self.myAgent.vrijemeDolaskaTramvaja( self.odTramvaj,
																self.myAgent.stajaliste, 
																self.myAgent.relacija )

					self.uTramvaju = self.myAgent.vrijemeDolaskaTramvaja( self.doTramvaj,
																self.odTramvaj, 
																self.myAgent.relacija )
							
					self.pjesiceTramvaj = 1
					self.tramvajPjesice = 1

					if self.odTramvaj != self.myAgent.infoPultLokacija:
						self.pjesiceTramvaj = self.myAgent.putDoLokacije( self.myAgent.infoPultLokacija, self.odTramvaj )

					if self.uTramvaju > 4:
						self.polazakTramvaja += (self.uTramvaju - 4)
						self.uTramvaju -=  4	

					self._polazakTramvaja = self.polazakTramvaja

					while self.polazakTramvaja < self.pjesiceTramvaj:
						self.polazakTramvaja += self._polazakTramvaja

					if self.doTramvaj != self.myAgent.lokacija:
						self.tramvajPjesice = self.myAgent.putDoLokacije( self.doTramvaj, self.myAgent.lokacija )			

					self.tramvajUkupnoTrajanje = self.polazakTramvaja + self.uTramvaju + self.tramvajPjesice
					
					self._polazakTramvaja = datetime.now() + timedelta( minutes = self.polazakTramvaja )
					self.dolazak = datetime.now() + timedelta( minutes = self.tramvajUkupnoTrajanje )

					print '\nUPUTE DO LOKACIJE: %s <TRAMVAJ>'% (self.myAgent.lokacija)
					print '-------------------------------'
					print '#TRENUTNO stajaliste tramvaja: %s'% (self.myAgent.stajaliste)
					print 'NAJBLIZE stajaliste tramvaja: %s [%s min]'% (self.odTramvaj, self.pjesiceTramvaj)
					print 'Izlaz iz tramvaja: %s'% (self.doTramvaj)
					print 'Dolazak tramvaja u: %s:%s za[%s min]'% (self._polazakTramvaja.hour, self._polazakTramvaja.minute, self.polazakTramvaja)
					print 'Putovanje tramvajem: [%s min]'% (self.uTramvaju)
					print 'Do dogadjaja je pjesice jos: [%s min]'% (self.tramvajPjesice)	
					print 'Ukupno trajanje putovanja: [%s min]'%(self.tramvajUkupnoTrajanje)
					print 'DOLAZAK NA ZELJENU LOKACIJU: %s:%s '% (self.dolazak.hour, self.dolazak.minute)

			else: print 'KRIVI UNOS\n'
	
	class porukeDogadjaja(EventBehaviour):		
		def _process(self):
			self.msg = None
			self.msg = self._receive(True)
			if self.msg:
				with open("dogadjaji.txt", "a") as dogadjaji:
					dogadjaji.write( self.msg.content )
			else:
				print "poruka nije dobivena"

	class porukeTramvaj(EventBehaviour):		
		def _process(self):
			self.msg = None
			self.msg = self._receive(True)
			if self.msg:
				lista = self.msg.content.split( ',' )
				self.myAgent.stajaliste = lista[ 0 ]
				self.myAgent.relacija = lista[ 1 ]
				#print self.myAgent.stajaliste
				#print self.myAgent.relacija
			else:
				print "poruka nije dobivena"
			
	def _setup( self ):
		self.nesreca = False

		loc = 'osoba_lokacija( %s )' % (self.infoPultLokacija)
		self.addBelieve(loc)

		p1 = self.glavno() 
		self.addBehaviour(p1,None)		

		self.configureKB("SWI", None, "/usr/bin/swipl")		
		self.znanje = self.ucitajZnanje('lokacija.pl')
		for z in self.znanje:
			#print z
			self.addBelieve( z )
		#bel = self.askBelieve( 'tramvaj_relacija(a1,d4)' )
		#print bel

		template = ACLTemplate()
		template.setOntology('dogadjaj')
		dt = MessageTemplate(template)		

		p2 = self.porukeDogadjaja() 
		self.addBehaviour(p2,dt)

		template = ACLTemplate()
		template.setOntology('tramvaj')
		tt = MessageTemplate(template)

		p3 = self.porukeTramvaj()		
		self.addBehaviour(p3,tt)		

	def ucitajZnanje(self,datoteka):
		znanje = []
		with open(datoteka, 'r') as f:
			for red in f:
				red = red.strip()				
				znanje.append(red[:-1])
		return znanje

	def ucitajDatoteku( self,datoteka ):
		if datoteka == "dogadjaji.txt":
			print "\n------------"
			print "|DOGADJAJI:|"
			print "------------"
		elif datoteka == "karta.txt":
			print "\n#############"
			print "KARTA GRADA:#"
			print "#############"

		brojac = 0

		with open( datoteka, 'r') as f:
				for red in f:
					brojac += 1
					red = red.strip()				
					print red
					if brojac == 6:
						print "---------------"
						brojac = 0

	def vrijemeDolaskaTramvaja(self, stajaliste, dolazak, relacija):		
		op_index = ops["+"]
		if relacija == 1:
			op_index = ops["-"]

		trajanje = 0

		while stajaliste != dolazak:			
			index = op_index( int( dolazak[1]), 1 ) 
			dolazak = dolazak[0] + str(index)
			#print dolazak
			trajanje += 1
			if index == 5:
				op_index = ops["-"]
			elif index == 1:
				op_index = ops["+"]
		return trajanje

	def putDoLokacije(self, od, do):
		uzduz = 10
		poprijeko = 15
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

		oznaka = abs(oznaka)
		index = abs(index)
		udaljenost1 = (oznaka + index) * uzduz

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
			sleep(1)
			udaljenost2 += poprijeko			

		oznaka = abs(int(ord(y[0]) - ord(do[0])))
		index = abs( int(y[1]) - int(do[1]) )
		udaljenost2 += (oznaka + index) * uzduz

		udaljenost = None

		if (udaljenost1 < udaljenost2) or (udaljenost2 == 0):
			udaljenost = udaljenost1
		else: udaljenost = udaljenost2
		return udaljenost	

if __name__ == '__main__':
	agent = infoPult( "infopult@127.0.0.1", "tajna" )
	agent.infoPultLokacija = sys.argv[ 1 ] 
	agent.start()