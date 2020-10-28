import pygame as pg
from random import randint
pg.display.init()

def toRGB(i):
    r = i>>16
    g = (i-(r<<16))>>8
    b = (i-((r<<16)+(g<<8)))
    return (r,g,b)
def fromRGB(clr):
    r = clr[0]
    g = clr[1]
    b = clr[2]
    return (r<<16) + (g<<8) + (b)

def toon(img):
    d = img
    d = d.convert(8)
    d = d.convert(24)
    return d

def scanline(img):
    d = img
    size = d.get_size()
    w = size[0]
    h = size[1]
    for i in range(h/8):
        pg.draw.rect(d,(0,0,0),(0,i*8,w,2))
    return d

def blur(img):
    i=4
    d = img
    size = d.get_size()
    w = size[0]
    h = size[1]
    d = pg.transform.smoothscale(d,(w/i,h/i))
    d = pg.transform.smoothscale(d,(w,h))
    return d
def pixelize(img):
    i=4
    d = img
    size = d.get_size()
    w = size[0]
    h = size[1]
    d = pg.transform.scale(d,(w/i,h/i))
    d = pg.transform.scale(d,(w,h))
    return d

def dark(img):
    d = img
    size = d.get_size()
    newd = pg.Surface(size,pg.SRCALPHA)
    newd.fill((0,0,0,128))
    d.blit(newd,(0,0))
    return d
def bright(img):
    d = img
    size = d.get_size()
    newd = pg.Surface(size,pg.SRCALPHA)
    newd.fill((255,255,255,128))
    d.blit(newd,(0,0))
    return d
