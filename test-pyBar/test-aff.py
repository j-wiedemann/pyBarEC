#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import math
import os
from numpy import *
from xml.dom import minidom
from classRdm import *
import function

def fakeReadXMLFile(string):
    """Fonction de test
    Lecture des données dans une chaines de caractères"""
    return minidom.parseString(string)

class fakeRdm(R_Structure) :
  """Programme de calcul RDM"""

  
  def __init__(self, string):
    # si on n'écrit pas ici explicitement le init de la classe parent, ce dernier n'est pas exécuté
    xml = fakeReadXMLFile(string)
    self.struct = Structure(xml)
    self.char_error = []

    self.Cases = self.GetCasCharge()
    self.CombiCoef = self.GetCombi()
    xmlnode = self.struct.XMLNodes["char"].getElementsByTagName('case')
    self.Chars = {}
    for cas in self.Cases:
      Char = CasCharge(cas, xmlnode, self.struct)
      self.Chars[cas] = Char
    self.BGCalculate()


def test():
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="1"/>
		<node d="1.,0" dep="0.01" id="N2" liaison="3,0,1000,0"/>
		<node d="2,0" id="N3" liaison="2"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,1" id="B1"/>
		<barre d="N2,N3" id="B2"/>
	</elem>
	<elem id="geo">
		<barre h="0.08" id="*" igz="1.0" profil="IPE 80" s="10.0" v="0.04"/>
	</elem>
	<elem id="material">
		<barre id="*" young="1.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<node d="0.0,-1.0,0.0" id="N2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi1"/>
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
  rdm = fakeRdm(string)
  print rdm.Chars['cas 1'].ddlValue


  #print "terminé", rdm.valid
test()
#cProfile.run('test()')
