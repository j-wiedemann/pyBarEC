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

import gtk
import gobject
#from function import *

class Singleton(object):
  def __new__(cls, *args, **kwargs):
    if '_inst' not in vars(cls):
      cls._inst = object.__new__(cls, *args, **kwargs)
    return cls._inst


class Message(Singleton):

  def __init__(self):
    # ne rien mettre ici
    pass

  def set_message(self, content):
    """Formate le message (ne conserve que la première ligne) et lance son affichage si nécessaire"""
    #print "set_message", content
    if self._content == content:
      return
    if content is None:
      self._content = None
    else:
      text, ind = content
      pos = text.find('\n')
      if not pos == -1:
        text = text[:pos]
      self._content = (text, ind)
    if self.has_changed is False:
      self.has_changed = True
      gobject.idle_add(self._print_message)

  def ini_message(self, box):
    self.has_changed = False
    self.box = box
    self._content = None

  def _print_message(self):
    """type = 0 : error; 1 : warning; 2 : info"""
    #print "_print_message", self._content
    self.has_changed = False
    box = self.box
    for elem in box.get_children():
      box.remove(elem)
    if self._content is None:
      return
    text, type = self._content

    # icone 
    image = gtk.Image()
    if type == 0:
      image.set_from_stock(gtk.STOCK_STOP, gtk.ICON_SIZE_BUTTON)
    elif type == 1:
      image.set_from_stock(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_BUTTON)
    elif type == 2:
      image.set_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_BUTTON)
    elif type == 3:
      image.set_from_stock(gtk.STOCK_APPLY, gtk.ICON_SIZE_BUTTON)
    image.show()
    box.pack_start(image, False)
    box.set_spacing(10)
    label = gtk.Label()
    label.set_text(text)
    label.set_use_markup(True)
    label.show()
    box.pack_start(label, False)


class Dialog:

  def __init__(self, errors):
    text = '\n'.join(errors)
    if text == '':
      return
    dialog = gtk.Dialog("Erreur", None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
    dialog.set_icon_from_file("glade/logo.png")
    box = dialog.get_content_area()
    box.set_border_width(80)
    hbox = gtk.HBox()
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(image, False, False, 0)

    label = gtk.Label(text)
    label.set_padding(20, 20)
    label.show()
    hbox.pack_start(label, False, False, 0)
    hbox.show_all()
    box.add(hbox)
    result = dialog.run()
    dialog.destroy()



