#!/usr/bin/env python
#coding: utf-8
"""
We will implement a class to represent two-dimensional vectors—that is Euclidean vectors
like those used in math and physics
"""
from math import hypot

class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Vector(%r, %r)' %(self.x, self.y)
    def __abs__(self):
        return hypot(self.x, self.y)
    def __bool__(self):
        return bool(abs(self))
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)
    def __mul__(self, scala):
        return Vector(self.x*scala, self.y*scala)

