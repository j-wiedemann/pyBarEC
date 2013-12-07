#!/usr/bin/env python
# -*- coding: utf-8 -*-


 
import math
import os
from numpy import *
from xml.dom import minidom
from classRdm import *
import function

__version__='1.3'

__date__ = "2008-7-1"

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
    self.conv = 1
    #rdm = classRdm.R_Structure(struct)
    self.Cases = self.GetCasCharge()
    self.CombiCoef = self.GetCombi()
    xmlnode = self.struct.XMLNodes["char"].getElementsByTagName('case')
    self.Chars = {}
    for cas in self.Cases:
      Char = CasCharge(cas, xmlnode, self.struct)
      self.Chars[cas] = Char
    self.SolveCombis()


