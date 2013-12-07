#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test de la vitesse d'accès à des valeurs dans un dictionnaire

# Conclusion : écarter la méthode get !!!
# Préferer : if key in di:

import cProfile
class A(object):
  """Classes contenant une légende et ses attributs"""
  def __init__(self, x, y, text):
    self.text = text
    self.x = x
    self.y = y

li = []
for i in range(10):
  a = A(0, 0, 'test')
  li.append(a)

di = {}
for i in range(10):
  a = A(0, 0, 'test')
  di[(a.x, a.y)] = a

n = 1000000
def test(li):
  for i in range(n):
    for a in li:
      if a.x == 1 and a.y == 1:
        pass

def test2(di):
  for i in range(n):
    for tu, a in di.items():
      if tu[0] == 1 and tu[1] == 1:
        pass


#cProfile.run('test(li)') #  1.431 CPUs
cProfile.run('test2(di)') # # 3,01 CPUs
#cProfile.run('test3(di2)') # 0,476 CPUs
#cProfile.run('test4(di2)') # #  1,89 CPUs
