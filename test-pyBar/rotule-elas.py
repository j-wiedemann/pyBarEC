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
		<node d="0,0" id="N1" liaison="0"/>
		<node d="1,0" dep="-0.01" id="N2" liaison="2"/>
		<node d="2,0" dep="-0.01" id="N3" liaison="2"/>
		<node d="3,0" id="N4" liaison="2,45"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
		<barre d="N3,N4" id="B3"/>
		<rot_elast rz="0" node="N2" id="B1"/>
		<rot_elast rz="0" node="N3" id="B2"/>

	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.15"/>
		<barre h="0.3" id="B2" igz="8e-05" s="0.0053" v="0.15"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1"/>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""

  string2="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="1,0" dep="-0.01" id="N2" liaison="2"/>
		<node d="2,0" dep="-0.01" id="N3" liaison="2"/>
		<node d="3,0" id="N4" liaison="2,45"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,1" id="B1"/>
		<barre d="N2,N3,0,1" id="B2"/>
		<barre d="N3,N4" id="B3"/>

	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.15"/>
		<barre h="0.3" id="B2" igz="8e-05" s="0.0053" v="0.15"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1"/>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0,1.5" id="combi 3"/>
		<combinaison d="1.35,1.0" id="combi 2"/>
		<combinaison d="1.0,1.0" id="combi 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="1,0" id="N2" dep="0.01" liaison="2"/>
		<node d="2,0" id="N3" liaison="2,45"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
		<rot_elast rz="0" node="N2" id="B1"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.15"/>
		<barre h="0.3" id="B2" igz="8e-05" s="0.0053" v="0.15"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="1,0" id="N2" liaison="2"/>
		<node d="2,0" id="N3" liaison="2"/>
		<node d="3,0" id="N4" liaison="2,45"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,1" id="B1"/>
		<barre d="N2,N3,0,1" id="B2"/>
		<barre d="N3,N4" id="B3"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.15"/>
		<barre h="0.3" id="B2" igz="8e-05" s="0.0053" v="0.15"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
	<barre fp="%50,0.0,-1000.0,0.0" id="B2"/>

		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,-0.5" id="N1" liaison="0"/>
		<node d="1,0" id="N2"  dep="0,0.01" />
		<node d="2,0" id="N3"  dep="0,0.01" />
		<node d="3,-0.5" id="N4" liaison="0"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
		<barre d="N3,N4" id="B3"/>
		<rot_elast rz="0" node="N2" id="B1"/>
		<rot_elast rz="0" node="N3" id="B2"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.15"/>

	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
	<barre fp="%50,0.0,-1000000.0,0.0" id="B2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""

  string2="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="1,0" id="N2"  dep="0.01" liaison="2"/>
		<node d="2,0" id="N3"  dep="0.01" liaison="2"/>
		<node d="3,0" id="N4" liaison="0"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,1" id="B1"/>
		<barre d="N2,N3,0,1" id="B2"/>
		<barre d="N3,N4" id="B3"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.15"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
	<barre fp="%50,0.0,-1000000.0,0.0" id="B2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="combi 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""

  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="@N1,0,1" id="N2"/>
		<node d="@N1,0,2" id="N3" liaison="0"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
		<rot_elast rz="0" node="N2" id="B1"/>

	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="1" s="1" v="0.1"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="1"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<node d="1000.0,0.0,0.0" id="N2"/>

		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="Combinaison 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="@N1,1,2" id="N2"/>
		<node d="@N1,2,1" id="N3" liaison="0"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,1" id="B1"/>
		<barre d="N2,N3" id="B2"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8e-05" s="0.005" v="0.1"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<node d="0.0,-1000.0,0.0" id="N2"/>
			<barre fp="1,0.0,-1000.0,0.0" id="B2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="Combinaison 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node d="@N1,1,2" id="N2"/>
		<node d="@N1,2,1" id="N3" liaison="0"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
	<rot_elast rz="0" node="N2" id="B1"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8e-05" s="0.005" v="0.1"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<node d="0.0,-1000.0,0.0" id="N2"/>
		<barre fp="1,0.0,-1000.0,0.0" id="B2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0" id="Combinaison 1"/>
	</elem>
	<elem id="units">
		<unit d="1000000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="0.0001" id="S"/>
	</elem>
</data>"""

  rdm = fakeRdm(string)
  char = rdm.Chars['cas 1']
  print "errors=",rdm.struct.errors
  print char.ddlValue
  print "w relax", char.RelaxBarRotation
  barre = 'B2'
  l = rdm.struct.Lengths[barre]
  print rdm.TestDefoPoint(char, barre, l/2)
  print "React", char.Reactions
  print "EndBarSol", char.EndBarSol


  #print "terminé", rdm.valid
test()
#cProfile.run('test()')
