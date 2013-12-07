#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from time import sleep
#from fakeclassRdm import fakeRdm
from classEditor import Editor
from classDialog import Dialog
import unittest
from xml.dom import minidom
import gtk
import gobject
def get_model_elem(model):
    """Retourne la liste des elem d'un model de combo"""
    li = []
    for elem in model:
      li.append(elem[0])
    return li

class FakeDialog(Dialog):
  pass

class FakeEditor(Editor):
  def __init__(self, app, new=False):
    #Editor.__init__(self, app, False)
    self.new = new
    self.xml = gtk.glade.XML("glade/pyBar.glade", "window2")
    self.w2=self.xml.get_widget("window2")
    self.xml.signal_autoconnect({
	 "on_w2_button2_clicked" : self.w1_refresh,
	 "on_w2_button4_clicked" : self.show_help,
	 "on_w2_button5_clicked" : self.add_page,
	 "on_w2_button6_clicked" : self.remove_page,
	 "on_w2_button8_clicked" : self._add_combinaison,
	 "on_w2_button9_clicked" : self._remove_combi,
	 "on_change_current_page" : self.get_page_num,
	 "on_change_unit" : self.get_unit,
	 "on_window2_destroy" : self.destroy,
	 "on_w2_button3_clicked" : self.destroy })
    self.book = self.xml.get_widget("book1")
    self.nodeList=[] 
    self.idHandlerList=[]



class EmptyRdm():
  """Inutile si self.new =True dans FakeEditor"""
  def __init__(self):
    self.xmldoc=""
  def GetRawNode(self):
    # retourne une liste à finir
    return ["N1:0,0", "N2:@,1,1", "N3:@N1,2,3"]
  def GetRawAppui(self):
    return [[], []]
  def GetRawBarre(self):
    return ["B1:N1,N2", "B2:N2,N3,1,1"]
  def GetRawCarac(self):
    return ["*:1,1"]
  def GetRawMaterial(self):
    return [{"*":1.}, {}, {}]
  def GetRawMv(self):
    return "*:1000"
  def GetRawAlpha(self):
    return "*:5e-4"
  def GetCombi(self):
    return {"combi1" : {"cas1":1}}
  def GetCasCharge(self):
    return ""
  def GetUnits(self):
    return {'F':1., 'E':1., 'M':1., 'S':1., 'I':1.}

class MyApp:
  def __init__(self, rdm):
    self.rdm = rdm
    self.rdm.file = "aucun"
    self.rdm.name = "test"

class emptyEditor(unittest.TestCase) :

  def setUp(self):
    self.rdm = EmptyRdm()
    self.ed=self._genere_editor()
    #print dir(self.ed)

  def tearDown(self):  
    del self.ed
    self.ed = None

  def _genere_editor(self):
    print "erreur : effacer multi processing:: refaire une classe héritée"
    rdm=self.rdm
    app = MyApp(rdm)
    editor=FakeEditor(app, True)
    #editor.put_data_to_editor()
    return editor


  def test_make_row_node(self): # incomplet
    vbox=gtk.VBox(False,0)
    elem="N8:0,0"
    self.ed._make_row_node(vbox, elem)
    hbox=vbox.get_children()[0]
    assert isinstance(hbox, gtk.HBox)
    iter = enumerate(hbox.get_children())
    tuple1=iter.next()
    # checkbutton suppression
    assert isinstance(tuple1[1], gtk.CheckButton)
    tuple1=iter.next()
    # entry nom du noeud
    assert isinstance(tuple1[1], gtk.Entry)
    assert tuple1[1].get_text() == "N8"

    tuple1=iter.next()
    combobox=tuple1[1]
    # combo noeud relatif
    assert isinstance(combobox, gtk.ComboBox)

    tuple1=iter.next()
    # entry X
    assert isinstance(tuple1[1], gtk.Entry)
    assert tuple1[1].get_text() == "0"

    tuple1=iter.next()
    combobox=tuple1[1]
    # combo noeud relatif
    assert isinstance(combobox, gtk.ComboBox)
    model = combobox.get_model()
    index = combobox.get_active()
    assert model[index][0] == ""

    tuple1=iter.next()
    # entry Y
    assert isinstance(tuple1[1], gtk.Entry)
    assert tuple1[1].get_text() == "0"
    del self.ed.nodeList

  def test_fill_preceding_node(self):
    combobox = gtk.combo_box_new_text()
    list=[]
    assert self.ed._fill_preceding_node(combobox, list) is None
    combobox = gtk.combo_box_new_text()
    list=["N1","N2","N3"]
    assert self.ed._fill_preceding_node(combobox, list) is None
    assert combobox.get_active() == 0
    combobox = gtk.combo_box_new_text()
    assert self.ed._fill_preceding_node(combobox, list, "N3") is None
    assert combobox.get_active() == 3 # nb elem + premier elem vide
    combobox = gtk.combo_box_new_text()
    assert self.ed._fill_preceding_node(combobox, list, "XXX") is not None
    assert combobox.get_active() == 0


  def test_update_node_combo(self):
    nodeList=["N1","N2","N3"]
    combobox = gtk.combo_box_new_text()
    self.ed._update_node_combo(combobox, nodeList, "N3")
    assert combobox.get_active() == 2
    self.ed.nodeList=[]
    combobox = gtk.combo_box_new_text()
    self.ed._update_node_combo(combobox, nodeList, "XXX")
    assert combobox.get_active() == -1

  def test_remove_elem_combo(self):
    # test 1 :: combo vide
    combobox = gtk.combo_box_new_text()
    assert self.ed._remove_elem_combo(combobox) == ""
    # test 2 :: 3 éléments
    nodeList=["N1","N2","N3"]
    self.ed._update_node_combo(combobox, nodeList, "N3")
    assert self.ed._remove_elem_combo(combobox) == "N3"
    model = combobox.get_model()
    assert len(model) == 0
    # test 2 :: 3 éléments
    nodeList=["N1","N2","N3"]
    self.ed._update_node_combo(combobox, nodeList, "")
    assert self.ed._remove_elem_combo(combobox) == ""
    model = combobox.get_model()
    assert len(model) == 0

class realEditor(unittest.TestCase) :
  def setUp(self):
    self.rdm = EmptyRdm()
    self.ed=self._genere_editor()
  
  def tearDown(self):  
    del self.ed
    self.ed = None

  def _genere_editor(self):
    rdm=self.rdm
    app = MyApp(rdm)
    editor=Editor(app, False)
    return editor

  def test_update_preceding_node(self):
    self.ed._update_preceding_node(0)
    vbox=self.ed.book.get_nth_page(0)
    # sw -> viewport -> vbox
    box=vbox.get_children()[1].get_children()[0].get_children()[0]
    for i,hbox in enumerate(box.get_children()):
      assert isinstance(hbox, gtk.HBox)
      if i == 0: continue
      combobox = hbox.get_children()[2]
      index = combobox.get_active()
      assert isinstance(combobox, gtk.ComboBox)
      model = combobox.get_model()
      li = get_model_elem(model)
      if i == 2 : 
        assert li == ["","N1"]
        assert model[index][0] == "N1"
      elif i == 3 : 
        assert li == ["","N1","N2"]
        assert model[index][0] == "N1"
    #print self.ed.nodeList

  def test_update_node_list(self):
    # modification de la liste des noeuds
    self.ed.nodeList=["N4", "N3", "N2"]
    box = self.ed.data_box['barre']
    combobox = box.get_children()[1].get_children()[2]
    model = combobox.get_model()
    assert isinstance(combobox, gtk.ComboBox)
    # renommage du noeud N1 en noeud N4
    self.ed._update_node_list("N4","N1")
    model = combobox.get_model()
    index = combobox.get_active()
    # vérification que le noeud N4 est actif
    assert model[index][0] == "N4"

if __name__ == '__main__':
  unittest.main()

