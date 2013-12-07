#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import Const
import function
import xml.etree.ElementTree as ET

def exit_as_ok_func():
  dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
					gtk.MESSAGE_QUESTION,
					gtk.BUTTONS_YES_NO,
			"Les données ont été modifiées dans la librairie des profilés. Voulez-vous les enregistrer?")
  dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
  result = dialog.run()
  dialog.destroy()
  if result == gtk.RESPONSE_YES:
    return True
  elif result == gtk.RESPONSE_NO:
    return False
  return None

def delete_as_ok_func(name):
  dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
				gtk.MESSAGE_QUESTION,
				gtk.BUTTONS_YES_NO,
		"Voulez-vous vraiment effacer \"%s\" et tout son contenu?" % name)
  result = dialog.run()
  dialog.destroy()
  if result == gtk.RESPONSE_YES:
    return True
  return False

class Singleton(object):
  def __new__(cls, *args, **kwargs):
    if '_inst' not in vars(cls):
      cls._inst = object.__new__(cls, *args, **kwargs)
    return cls._inst

  # close the window and quit
  def destroy(self):
    if self.has_changed:
      status = exit_as_ok_func()
      if status == True:
        self._save()
        self.window.destroy()
        return False
      elif status == False:
        return False
      return True
    self.window.destroy()
    return False

  # close the window and main quit
  def main_delete_event(self, widget, event):
    if self.has_changed:
      status = exit_as_ok_func()
      if status == True:
        self._save()
        gtk.main_quit()
        return False
      elif status == False:
        gtk.main_quit()
        return False
      return True
    gtk.main_quit()
    return False


  def on_dragdata_received_cb(self, treeview, drag_context, x, y,\
 				    selection, info, eventtime):
    """Fonction pour gérer l'événement du DND"""
    model, iter_to_copy = treeview.get_selection().get_selected()
    temp = treeview.get_dest_row_at_pos(x, y)
    if temp != None:
      path, pos = temp
    else:
      path, pos = (len(model)-1,), gtk.TREE_VIEW_DROP_AFTER
    target_iter = model.get_iter(path)
    if self.check_row_path(model, iter_to_copy, target_iter, pos):
      self._iter_copy(model, iter_to_copy, target_iter, pos)
      drag_context.finish(True, True, eventtime)
      self.has_changed = True
      #treeview.expand_all()
    else:
      drag_context.finish(False, False, eventtime) 

  def _iter_copy(self, model, iter_to_copy, target_iter, pos):
    """Fonction itérative pour le déplacement des éléments du treeview"""
    n = len(model[0]) # tester
    data = []
    for i in range(n):
      data.append(model.get_value(iter_to_copy, i))
    if (pos == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE) or (pos == gtk.TREE_VIEW_DROP_INTO_OR_AFTER):
      new_iter = model.prepend(target_iter, data)
    elif pos == gtk.TREE_VIEW_DROP_BEFORE:
      new_iter = model.insert_before(None, target_iter, data)
    elif pos == gtk.TREE_VIEW_DROP_AFTER:
      new_iter = model.insert_after(None, target_iter, data)

    for n in range(model.iter_n_children(iter_to_copy)): 
      next_iter_to_copy = model.iter_nth_child(iter_to_copy, n)
      self._iter_copy(model, next_iter_to_copy, new_iter,
			gtk.TREE_VIEW_DROP_INTO_OR_BEFORE)

  def _ini_tools(self): # XXX revoir
    """Création de la barre d'outils supérieure"""
    toolbar = gtk.Toolbar()
    toolbar.set_size_request(400, 80)
    toolbar.set_border_width(5)

    toolitem = gtk.ToolItem()
    iconbox = gtk.VBox(False, 0)
    #toolitem.set_expand(False)
    toolitem.set_border_width(5)
    button = gtk.Button()
    button.unset_flags(gtk.CAN_FOCUS)
    button.set_relief(gtk.RELIEF_NONE)
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_BUTTON)
    iconbox.pack_start(image, False, False, 0)
    label = gtk.Label("Enregistrer")
    iconbox.pack_start(label, False, False, 0)
    button.add(iconbox)
    button.connect("clicked", self._save)
    toolitem.add(button)
    toolitem.set_tooltip_text('Enregistrer la librairie')
    toolbar.insert(toolitem, 0)

    toolitem = gtk.ToolItem()
    iconbox = gtk.VBox(False, 0)
    toolitem.set_border_width(5)
    button = gtk.Button()
    button.unset_flags(gtk.CAN_FOCUS)
    button.set_relief(gtk.RELIEF_NONE)
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON)
    iconbox.pack_start(image, False, False, 0)
    label = gtk.Label(self.BUTTON_LABEL)
    iconbox.pack_start(label, False, False, 0)
    button.add(iconbox)
    button.connect("clicked", self._insert_profil)
    toolitem.add(button)
    toolitem.set_tooltip_text('Ajouter un élément')
    toolbar.insert(toolitem, 1)

    toolitem = gtk.ToolItem()
    iconbox = gtk.VBox(False, 0)
    toolitem.set_border_width(5)
    button = gtk.Button()
    button.unset_flags(gtk.CAN_FOCUS)
    button.set_relief(gtk.RELIEF_NONE)
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_BUTTON)
    iconbox.pack_start(image, False, False, 0)
    label = gtk.Label("Groupe")
    iconbox.pack_start(label, False, False, 0)
    button.add(iconbox)
    button.connect("clicked", self._insert_group)
    toolitem.add(button)
    toolitem.set_tooltip_text('Ajouter un groupe')
    toolbar.insert(toolitem, 2)

    toolitem = gtk.ToolItem()
    iconbox = gtk.VBox(False, 0)
    toolitem.set_border_width(5)
    button = gtk.Button()
    button.unset_flags(gtk.CAN_FOCUS)
    button.set_relief(gtk.RELIEF_NONE)
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_BUTTON)
    iconbox.pack_start(image, False, False, 0)
    label = gtk.Label("Défaut")
    iconbox.pack_start(label, False, False, 0)
    button.add(iconbox)
    button.connect("clicked", self._restaure_default)
    toolitem.add(button)
    toolitem.set_tooltip_text('Restaurer la librairie par défaut')
    toolbar.insert(toolitem, 3)
 
    toolbar.show_all()
    return toolbar

  def drag_data_get_data(self, treeview, context, selection, target_id,
                           etime): # inutilisée
    #print "drag_data_get_data"
    treeselection = treeview.get_selection()
    model, iter = treeselection.get_selected()
    data = []
    for i in range(5): # XXX automatiser
      data.append(model.get_value(iter, i))
    data[0] = str(data[0]) # conversion booléen
    li = []
    for i in data: # XXX provisoire
      if i == None:
        li.append("")
      else:
        li.append(i)
    data = li
    #data = [i for i in data if not i is None]
    print data
    data = '\n'.join(data)
    selection.set(selection.target, 8, data)

    # Code à garder pour filtrer une ligne
    # peut servir à n'afficher que les répertoires 
    # create the filter to hide first column
    #filter = self.treestore.filter_new()
    #filter.set_visible_column(0)
    #self.treeview = gtk.TreeView(filter)

  def col_edited_cb( self, cell, path, new_text, model, col):
    """Called when a text cell is edited.  It puts the new text
    in the model so that it is displayed properly."""
    #print "Change '%s' to '%s'" % (model[path][col], new_text)
    if not model[path][col] == new_text:
      self.has_changed = True
    model[path][col] = new_text

  def check_row_path(self, model, iter_to_copy, target_iter, pos):
    type_copy = model.get_value(iter_to_copy, 0)
    type_dest = model.get_value(target_iter, 0)
    # on empèche de pouvoir insérer dans un profil
    if (pos == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE) or (pos == gtk.TREE_VIEW_DROP_INTO_OR_AFTER) and type_dest == False: return False

    path_of_iter_to_copy = model.get_path(iter_to_copy)
    path_of_target_iter = model.get_path(target_iter)
    if path_of_target_iter[0:len(path_of_iter_to_copy)] ==\
		path_of_iter_to_copy:
      return False
    else:
      return True

  def _restaure_default(self, widget):
    """Restaure la librairie par défaut"""
    self.treestore.clear()
    self._read_xml_file(self.DEFAULT_FILE)
    self.has_changed = True


  def _read_xml_file(self, file):
    """Ouvre et extrait le fichier xml"""
    try:
      tree = ET.parse(file)
    except:
      print "Impossible d'extraire le contenu du fichier %s" % file
      return False
    root = tree.getroot()
    for elem in root:
      self._fill_treestore(elem)

  def _write_data(self, xml, root, file):
    """Ecriture dans le fichier de données au format xml"""
    path = os.path.join(Const.PATH, Const.USERDIRLIBRARY)
    if not os.path.isdir(path):
      os.mkdir(path)
    file = os.path.join(path, file)
    #print ET.tostring(root)
    #return
    try:
      xml.write(file, encoding="UTF-8", xml_declaration=True)
    except IOError:
      print "Impossible d'ouvrir le fichier %s" % self.DEFAULT_FILE

  def _event_handler(self, widget, event):
    if not  event.type == gtk.gdk.KEY_PRESS: return
    key = gtk.gdk.keyval_name (event.keyval)
    if not key == "Delete": return

    model, iter = self.treeview.get_selection().get_selected()
    if iter is None: return
    type = model.get_value(iter, 0)
    name = model.get_value(iter, 1)

    if type == True:
      if delete_as_ok_func(name):
        self.treestore.remove(iter)
      else: return
    else:
      self.treestore.remove(iter)
    self.has_changed = True

  def _active_selected(self):
    """Ouvre le treeview et active l'élément sélectionné"""
    if self.path == None: return
    self.treeview.expand_to_path(self.path)
    treeselection = self.treeview.get_selection()
    treeselection.select_path(self.path)
    self.treeview.scroll_to_cell(self.path)
    


class MaterialManager(Singleton):

  TARGETS = [('text/plain', gtk.TARGET_SAME_WIDGET, 0)]
  DEFAULT_FILE = "library/default_material.xml"
  BUTTON_LABEL = "Matériau"

  def __init__(self, selected=None):
    # la classe est héritée de Singleton
    if hasattr(self, 'window') and not self.window == None: return
    self.selected = selected
    self.has_changed = False
    self.path = None
    # Create a new window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_icon_from_file("glade/logo.png")
    self.window.set_title("Gestionnaire des matériaux")

    self.window.set_size_request(500, 500)
    self.window.set_destroy_with_parent(True)

    vbox = gtk.VBox(False, 0)
    vbox.show()
    hbox = self._ini_tools()
    vbox.pack_start(hbox, False, False, 0)

    # create a TreeStore with many strings column to use as the model
    self.treestore = gtk.TreeStore("gboolean", gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)


    # importation depuis fichier cvs
    #self._fill_treestore_cvs()
    path = os.path.join(Const.PATH, Const.USERDIRLIBRARY)
    if not os.path.isdir(path):
      file = self.DEFAULT_FILE
    else:
      file = os.path.join(path, Const.MATFILELIBRARY)
      if not os.path.isfile(file):
        file = self.DEFAULT_FILE
    self._read_xml_file(file)

    # create the TreeView using treestore
    self.treeview = gtk.TreeView(self.treestore)
    self.treeview.connect('event', self._event_handler)
    self.treeview.connect('cursor-changed', self._change_row)
 
    # DND
    self.treeview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
			self.TARGETS,
			gtk.gdk.ACTION_DEFAULT|
			gtk.gdk.ACTION_MOVE)
    self.treeview.enable_model_drag_dest(self.TARGETS,
			gtk.gdk.ACTION_DEFAULT)

    self.treeview.connect("drag_data_received",
			self.on_dragdata_received_cb)
   
    # create the TreeViewColumn to display the data

    # groupe ou profil
    self.column0 = gtk.TreeViewColumn('Private')
    self.column0.set_visible(False)
    # nom
    self.column1 = gtk.TreeViewColumn('Nom')
    # Coef Young
    self.column2 = gtk.TreeViewColumn('Module\nd\'Young\n(GPa)')
    self.column3 = gtk.TreeViewColumn()
    # MV
    label = gtk.Label("Masse\nvolumique\n(kg/m<sup>3</sup>)")
    label.set_use_markup(True)
    label.show()
    self.column3.set_widget(label)
    # alpha
    self.column4 = gtk.TreeViewColumn()
    label = gtk.Label("Coefficient\nde dilatation\n(K<sup>-1</sup>)")
    label.set_use_markup(True)
    label.show()
    self.column4.set_widget(label)

    # add columns to treeview
    self.treeview.append_column(self.column0)
    self.treeview.append_column(self.column1)
    self.treeview.append_column(self.column2)
    self.treeview.append_column(self.column3)
    self.treeview.append_column(self.column4)

    # create a CellRendererText to render the data
    self.cell0 = gtk.CellRendererText()
    self.cell1 = gtk.CellRendererText()
    self.cell1.set_property('editable', True)
    # numéro de la colonne (attention à la colonne invisible)
    self.cell1.connect( 'edited', self.col_edited_cb, self.treestore, 1)
    self.cell2 = gtk.CellRendererText()
    self.cell2.connect( 'edited', self.col_edited_cb, self.treestore, 2)
    self.cell3 = gtk.CellRendererText()
    self.cell3.connect( 'edited', self.col_edited_cb, self.treestore, 3)
    self.cell4 = gtk.CellRendererText()
    self.cell4.connect( 'edited', self.col_edited_cb, self.treestore, 4)

    # add the cell0 to the column1 and allow it to expand
    self.column0.pack_start(self.cell0, True)
    self.column1.pack_start(self.cell1, True)
    self.column2.pack_start(self.cell2, True)
    self.column3.pack_start(self.cell3, True)
    self.column4.pack_start(self.cell4, True)

    # set the cell "text" attribute to column 0 - retrieve text
    # from that column in treestore
    self.column0.add_attribute(self.cell0, 'text', 0)
    self.column1.add_attribute(self.cell1, 'text', 1)
    self.column2.add_attribute(self.cell2, 'text', 2)
    self.column3.add_attribute(self.cell3, 'text', 3)
    self.column4.add_attribute(self.cell4, 'text', 4)

    # make it searchable
    self.treeview.set_search_column(0)
    # XXX inutile??

    # Allow sorting on the column # XXX revoir
    self.column1.set_sort_column_id(0) # attention : 0 devient la colonne visible 

    # Allow drag and drop reordering of rows
    #self.treeview.set_reorderable(True)

    # active l'élément sélectionné
    self.window.set_focus(self.treeview)
    self._active_selected()
    #self.treeview.set_flags(gtk.CAN_FOCUS)

    sw = gtk.ScrolledWindow()
    sw.add(self.treeview)
    
    vbox.pack_start(sw, True, True, 0)
    self.window.add(vbox)
    self.window.show_all()

  def send_data(self, widget=None):
    """Retourne la liste des caractéristiques d'un profilé"""
    model, iter = self.treeview.get_selection().get_selected()
    resu = None
    if iter:
      resu = []
      for i in range(1, 5):
        val = model.get_value(iter, i)
        if val == None:
          return None
        resu.append(val)
    return resu


  def _fill_treestore(self, node, parent_iter=None):
    """Méthode récursive pour remplir le treeview"""
    name = node.get('id')
    if node.tag == 'group':
      type = True
      E, mv, a = None, None, None
    else:
      type = False
      E = node.get('young')
      mv = node.get('mv')
      a = node.get('alpha')
    if parent_iter == None:
      parent_iter = self.treestore.append(None, [type, name, E, mv, a])
    else:
      parent_iter = self.treestore.append(parent_iter, [type, name, E, mv, a])
    if self.selected == name:
      self.path = self.treestore.get_path(parent_iter)
    for elem in node:
      self._fill_treestore(elem, parent_iter)


  def _change_row(self, widget):
    """Rend éditable ou non les colonnes 1 à + en fonction du type de ligne"""
    model, iter = self.treeview.get_selection().get_selected()
    if iter: # XXX utiliser self.cell ???
      type = model.get_value(iter, 0)
      cell2 = self.treeview.get_columns()[2].get_cell_renderers()
      cell3 = self.treeview.get_columns()[3].get_cell_renderers()
      cell4 = self.treeview.get_columns()[4].get_cell_renderers()
      if type:
        cell2[0].set_property('editable', False)
        cell3[0].set_property('editable', False)
        cell4[0].set_property('editable', False)
      else:
        cell2[0].set_property('editable', True)
        cell3[0].set_property('editable', True)
        cell4[0].set_property('editable', True)



  def _insert_profil(self, widget):
    iter = self.treestore.insert(None, 0, (False, 'Nouveau', '', '', ''))
    self.treeview.get_selection().select_iter(iter)
    path = self.treestore.get_path(iter)
    # move scrollbar
    self.treeview.scroll_to_cell(path)
    self.has_changed = True

  def _insert_group(self, widget):
    iter = self.treestore.insert(None, 0, (True, 'Nouveau groupe', '', '', ''))
    self.treeview.get_selection().select_iter(iter)
    path = self.treestore.get_path(iter)
    # move scrollbar
    self.treeview.scroll_to_cell(path)
    self.has_changed = True

  def _get_rows(self, model, iter, data, string):
    """Méthode de récupération des lignes du treemodel
    key contient une clé du type 0:1"""
    key = model.get_string_from_iter(iter)
    string.append(key)
    data.append([model.get_value(iter, 0),
		model.get_value(iter, 1),
		model.get_value(iter, 2),
		model.get_value(iter, 3),
		model.get_value(iter, 4)
		])
    for n in range(model.iter_n_children(iter)):
      child = model.iter_nth_child(iter, n)
      self._get_rows(model, child, data, string)
   

  def _save(self, widget=None):
    """Enregistre les modifications de la librairie dans le fichier utilisateur"""
    iter = self.treestore.get_iter_first()
    li_data = []
    # les dictionnaires ne permettent pas de conserver l'ordre
    li_string = []
    for n in range(self.treestore.iter_n_children(None)):
      self._get_rows(self.treestore, iter, li_data, li_string)
      iter = self.treestore.iter_next(iter)

    # création du xml
    string = '<data pyBar="%s" version="%s"></data>' % (Const.SITE_URL, Const.VERSION)
    xml = ET.ElementTree(ET.fromstring(string))
    root = xml.getroot()
    prec = 0
    prec_node = root
    parents = {0: root}
    for i, key in enumerate(li_string):
      n = len(key.split(':'))
      type = li_data[i][0]
      name = "%s" % li_data[i][1]
      if n == prec: # meme niveau, meme parent
        parent = parents[n-1]
      elif n == prec + 1: # niveau inférieur
        parent = prec_node
        parents[prec] = prec_node
      else:
        parent = parents[n-1]
      if type == True:
        node = ET.SubElement(parent, "group", {"id": name})
      else:
        node = ET.SubElement(parent, "materiau", {"id": name})
        E = "%s" % li_data[i][2].replace(',', '.')
        mv = "%s" % li_data[i][3].replace(',', '.')
        a = "%s" % li_data[i][4].replace(',', '.')
        node.set("young", E)
        node.set("mv", mv)
        node.set("alpha", a)
      prec_node = node
      prec = n
    function.indent(root)
    self._write_data(xml, root, Const.MATFILELIBRARY)
    self.has_changed = False



class ProfilManager(Singleton):

  TARGETS = [('text/plain', gtk.TARGET_SAME_WIDGET, 0)]
  DEFAULT_FILE = "library/default_section.xml"
  BUTTON_LABEL = "Section"


  def __init__(self, selected=None):
    # la classe est héritée de Singleton
    if hasattr(self, 'window') and not self.window == None: return
    self.selected = selected
    self.has_changed = False
    self.path = None
    # Create a new window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_icon_from_file("glade/logo.png")
    self.window.set_title("Gestionnaire des profilés")

    self.window.set_size_request(500, 500)
    self.window.set_destroy_with_parent(True)

    #self.window.connect("delete_event", self.delete_event)
    vbox = gtk.VBox(False, 0)
    vbox.show()
    hbox = self._ini_tools()
    vbox.pack_start(hbox, False, False, 0)

    # create a TreeStore with many strings column to use as the model
    self.treestore = gtk.TreeStore("gboolean", gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING)


    # importation depuis fichier cvs
    #self._fill_treestore_cvs()
    path = os.path.join(Const.PATH, Const.USERDIRLIBRARY)
    if not os.path.isdir(path):
      file = self.DEFAULT_FILE
    else:
      file = os.path.join(path, Const.PROFILFILELIBRARY)
      if not os.path.isfile(file):
        file = self.DEFAULT_FILE
    self._read_xml_file(file)

    # create the TreeView using treestore
    self.treeview = gtk.TreeView(self.treestore)
    self.treeview.connect('event', self._event_handler)
    self.treeview.connect('cursor-changed', self._change_row)
 
    # DND
    self.treeview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
			self.TARGETS,
			gtk.gdk.ACTION_DEFAULT|
			gtk.gdk.ACTION_MOVE)
    self.treeview.enable_model_drag_dest(self.TARGETS,
			gtk.gdk.ACTION_DEFAULT)

    self.treeview.connect("drag_data_received",
			self.on_dragdata_received_cb)
   
    # create the TreeViewColumn to display the data

    # groupe ou profil
    self.column0 = gtk.TreeViewColumn('Private')
    self.column0.set_visible(False)
    # nom
    self.column1 = gtk.TreeViewColumn('Nom')
    # masse linéique
    self.column2 = gtk.TreeViewColumn('Masse\nlinéique\n(kg/m)')
    self.column3 = gtk.TreeViewColumn()
    # A
    label = gtk.Label("Section\nDroite\n(cm<sup>2</sup>)")
    label.set_use_markup(True)
    label.show()
    self.column3.set_widget(label)
    # moment
    self.column4 = gtk.TreeViewColumn()
    label = gtk.Label("Moment\nQuadratique\n(cm<sup>4</sup>)")
    label.set_use_markup(True)
    label.show()
    self.column4.set_widget(label)
    # hauteur
    self.column5 = gtk.TreeViewColumn('h\n(cm)')

    # add columns to treeview
    self.treeview.append_column(self.column0)
    self.treeview.append_column(self.column1)
    self.treeview.append_column(self.column2)
    self.treeview.append_column(self.column3)
    self.treeview.append_column(self.column4)
    self.treeview.append_column(self.column5)

    # create a CellRendererText to render the data
    self.cell0 = gtk.CellRendererText()
    self.cell1 = gtk.CellRendererText()
    self.cell1.set_property('editable', True)
    # numéro de la colonne (attention à la colonne invisible)
    self.cell1.connect( 'edited', self.col_edited_cb, self.treestore, 1)
    self.cell2 = gtk.CellRendererText()
    self.cell2.connect( 'edited', self.col_edited_cb, self.treestore, 2)
    self.cell3 = gtk.CellRendererText()
    self.cell3.connect( 'edited', self.col_edited_cb, self.treestore, 3)
    self.cell4 = gtk.CellRendererText()
    self.cell4.connect( 'edited', self.col_edited_cb, self.treestore, 4)
    self.cell5 = gtk.CellRendererText()
    self.cell5.connect( 'edited', self.col_edited_cb, self.treestore, 5)

    # add the cell0 to the column1 and allow it to expand
    self.column0.pack_start(self.cell0, True)
    self.column1.pack_start(self.cell1, True)
    self.column2.pack_start(self.cell2, True)
    self.column3.pack_start(self.cell3, True)
    self.column4.pack_start(self.cell4, True)
    self.column5.pack_start(self.cell5, True)

    # set the cell "text" attribute to column 0 - retrieve text
    # from that column in treestore
    self.column0.add_attribute(self.cell0, 'text', 0)
    self.column1.add_attribute(self.cell1, 'text', 1)
    self.column2.add_attribute(self.cell2, 'text', 2)
    self.column3.add_attribute(self.cell3, 'text', 3)
    self.column4.add_attribute(self.cell4, 'text', 4)
    self.column5.add_attribute(self.cell5, 'text', 5)

    # make it searchable
    self.treeview.set_search_column(0)
    # XXX inutile??

    # Allow sorting on the column # XXX revoir
    self.column1.set_sort_column_id(0) # attention : 0 devient la colonne visible 

    # Allow drag and drop reordering of rows
    #self.treeview.set_reorderable(True)

    # active l'élément sélectionné
    self.window.set_focus(self.treeview)
    self._active_selected()
    #self.treeview.set_flags(gtk.CAN_FOCUS)

    sw = gtk.ScrolledWindow()
    sw.add(self.treeview)
    
    vbox.pack_start(sw, True, True, 0)
    self.window.add(vbox)
    self.window.show_all()


  def _save(self, widget=None):
    """Enregistre les modifications de la librairie dans le fichier utilisateur"""
    iter = self.treestore.get_iter_first()
    li_data = []
    # les dictionnaires ne permettent pas de conserver l'ordre
    li_string = []
    for n in range(self.treestore.iter_n_children(None)):
      self._get_rows(self.treestore, iter, li_data, li_string)
      iter = self.treestore.iter_next(iter)

    # création du xml
    string = '<data pyBar="%s" version="%s"></data>' % (Const.SITE_URL, Const.VERSION)
    xml = ET.ElementTree(ET.fromstring(string))
    root = xml.getroot()
    prec = 0
    prec_node = root
    parents = {0: root}
    for i, key in enumerate(li_string):
      n = len(key.split(':'))
      type = li_data[i][0]
      name = "%s" % li_data[i][1]
      if n == prec: # meme niveau, meme parent
        parent = parents[n-1]
      elif n == prec + 1: # niveau inférieur
        parent = prec_node
        parents[prec] = prec_node
      else:
        parent = parents[n-1]
      if type == True:
        node = ET.SubElement(parent, "group", {"id": name})
      else:
        node = ET.SubElement(parent, "profil", {"id": name})
        masse = "%s" % li_data[i][2].replace(',', '.')
        section = "%s" % li_data[i][3].replace(',', '.')
        igz = "%s" % li_data[i][4].replace(',', '.')
        h = "%s" % li_data[i][5].replace(',', '.')
        node.set("m", masse)
        node.set("s", section)
        node.set("igz", igz)
        node.set("h", h)
      prec_node = node
      prec = n
    function.indent(root)
    self._write_data(xml, root, Const.PROFILFILELIBRARY)
    self.has_changed = False



  def _get_rows(self, model, iter, data, string):
    """Méthode de récupération des lignes du treemodel
    key contient une clé du type 0:1"""
    key = model.get_string_from_iter(iter)
    string.append(key)
    data.append([model.get_value(iter, 0),
		model.get_value(iter, 1),
		model.get_value(iter, 2),
		model.get_value(iter, 3),
		model.get_value(iter, 4),
		model.get_value(iter, 5)
		])
    for n in range(model.iter_n_children(iter)):
      child = model.iter_nth_child(iter, n)
      self._get_rows(model, child, data, string)
   



  def _insert_profil(self, widget):
    iter = self.treestore.insert(None, 0, (False, 'Nouveau', '', '', '', ''))
    self.treeview.get_selection().select_iter(iter)
    path = self.treestore.get_path(iter)
    # move scrollbar
    self.treeview.scroll_to_cell(path)
    self.has_changed = True

  def _insert_group(self, widget):
    iter = self.treestore.insert(None, 0, (True, 'Nouveau groupe', '', '', '', ''))
    self.treeview.get_selection().select_iter(iter)
    path = self.treestore.get_path(iter)
    # move scrollbar
    self.treeview.scroll_to_cell(path)
    self.has_changed = True

  def _change_row(self, widget):
    """Rend éditable ou non les colonnes 1 à + en fonction du type de ligne"""
    #print "_change_row"
    model, iter = self.treeview.get_selection().get_selected()
    if iter: # XXX utiliser self.cell ???
      type = model.get_value(iter, 0)
      cell2 = self.treeview.get_columns()[2].get_cell_renderers()
      cell3 = self.treeview.get_columns()[3].get_cell_renderers()
      cell4 = self.treeview.get_columns()[4].get_cell_renderers()
      cell5 = self.treeview.get_columns()[5].get_cell_renderers()
      if type:
        cell2[0].set_property('editable', False)
        cell3[0].set_property('editable', False)
        cell4[0].set_property('editable', False)
        cell5[0].set_property('editable', False)
      else:
        cell2[0].set_property('editable', True)
        cell3[0].set_property('editable', True)
        cell4[0].set_property('editable', True)
        cell5[0].set_property('editable', True)


  def send_data(self, widget=None):
    """Retourne la liste des caractéristiques d'un profilé"""
    model, iter = self.treeview.get_selection().get_selected()
    resu = None
    if iter:
      resu = []
      for i in range(1, 6):
        if i == 2: continue # masse linéique inutile
        val = model.get_value(iter, i)
        if val == None:
          return None
        resu.append(val)
    return resu


  def _fill_treestore(self, node, parent_iter=None):
    """Méthode récursive pour remplir le treeview"""
    name = node.get('id')
    if node.tag == 'group':
      type = True
      section, m, igz, h = None, None, None, None
    else:
      type = False
      section = node.get('s')
      m = node.get('m')
      igz = node.get('igz')
      h = node.get('h')
    if parent_iter == None:
      parent_iter = self.treestore.append(None, [type, name, m, section, igz, h])
    else:
      parent_iter = self.treestore.append(parent_iter, [type, name, m, section, igz, h])
    if self.selected == name:
      self.path = self.treestore.get_path(parent_iter)
    for elem in node:
      self._fill_treestore(elem, parent_iter)

  def _fill_treestore_cvs(self):
    di = self._read_file()
    print di
    for key, elem in di.items():
      piter = self.treestore.append(None, [True, "Profilé %s" % key, None, None, None, None])
      for profil in elem:
        iter = self.treestore.append(piter, [False, profil[0], profil[1], profil[2], profil[3], profil[7]])


  def _read_file(self): # fonction pour récupérer la liste des éléments depuis un tableur
    f = open('biblio.csv','r')
    lines = f.readlines()
    f.close()
    lines = [i.strip("\n") for i in lines]
    # XXX il y a un espace forcé dans les profils suivants à deux lettres
    profils = {"IPE":[], "IPN":[], "UPE":[], 'UPN':[], 'HE ':[], 'HD ':[], 'HL ':[]}
    for line in lines:
      content = line.split(';')
      key = content[0][0:3]
      profils[key].append(content)
    return profils


def main():
  gtk.main()

if __name__ == "__main__":
  #manager = ProfilManager("IPN 120")
  manager = MaterialManager("AcierC32")
  manager.window.connect("delete_event", manager.main_delete_event)
  main()
