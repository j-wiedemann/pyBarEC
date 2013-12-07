#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
#from fakeclassRdm import fakeRdm
import classRdm
import function
from xml.dom import minidom

string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="3,inf,inf,5000.0"/>
		<node d="1,0" id="N2"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
	</elem>
	<elem id="geo">
		<barre h="" id="*" igz="1.0" s="1e-06" v=""/>
	</elem>
	<elem id="material">
		<barre id="*" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<node d="0.0,-1000.0,0.0" id="N2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1.0" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="1e-06" id="S"/>
	</elem>
</data>"""

string2="""<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="1"/>
		<node d="@N1,1,0" id="N2" rz="1000" liaison="2"/>
		<node d="@N2,1,0" id="N3" liaison="2"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
	</elem>
	<elem id="geo">
		<barre h="0.08" id="*" igz="1.0" profil="IPE 80" s="1.0" v="0.04"/>
	</elem>
	<elem id="material">
		<barre id="*" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<node d="0.0,-1000.0,0.0" id="N2"/>
			<barre fp="0.25,0.0,-200.0,0.0" id="B1"/>
		</case>
		<case id="cas 2">
			<barre fp="0.2,0.0,-300.0,0.0" id="B1"/>
			<barre fp="0.3,0.0,-5000.0,0.0" id="B2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="2.0,2.0" id="combi1"/>
		<combinaison d="1.0,2.0" id="combi2"/>
		<combinaison d="1.0,0.0" id="combi3"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1000.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""


def fakeReadXMLFile(string):
    """Fonction de test
    Lecture des données dans une chaines de caractères"""
    return minidom.parseString(string)

def test():
  xml = fakeReadXMLFile(string2)
  rdm = classRdm.Structure(xml)
  #rdm = classRdm.StructureFile("exemples/charpente.dat")
  Rrdm = classRdm.R_Structure(rdm)



  #rdm.SolveOneCombi()
  Rrdm.BGCalculate()
  #print "Reac in test() = ", Rrdm.Chars['cas 2'].Reactions
  print "Maxi", Rrdm.SearchCasesMax()
  print Rrdm._SearchCombiVMax('combi1')
  #print "fp", Rrdm.GetCombiChar('combi1')

def test_GetCombiChar():
  print "Test de la fonction GetCombiChar"
  xml = fakeReadXMLFile(string2)
  rdm = classRdm.Structure(xml)
  #rdm = classRdm.StructureFile("exemples/charpente.dat")
  Rrdm = classRdm.R_Structure(rdm)
  Rrdm.SolveAllCases()
  Rrdm.Chars['cas 1'].diCharBarreFp = {u'B1': {0.4: [0.0, -1000.0, 0.0]}, u'B2': {0.6: [0.0, -1000.0, 0.0]}}
  Rrdm.Chars['cas 2'].diCharBarreFp = {u'B1': {0.4: [0.0, -1000.0, 0.0], 0.6: [0.0, -1000.0, 0.0]}, u'B2': {0.6: [0.0, -1000.0, 0.0]}}
  Rrdm.Chars['cas 1'].diCharBarreQu = {u'B1': {0.4: [0.0, -1000.0], 0.6: [0.0, -1000.0]}, u'B2': {0.6: [0.0, -1000.0]}}
  Rrdm.Chars['cas 2'].diCharBarreQu = {u'B1': {0.4: [0.0, -1000.0], 0.6: [0.0, -1000.0]}, u'B2': {0.6: [0.0, -1000.0]}}
  Rrdm.Chars['cas 1'].diCharTri = {u'B1': {0.4: [0.0, -1000.0], 0.6: [0.0, -1000.0]}, u'B2': {0.6: [0.0, -1000.0]}}
  Rrdm.Chars['cas 2'].diCharTri = {u'B1': {0.4: [0.0, -1000.0], 0.6: [0.0, -1000.0]}, u'B2': {0.6: [0.0, -1000.0]}}
  Rrdm.Chars['cas 1'].diCharTherm = {u'B1': [10, -10], u'B2': [0.0, -100.0]}
  Rrdm.Chars['cas 2'].diCharTherm = {u'B1': [0, 0], u'B2': [0.0, -100.0]}
  charFp, charQu, charTri, charTherm = Rrdm.GetCombiChar('combi1')
  assert charFp['B1'][0.6] == [0, -2000, 0]
  assert charFp['B1'][0.4] == [0, -4000, 0]
  assert charQu['B1'][0.4] == [0, -4000]
  assert charTri['B1'][0.4] == [0, -4000]



test()
#test_GetCombiChar() revoir
