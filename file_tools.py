#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2007 Philippe LAWRENCE
#
# This file is part of pyBar.
#    pyBar is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyBar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyBar; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import os
import sys
import gtk
import Const

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

def set_user_dir():
    """Crée le dossier pour les fichiers utilisateur"""
    path = Const.PATH
    if not os.path.isdir(path):
      import shutil
      os.mkdir(path)
      path = os.path.join(path, Const.DIREXEMPLES)
      os.mkdir(path)
      script_path = module_path()
      src = os.path.join(script_path, Const.DIREXEMPLES)
      try:
        files = os.listdir(src)
      except OSError:
        files = []
      for file in files:
        file_src = os.path.join(src, file)
        if os.path.isdir(file_src):
          continue
        shutil.copy(file_src, path)


# -----------------------------------------------------
#
#    OUVERTURE D'UN NOUVEAU FICHIER
#
#-------------------------------------------------------

def recursive_file_select(path):
    path = file_save(path)
    if path is None:
      return None
    if not path[-4:] == ".dat" :
      path += ".dat"
    if save_as_ok_func(path):
      return path
    else:
      recursive_file_select()

def exit_as_ok_func(filename):
    err = "Enregistrer le fichier '%s'?"  % filename
    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                         gtk.MESSAGE_QUESTION,
                                         gtk.BUTTONS_YES_NO, err)
    dialog.add_button("Oui pour tous", 2)
    dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
    dialog.set_icon_from_file("glade/logo.png")
    result = dialog.run()
    dialog.destroy()
    if result == gtk.RESPONSE_YES:
      return 1
    if result == gtk.RESPONSE_CANCEL:
      return -1
    if result == 2:
      return 2
    return 0

def exit_as_ok_func2(message):
    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                        gtk.MESSAGE_QUESTION,
                                        gtk.BUTTONS_YES_NO, message)
    dialog.set_icon_from_file("glade/logo.png")
    result = dialog.run()
    dialog.destroy()
    if result != gtk.RESPONSE_YES:
      return False
    return True



def save_as_ok_func(filename):
    if filename is None:
      return
    if os.path.exists(filename):
      err = "Ecraser le fichier '%s'?"  % filename
      dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                         gtk.MESSAGE_QUESTION,
                                         gtk.BUTTONS_YES_NO, err)
      dialog.set_icon_from_file("glade/logo.png")
      result = dialog.run()
      dialog.destroy()
      if result != gtk.RESPONSE_YES:
        return False
      return True
    return True


def open_as_ok_func(filename):
    if filename is None:
      return
    if os.path.exists(filename):
      dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
					gtk.MESSAGE_INFO,
					gtk.BUTTONS_OK,
			"Le fichier '%s' est déjà ouvert"  % filename)
      dialog.set_icon_from_file("glade/logo.png")
      result = dialog.run()
      dialog.destroy()


def open_dialog_resol():
    """Fenêtre d'affichage de choix de la résolution"""
    dialog = gtk.Dialog("Exportation Bitmap",
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
			gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.set_icon_from_file("glade/logo.png")

    vbox = gtk.VBox(False, 0)
    vbox.set_border_width(5)

    label = gtk.Label("Choix de la résolution")
    label.set_size_request(-1, 30)
    label.set_alignment(0, 0.5)
    vbox.pack_start(label, False, True, 0)

    adj = gtk.Adjustment(50., 0., 100., 10., 20.0, 0.0)
    spin = gtk.SpinButton(adj, 0, 0)
    spin.set_size_request(30, -1)
    #spin.set_wrap(True) ???
    vbox.pack_start(spin, False, False, 0)

    dialog.vbox.add(vbox)
    dialog.show_all()
    result = dialog.run()
    dialog.destroy()
    if result == gtk.RESPONSE_OK:
      return spin.get_value()
    return False

def open_dialog_bars(bars, selected_bars):
    """Fenêtre d'affichage de sélection des barres actives"""
    dialog = gtk.Dialog("Choix des barres",
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
			gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.set_icon_from_file("glade/logo.png")

    vbox = gtk.VBox(False, 0)
    vbox.set_border_width(5)

    label = gtk.Label("Choix des barres")
    label.set_size_request(-1, 30)
    label.set_alignment(0, 0.5)
    vbox.pack_start(label, False, True, 0)

    buttons = []
    for bar in bars:
      button = gtk.CheckButton(bars[bar])
      buttons.append(button)
      if bar in selected_bars:
        button.set_active(True)
      vbox.pack_start(button, False, False, 0)

    dialog.vbox.add(vbox)
    dialog.show_all()
    result = dialog.run()
    dialog.destroy()
    if result == gtk.RESPONSE_OK:
      keys = bars.keys()
      resu = {}
      for i, button in enumerate(buttons):
       if button.get_active():
         key = keys[i]
         resu[key] = bars[key]
      return resu
    return False


def file_export(path, preselect=None):
#def file_export(preselect=None, path=None):
  """Return selected file name or None"""
  # Create a new file selection widget
  dialog = gtk.FileChooserDialog("Enregistrer sous",
		None, gtk.FILE_CHOOSER_ACTION_SAVE,
		(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
		gtk.STOCK_SAVE, gtk.RESPONSE_OK))
  dialog.set_icon_from_file("glade/logo.png")
  #if not path is None and os.path.isdir(path): 
  dialog.set_current_folder(path)
  #elif os.path.isdir("exemples"): 
  #  script_path = module_path()
  #  dir_exemple = os.path.join(script_path, "exemples")
  #  dialog.set_current_folder(dir_exemple)
  dialog.set_default_response(gtk.RESPONSE_OK)

  filter = gtk.FileFilter()
  filter.set_name("JPEG")
  filter.add_mime_type("image/jpeg")
  filter.add_pattern("*.jpg")
  dialog.add_filter(filter)

  filter = gtk.FileFilter()
  filter.set_name("PNG")
  filter.add_mime_type("image/png")
  filter.add_pattern("*.png")
  dialog.add_filter(filter)

  filter = gtk.FileFilter()
  filter.set_name("SVG")
  filter.add_pattern("*.svg")
  dialog.add_filter(filter)

  # select a specific file 
  if preselect:
    dialog.set_current_name(preselect)
  reponse = dialog.run()
  if reponse == gtk.RESPONSE_OK:
    filter = dialog.get_filter()
    format = filter.get_name()
    file = dialog.get_filename()
    if sys.platform == 'win32':
      file = file.decode('utf-8')
    if format == 'JPEG' and  (not file[-4:] == '.jpg' and not file[-4:] == '.jpeg'):
      file += '.jpg'
    elif format == 'PNG' and  not file[-4:] == '.png':
      file += '.png'
    elif format == 'SVG' and  not file[-4:] == '.svg':
      file += '.svg'
    dialog.destroy()
    return file, format
  dialog.destroy()
  return None

def file_save(path, ext=".dat", preselect=None):
  """Return selected file name or None"""
  # Create a new file selection widget
  dialog = gtk.FileChooserDialog("Enregistrer sous",
		None, gtk.FILE_CHOOSER_ACTION_SAVE,
		(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
		gtk.STOCK_SAVE, gtk.RESPONSE_OK))
  dialog.set_icon_from_file("glade/logo.png")
  dialog.set_current_folder(path)
  #elif os.path.isdir("exemples"): 
  #  script_path = module_path()
  #  dialog.set_current_folder(dir_exemple)
  dialog.set_default_response(gtk.RESPONSE_OK)
  filtre = gtk.FileFilter()
  filtre.set_name("Fichier données")
  filtre.add_pattern("*%s" % ext)
  dialog.add_filter(filtre)
  # select a specific file 
  if preselect:
    dialog.set_current_name(preselect)
  reponse = dialog.run()
  if reponse == gtk.RESPONSE_OK:
    file = dialog.get_filename()
    if sys.platform == 'win32':
      file = file.decode('utf-8')
    file_ext = os.path.splitext(file)[1].lower()
    if not file_ext == ext:
    #if not file[-4:] == ext:
      file += ext
  else:
    file = None
  dialog.destroy()
  return file


# -----------------------------------------------------
#
#    OUVERTURE D'UN FICHIER
#
#-------------------------------------------------------

def file_selection(path):
  """Return selected file name or None"""
  # Create a new file selection widget
  dialog = gtk.FileChooserDialog("Choisir un fichier",
				   None,
				   gtk.FILE_CHOOSER_ACTION_OPEN,
				   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
					gtk.STOCK_OPEN, gtk.RESPONSE_OK))
  dialog.set_default_response(gtk.RESPONSE_OK)
  dialog.set_icon_from_file("glade/logo.png")
  #script_path = os.path.dirname(os.path.realpath(__file__))
  script_path = module_path()
  dir_exemple = os.path.join(script_path, Const.DIREXEMPLES)
  dialog.add_shortcut_folder(dir_exemple)
  if path is None:
    path = dir_exemple
  dialog.set_current_folder(path)
  filtre = gtk.FileFilter()
  filtre.set_name("Fichiers pyBar")
  filtre.add_pattern("*.dat")
  filtre.add_pattern("*.dxf")
  filtre.add_pattern("*.DXF")
  dialog.add_filter(filtre)
  reponse = dialog.run()
  if reponse == gtk.RESPONSE_OK:
    file = dialog.get_filename()
    if sys.platform == 'win32':
      file = file.decode('utf-8')
  else:
    file = None
  dialog.destroy()
  return file



