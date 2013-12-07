#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
try:
  import pygtk
except:
  print "Librairie pygtk indisponible"
  sys.exit(0)
try:
  pygtk.require('2.0')
except:
  print "Nécessite pygtk2.0"
  sys.exit(0)
import gtk
#print gtk.pygtk_version
#print gtk.gtk_version
import gtk.glade
import pango
#from xml.dom import minidom
#import gobject
import classEditor
from file import *
#import classDrawing
import classRdm
import Const
import classProfilManager
import classPrefs
import classCMenu
import gobject
import function
from time import sleep
from xml.dom import minidom

class EditorTest(classEditor.Editor):

  def get_xml_structure(self, widget, n):
    if not self.mode == -1:
      self.data_editor._set_xml_structure()
    print self.data_editor.XML.toprettyxml()
    self.update_editor_title(False)


def fakeReadXMLFile(string):
    """Fonction de test
    Lecture des données dans une chaines de caractères"""
    return minidom.parseString(string)

string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.2">
	<elem id="node">
		<node d="0,0" id="N3" liaison="0"/>
		<node d="1&lt;45" id="N2"/>
		<node d="@N3,4.7,5.1" id="N1" dep="0,0.01"/>
		<node d="4.7,2" id="N4" liaison="3,1000,0,0"/>
		<node d="4.7,0" id="N5" liaison="0"/>
		<node d="4.7,2" id="N6" liaison="2,45"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2" id="B1"/>
		<barre d="N2,N3" id="B2"/>
		<barre d="N3,N4" id="B3"/>
		<barre d="N4,N5" id="B4"/>
		<barre d="N2,N4,1,1" id="B5"/>
		<rot_elast kz="1" node="N2" barre="B5"/>
		<rot_elast kz="1" node="N4" barre="B5"/>
	</elem>
	<elem id="geo">
		<barre h="0.19" id="*" igz="3.692e-05" profil="HE 200 A" s="0.00538" v="0.095"/>
		<barre h="0.19" id="B1" igz="3.6e-05" profil="" s="0.005" v="0.095"/>
		<barre h="0.19" id="B2" igz="3.66e-05" profil="" s="0.005" v="0.095"/>
	</elem>
	<elem id="material">
		<barre alpha="1e-5" id="*" mv="7800.0" young="210000000000.0"/>
		<barre alpha="2e-5" id="B1" mv="tt" young="200000000000.0"/>
	</elem>
	<elem id="char">
		<case id="cas 1">
			<barre id="*" pp="true"/>
			<node d="&lt;,100000.0,45,0.0" id="N2"/>
			<node d="100000.0,0.0,0.0" id="N1"/>
			<barre id="B1" therm="50.0,0.0"/>
			<barre id="B2" tri="@,0.5,2.1,3.0,5.0,48.0"/>
			<barre id="B2" tri="@,%25,%35,1.0,2.0,45.0"/>
			<barre id="B2" tri="%5,%15,1.0,2.0,49.0"/>
		</case>
		<case id="cas 2">
			<barre id="B2" qu="0,1,0.0,-120000.0"/>
			<barre id="B1" qu="%25,%35,0.0,-120000.0"/>
			<barre id="B1" qu="@,%5,%35,0.0,-10000.0"/>
		</case>
		<case id="cas 3">
			<barre fp="%50,0.0,-120000.0,0.0" id="B2"/>
			<barre fp="2,0.0,-150000.0,0.0" id="B2"/>
			<barre fp="@,2,0.0,-150000.0,0.0" id="B2"/>
			<barre fp="@&lt;,2,2000.0,45,5" id="B2"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.35,1.5,0.0" id="combi 1"/>
		<combinaison d="1.35,1.5,2.0" id="combi 2"/>
	</elem>
	<elem id="prefs">
		<unit d="1000.0" id="C"/>
		<unit d="1000000000.0" id="E"/>
		<unit d="1000.0" id="F"/>
		<unit d="1e-08" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="0.01" id="L"/>
		<unit d="0.0001" id="S"/>
		<const g="10" />
	</elem>
</data>"""

string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.3">
	<elem id="node">
		<node d="0.0,0.0" id="N1" liaison="1"/>
		<node d="19.6850393701,0.0" id="N2" dep="0,0.5" liaison="3,0.0,0.0,0.0"/>
		<node d="39.3700787402,0.0" id="N3" liaison="2"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,0" id="B1"/>
		<barre d="N2,N3,0,0" id="B2"/>
		<rot_elast kz="1" node="N2" barre="B2"/>
	</elem>
	<elem id="geo">
		<barre h="" id="*" igz="2.40251206662e-06" profil="" s="232.500465001" v=""/>
	</elem>
	<elem id="material">
		<barre id="*" young="145037.680789"/>
	</elem>
	<elem id="char">
		<case id="fp">
			<node d="0.0,-0.224809024733,0.0" id="N2"/>
		</case>
		<case id="cas 2">
			<node d="0.0,-0.224809024733,0.0" id="N2"/>
		</case>
	</elem>
	<elem id="combinaison"/>
	<elem id="prefs">
		<unit d="6894.76" id="C"/>
		<unit d="6894.76" id="E"/>
		<unit d="4.44822" id="F"/>
		<unit d="4.16231e-7" id="I"/>
		<unit d="0.45359237" id="M"/>
		<unit d="0.0254" id="L"/>
		<unit d="6.4516e-4" id="S"/>
		<const g="10.0"/>
		<conv conv="1.0"/>
	</elem>
</data>
"""
string="""<?xml version="1.0" ?>
<data pyBar="http://open.btp.free.fr/?/pyBar" version="2.3">
	<elem id="node">
		<node d="0.0,0.0" id="N1" liaison="1"/>
		<node d="10.0,0.0" id="N2" liaison="2"/>
		<node d="12.0,0.0" id="N3" liaison="2"/>
		<node d="15.0,0.0" id="N4" liaison="2"/>
		<node d="18,0" id="N5" liaison="2"/>
	</elem>
	<elem id="barre">
		<barre d="N1,N2,0,0" id="B1"/>
		<barre d="N2,N3,0,0" id="B2"/>
		<barre d="N3,N4,0,0" id="B3"/>
		<barre d="N4,N5,0,0" id="B4"/>
	</elem>
	<elem id="geo">
		<barre h="0.14" id="*" igz="6.05e-06" profil="UPN 140" s="0.00204" v="0.07"/>
	</elem>
	<elem id="material">
		<barre id="B1,B2" mv="7800" young="210000"/>
		<barre id="B3" mv="7000" young="200000"/>
	</elem>
	<elem id="char">
		<case id="CP">
			<barre id="*" pp="true"/>
		</case>
		<case id="Q1">
			<barre id="B1" qu="0,,0.0,-10000"/>
		</case>
		<case id="Q2">
			<barre id="B2" qu="0,,0.0,-10000.0"/>
		</case>
		<case id="Q3">
			<barre id="B3" qu="0,,0.0,-10000.0"/>
		</case>
	</elem>
	<elem id="combinaison">
		<combinaison d="1.35,1.5,0.0,0.0" id="1,35G+1,5Q1"/>
		<combinaison d="1.35,1.5,1.5,1.5" id="1,35G+1,5Q1+1,5Q2+1,5Q3"/>
		<combinaison d="1.35,1.5,0.0,1.5" id="1,35G+1,5Q1+1,5Q3"/>
		<combinaison d="1.35,0.0,1.5,0.0" id="1,35G+1,5Q2"/>
		<combinaison d="1.35,0.0,0.0,1.5" id="1,35G+1,5Q3"/>
		<combinaison d="1.0,1.0,1.0,1.0" id="G+Q1+Q2+Q3"/>
	</elem>
	<elem id="prefs">
		<unit d="1.0" id="C"/>
		<unit d="1000000.0" id="E"/>
		<unit d="1.0" id="F"/>
		<unit d="1.0" id="I"/>
		<unit d="1.0" id="M"/>
		<unit d="1.0" id="L"/>
		<unit d="1.0" id="S"/>
		<const g="9.81"/>
		<conv conv="1.0"/>
	</elem>
</data>"""

class fakeEmptyRdm(classEditor.EmptyRdm) :
  """Programme de calcul RDM"""
  
  def __init__(self):
    self.XMLNodes = None
    self.name = 'test'

  def GetUnits(self, UP=None):
    return Const.default_unit()

class fakeRdm(classRdm.R_Structure):
  """Programme de calcul RDM"""
  
  def __init__(self, xml):
    # si on n'écrit pas ici explicitement le init de la classe parent, ce dernier n'est pas exécuté
    #self.struct = classRdm.StructureFile("exemples/portique-simple2.dat")
    #self.struct = classRdm.StructureFile("exemples/barre-affaissement-appui.dat")
    xml = fakeReadXMLFile(string)
    self.struct = classRdm.Structure(xml)
    self.XMLNodes = self.struct.XMLNodes
    self.struct.file = "test_file"
    self.struct.name = "test_name"
    self.char_error = []
    self.conv = self.GetConv()


    self.Cases = self.GetCasCharge()
    self.CombiCoef = self.GetCombi()
    xmlnode = self.struct.XMLNodes["char"].getElementsByTagName('case')
    self.Chars = {}
    for cas in self.Cases:
      Char = classRdm.CasCharge(cas, xmlnode, self.struct)
      self.Chars[cas] = Char
    self.SolveCombis()

class fakeStudy(object):
  def __init__(self, rdm):
    self.rdm = rdm
    self.id = 0

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
  rdm = fakeRdm(string)
  study = fakeStudy(rdm)
  #rdm = fakeEmptyRdm()
  try:
    MyApp = EditorTest(study)
    MyApp.record_button.connect("clicked", MyApp.get_xml_structure, 0)
    main()
  except KeyboardInterrupt:
    sys.exit(0)


