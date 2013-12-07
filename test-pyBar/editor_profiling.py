#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cProfile
from fakeclassRdm import fakeRdm
import os
import sys
import pango
import gtk.glade
from xml.dom import minidom
from function import *
#import gobject
#from time import sleep
import Const
import classDialog
import classProfilManager
import classPrefs
from classEditor import Editor



def get_rdm():
  rdm = fakeRdm("XXX")
  rdm.file = 'test'
  rdm.name = 'test'
  string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N1" liaison="0"/>
		<node affaissement="0.02" d="3,0" id="N2" liaison="2"/>
		<node affaissement="0.02" d="@N2,5,0" id="N3" liaison="2"/>
		<node d="@N3,4,0" id="N4"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
		<barre d="N3,N4" id="B3"/>
	</elem>
	<elem id="geo">
		<barre h="0.3" id="*" igz="8.3e-05" s="0.0053" v="0.1"/>
		<barre h="0.3" id="B2" igz="8e-05" s="0.0053" v="0.1"/>
	</elem>
	<elem id="material">
		<barre id="*" mv="7800.0" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<barre id="*" pp="true"/>
		</case>
		<case id="cas 2">
			<barre fp="2,0.0,-1000.0,0.0" id="B1"/>
		</case>
		<case id="cas 3">
			<barre fp="4,0.0,-1000.0,0.0" id="B2"/>
		</case>
		<case id="cas 4">
			<barre fp="1,0.0,-1000.0,0.0" id="B3"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.0,0.0,0.0,0.0" id="combi1"/>
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
  rdm.fakeReadXMLFile(string)
  rdm.GetXMLElem()
  rdm._ExtractData()
  return rdm

def test(rdm):
  for i in range(20):
    Editor(rdm)
# init semble être la fonction la plus consommatrice en temps cpu !!!!
print "désactiver gobject dans classEditor"
rdm = get_rdm()
  #print "terminé", rdm.valid
cProfile.run('test(rdm)')
