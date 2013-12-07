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

#import gtk.glade
import cairo
from function import *
import Const
import classPrefs
import math

# -----------------------------------------------------
#
#    CREATION DU PIXMAP POUR L'EQUILIBRE D'UNE BARRE
#
#-------------------------------------------------------

class SigmaDraw:

  def __init__(self, area):
    self.area = area
    # required size: 300px, 300px
    colormap = gtk.gdk.colormap_get_system() 

    bg = color = colormap.alloc_color("white",
			writeable=False, best_match=True)

    area.modify_bg(gtk.STATE_NORMAL, bg)

    self.w, self.h = area.get_size_request()
    self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.w, self.h)
    self.cr = cr = cairo.Context(self.surface)

  def _expose_commun(self):
    """Redessine un fond blanc"""
    cr = self.cr
    cr.save()
    cr.set_source_rgba(1, 1, 1, 1)
    cr.rectangle(0, 0, self.w, self.h)
    cr.fill()
    cr.stroke()
    cr.restore()


  def draw_error(self):
    self._expose_commun()
    cr = self.cr
    cr.set_font_size(12)
    cr.move_to(5, 20)
    cr.show_text("Diagramme non disponible")

  def draw_chart(self, tu_sig_inf, tu_sig_sup, h, v, unit):
    """Gère l'ensemble des fonctions du tracé des contraintes"""
    #print "draw_chart", tu_sig_inf, tu_sig_sup
    (sig_inf, text_sig_inf), (sig_sup, text_sig_sup) = tu_sig_inf, tu_sig_sup
    cr = self.cr
    cr.set_font_size(12)
    self.margin = 50
    self.y_scale = (self.h-2*self.margin) / h
    try:
      self.sig_scale = (Const.SIGMA_SIZE_MAX-2*self.margin) /\
		max(abs(sig_inf), abs(sig_sup))
    except ZeroDivisionError:
      self.sig_scale = None

    self._expose_commun()
    self._draw_axis(h, v, unit)
    self._draw_arrows(sig_inf, sig_sup, text_sig_inf, text_sig_sup, h, v)

  def _draw_axis(self, h, v, unit):
    """Dessine les axes du repère"""
    cr = self.cr
    x0 = self.w / 2
    y0 = self.margin + self.y_scale*v
    self.x0, self.y0 = x0, y0
    self._draw_one_axis(x0, y0, 0)

    cr.move_to(self.w-1.5*self.margin, y0-10)
    cr.show_text(u'\u03C3 (%s)' % unit)
    y0 = self.h / 2
    self._draw_one_axis(x0, y0, -math.pi/2)
    cr.move_to(x0-3, self.margin-25)
    cr.show_text('y')

  def _draw_arrows(self, sig_inf, sig_sup, text_sig_inf, text_sig_sup, h, v):
    """Dessine les flèches de contrainte"""
    if self.sig_scale is None or math.isinf(self.sig_scale):
      return
    cr = self.cr
    cr.save()
    cr.set_source_rgb(1, 0, 0)
    y = 0
    n = 8 # n arrows
    dy = h / n
    sig0 = sig_sup*self.sig_scale
    for i in range(n+1):
      dsig = (sig_inf-sig_sup)*i*dy/h*self.sig_scale
      sig = dsig+sig0
      self._draw_arrow(self.x0, sig, y*self.y_scale+self.margin)
      y += dy
    self._draw_attache(sig_inf, sig_sup, h, v)
    self._draw_legend(sig_inf, sig_sup, text_sig_inf, text_sig_sup, h, v)
    cr.restore()

  def _draw_arrow(self, x0, sig, y):
    """Dessine une flèche de contrainte"""
    cr = self.cr
    cr.save()
    cr.set_line_width(1)
    cr.translate(x0, y)
    dx = sig < 0 and -2 or 2
    cr.move_to(dx, 0)
    cr.rel_line_to(sig-2*dx, 0)
    cr.stroke()

    if abs(sig) <= 5:
      cr.restore()
      return

    if sig > 0:
      d = 5
    else:
      d = -5
    # arrow
    cr.move_to(sig-dx, 0)
    cr.rel_line_to(-d, -d)
    cr.rel_line_to(0, 2*d)
    cr.close_path()
    cr.fill()
    cr.stroke()
    cr.restore()

  def _draw_attache(self, sig_inf, sig_sup, h, v):
    """Dessine la ligne qui relie sigma sup et inf"""
    cr = self.cr
    cr.save()
    cr.set_line_width(1)
    px = max(cr.device_to_user_distance(1, 1))
    cr.set_dash([3 * px], 0)
    cr.translate(self.x0, self.y0)
    cr.move_to(sig_sup*self.sig_scale, -v*self.y_scale)
    cr.line_to(sig_inf*self.sig_scale, (h-v)*self.y_scale)
    cr.stroke()
    cr.restore()

  def _draw_legend(self, sig_inf, sig_sup, text_sig_inf, text_sig_sup, h, v):
    """Ecrit les valeurs des contraintes"""
    cr = self.cr
    cr.save()
    cr.translate(self.x0, self.y0)
    #text_sig_sup = PrintValue(sig_sup)
    x_bearing, y_bearing, width, height = cr.text_extents(text_sig_sup)[:4]
    if sig_sup >= 0:
      cr.move_to(sig_sup*self.sig_scale+5, -v*self.y_scale+height/2)
    else:
      cr.move_to(sig_sup*self.sig_scale-width-5, -v*self.y_scale+height/2)
    cr.show_text(text_sig_sup)
    #text_sig_inf = PrintValue(sig_inf)
    x_bearing, y_bearing, width, height = cr.text_extents(text_sig_inf)[:4]
    if sig_inf >= 0:
      cr.move_to(sig_inf*self.sig_scale+5, (h-v)*self.y_scale)
    else:
      cr.move_to(sig_inf*self.sig_scale-width-5, (h-v)*self.y_scale)
    cr.show_text(text_sig_inf)

    # valeur en G
    sig_G = ((h-v)*sig_sup+v*sig_inf)/h
    if abs(sig_G) > max(abs(sig_sup), abs(sig_inf))/1e4:
      text_sig_G = PrintValue(sig_G)
      x_bearing, y_bearing, width, height = cr.text_extents(text_sig_G)[:4]
      if sig_G > 0:
        cr.move_to(sig_G*self.sig_scale+5, height+5)
      else:
        cr.move_to(sig_G*self.sig_scale-width-5, height+5)
      cr.show_text(text_sig_G)
    cr.restore()

  def _draw_one_axis(self, x, y, angle):
    """Dessine un axe de centre x, y avec flèche"""
    cr = self.cr
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    cr.set_line_width(1)
    dx = (self.w - 2 * self.margin)/2. + 15
    a = 6
    #print dx
    cr.move_to(-dx, 0)
    cr.rel_line_to(2*dx, 0)
    cr.stroke()
    cr.move_to(dx-a, -a)
    cr.rel_line_to(a+1, a)
    cr.rel_line_to(-a-1, a)
    cr.close_path()
    cr.fill()
    cr.stroke()
    cr.restore()

#---------------------------------------------------------------
#
#        FENETRE D'AFFICHAGE DES SOLLICITATIONS SUR UNE BARRE
#
#---------------------------------------------------------------

class ResuParBarre:

  def __init__(self, parent, barre, n_case):

# trop de références: study, parent, rdm, drawing
    self.parent = parent
    tab = parent.active_tab
    drawing = tab.active_drawing
    try:
      self.drawing = drawing.parent
    except AttributeError:
      self.drawing = drawing
    id_study = self.drawing.id_study
    study = parent.studies[id_study]
    self.study = study
    self.rdm = study.rdm

    self.Char = self.rdm.GetCharByNumber(n_case)
    self.barre = barre
    self.h = None
    builder = self.builder = gtk.Builder()
    builder.add_from_file("glade/w3.glade")
    self.window = builder.get_object("window3")
    self.window.show()
    self._ini_window()
    hbox = builder.get_object("label1").get_parent()
    self.combobox = gtk.combo_box_new_text()
    self.combobox.show()
    hbox.pack_start(self.combobox, False, False)
    self.label = builder.get_object("label3")
    self.content = builder.get_object("label4")
    self.check = builder.get_object("check1")
    self._fill_combobox()
    self.combobox.connect('changed', self.on_combobox1_changed)
    #self.set_active_barre()
    builder.connect_signals(self)
    self.area = builder.get_object("area")
    #self.area.set_size_request(300, 300)
    self.area.connect("expose-event", self._expose_event)
    style = self.area.get_style()
    self.gc = style.fg_gc[gtk.STATE_NORMAL]
    self._chart = SigmaDraw(self.area)

    # connexion du bouton 
    spin = self.spin = builder.get_object("spinbutton1")
    self.on_set_unit()
    spin.connect('value-changed', self._get_point_value)
    self._get_point_value()

  def on_configure_event(self, widget, event):
    """Gère les évènements correspondant au redimensionnement de la fenetre"""
    #print "ResuParBarre::_configure_event"
    size = self.window.get_size()
    self._w = size[0]
    self._h = size[1]


  def _expose_event(self, area, event):
    #print "expose"
    x, y, width, height = event.area
    if self.h is None:
      self._draw_error()
    else:
      self._draw_chart(self.sig_inf, self.sig_sup, self.h, self.v, self.sig_unit)
    #self.area.window.draw_drawable(self.gc, self._chart.pixmap, 
#				x, y, x, y, width, height)
    cr = area.window.cairo_create()
    cr.set_source_surface(self._chart.surface, 0, 0)
    cr.paint()

  def _ini_window(self):
    """Lecture des préférence pour la fenetre"""
    self.UP = classPrefs.UserPrefs()
    try:
      self._w, self._h = self.UP.get_w3_size()
    except:
      self._w, self._h = 300, 700
    self.window.resize(self._w, self._h)

  def new_rdm_object(self, drawing, study, Char):
    """Lance une mise à jour de la fenetre à partir d'un nouvel objet rdm"""
    if not Char is None:
      self.Char = Char
    #print "ResuParBarre::new_rdm_object"
    self.rdm = study.rdm
    self.study = study

    try:
      self.drawing = drawing.parent
    except AttributeError:
      self.drawing = drawing
    self.on_set_unit()
    self._fill_combobox()
    self.do_calculate()

  def set_w3_sensitive(self, is_true=True):
    """Rend la fenetre entière insensible""" 
    self.window.set_sensitive(is_true)

  def on_window_destroy(self, widget, event):
    self.UP.save_w3_config(self._w, self._h)
    del(self.parent.w3)

  def _destroy(self, widget):
    self.window.destroy()

  def set_active_barre(self):
    """Actualise la valeur active dans le combobox de la fenetre résultats
    quand on clique sur une barre de la fenetre principale"""
    index = 0
    for barre in self.liBarre:
      if barre == self.barre:
        self.combobox.set_active(index)
      index += 1

  def _fill_combobox(self):
    """Actualise l'affichage du combobox en fonction du nombre de barre"""
    #print "_fill_combobox"
    barres = self.rdm.struct.GetBars()
    fill_elem_combo(self.combobox, barres, self.barre)

  def on_combobox1_changed(self, widget):
    """Effectue les nouveaux calculs lorsqu'une barre est choisie 
    dans le combobox"""
    #print "on_combobox1_changed"
    model = self.combobox.get_model()
    index = self.combobox.get_active()
    if not index == -1:
      barre = model[index][0]
      self.barre = self.drawing.s_bar = barre
    self.on_set_unit()
    self.do_calculate()


  def on_set_unit(self, widget=None):
    """Met à jour les boutons lors d'un clic sur le changement d'unité des longueur"""
    #print "on_set_unit"
    if widget is None:
      widget = self.check
    barre = self.barre
    struct = self.rdm.struct
    unit_L = self.study.get_unit_name('L')
    if not barre in struct.Barres:
      return
    b = self.spin
    value = b.get_value()
    l = struct.Lengths[barre]/struct.units['L']
    if widget.get_active():
      text = "Distance de l'origine en %s" % unit_L
      text2 = "Distance en %s" % unit_L
      d = l/100
      value = value*d
      b.set_increments(d, 5*d)
      b.set_digits(2)
      b.set_range(0, l)
    else:
      text = "Distance de l'origine en %"
      text2 = "Distance en %"
      value = value/l*100
      b.set_increments(1, 5)
      b.set_digits(0)
      b.set_range(0, 100)
    b.set_value(value)
    self.label.set_text(text)
    label = widget.get_children()[0]
    label.set_text(text2)

  def _get_point_value(self, widget=None):
    """Lance le calcul des sollicitations en un point d'une barre
    Dessine un point sur la barre dans la fenetre w1"""
    #print "ResuParBarre::_get_point_value"
    if self.barre is None:
      return
    u = self.do_calculate()
    drawing = self.drawing
    tab = self.parent.active_tab
    area = tab.area
    rdm = self.rdm
    struct = rdm.struct
    tab.new_surface(tab.area_w, tab.area_h)
    cr = tab.cr
    drawing.push_w3_group(struct, cr, self.barre, u)
    tab.paint_all_struct(cr)
    x, y, w, h = tab.mapping.box[drawing.id]
    rect = gtk.gdk.Rectangle(x, y, w, h)
    tab.expose_event(area, rect)

  def do_calculate(self):
    #print "w3::do_calculate"
    barre = self.barre
    if barre is None:
      return None
    rdm = self.rdm
    struct = rdm.struct
    units = struct.units
    unit_F = self.study.get_unit_name('F')
    unit_L = self.study.get_unit_name('L')
    # en cas de changement dans les barres
    self.window.set_title("Barre %s - %s" % (barre, self.Char.name))
    self.set_w3_sensitive()
    l = struct.Lengths[self.barre]
    charQu = self.Char.charBarQu.get(barre, {})
    charFp = self.Char.charBarFp.get(barre, {})
    charTri = self.Char.charBarTri.get(barre, None)
    if self.check.get_active():
      u = self.spin.get_value()*units['L']
    else:
      u = self.spin.get_value()/100*l
    str_u = PrintValue(u, units['L'])
    N = rdm.NormalPoint(self.Char, barre, u, charQu, charFp, charTri, rdm.conv)
    V = rdm.TranchantPoint(self.Char, barre, u, charQu, charFp, charTri, rdm.conv)
    mf = rdm.MomentPoint(self.Char, barre, u, charQu, charFp, charTri, rdm.conv)
    sigma_is_valid = False
    if barre in struct.Sections:
      S = struct.Sections[barre]
    else:
      S = struct.Sections["*"]
    if barre in struct.MQua:
      I = struct.MQua[barre]
    else:
      I = struct.MQua["*"]
    if barre in struct.Section_H:
      H = struct.Section_H[barre]
    elif "*" in struct.Section_H:
      H = struct.Section_H["*"]
    else:
      H = None
    if barre in struct.Section_v:
      v = struct.Section_v[barre]
    elif "*" in struct.Section_v:
      v = struct.Section_v["*"]
    else:
      v = None
      
    if not H is None and not v is None: 
      sigma_is_valid = True
      sig_sup = N/S - mf*v/I
      sig_inf = N/S + mf*(H-v)/I
      text_sig_sup = PrintValue(sig_sup, units['C'])
      text_sig_inf = PrintValue(sig_inf, units['C'])
      unit_C = self.study.get_unit_name('C')
      #print "unit_C=", unit_C
    N = PrintValue(N, units['F'])
    V = PrintValue(V, units['F'])
    mf = PrintValue(mf, units['F']*units['L'])
    #fleche = PrintValue(rdm.DefoPoint(barre, u))
    fleche = PrintValue(rdm.FlechePoint(self.Char, barre, u)[1], units['L'])
    dep = rdm.DepPoint(self.Char, barre, u)
    depx = PrintValue(dep[0], units['L'])
    depy = PrintValue(dep[1], units['L'])
    text = "<b>Résultats pour la barre: %s</b>\n\nLongueur initiale: %s %s\n" % (barre, PrintValue(l, units['L']), unit_L)
    text += "Position sur la barre x = %s %s" % (str_u, unit_L)
    text += "\nValeurs des sollicitations:\nN = %s %s" % (N, unit_F)
    text += "\nV = %s %s" % (V, unit_F)
    text += "\nM<sub>z</sub> = %s %s.%s" % (mf, unit_F, unit_L)
    text += "\n\nDéplacement du point:"
    text += "\nsuivant x: %s %s" % (depx, unit_L)
    text += "\nsuivant y: %s %s" % (depy, unit_L)
    text += "\nFlèche = %s %s" % (fleche, unit_L)
    text += "\n<b>Diagramme contraintes normales</b>"
    label = self.content
    label.set_text(text)
    label.set_use_markup(True)

    if sigma_is_valid: 
      self.h = H
      self.v = v
      self.sig_inf, self.sig_sup = (sig_inf, text_sig_inf), (sig_sup, text_sig_sup)
      self.sig_unit = unit_C
    else:
      self.h = None
    self.area.queue_draw()
    return u

  def _draw_error(self):
    """Ecrit le message "Diagramme indisponible" """
    self._chart.draw_error()

  def _draw_chart(self, sig_inf, sig_sup, h, v, unit):
    if not hasattr(self, '_chart'):
      return
    self._chart.draw_chart(sig_inf, sig_sup, h, v, unit)


