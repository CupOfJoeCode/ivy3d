import pygame as pg
from pygame import gfxdraw
from math import *
import shapes
from sceneFile import scene,world,player
from random import randint
import guibuttons
from time import sleep
from glob import glob
import easygui
pg.init()

VERSION = "Beta 0.2"



w = 800
h = 600

zscale = 400.0

translate = (w/2,h/2)

d = pg.display.set_mode((w,h))
pg.display.set_caption("Ivy3d v " + VERSION)
pg.display.set_icon(pg.image.load("favicon.png"))

running = True

#Projects 3d Point To 2d Point
def project(point):
    x = point[0]
    y = point[1]
    z = point[2]
    return (x*(2**(z/zscale)) + translate[0],-y*(2**(z/zscale)) + translate[1])

def scaleVector(vec,vec2):
    a = list(vec)
    for i in range(0,len(a)):
        a[i]*=vec2[i]
    return tuple(a)

def translateVector(vec,vec2):
    a = list(vec)
    for i in range(0,len(a)):
        a[i]+=vec2[i]
    return tuple(a)

#wip
def rotateVector(vec,aa):
    x = vec[0]
    y = vec[1]
    z = vec[2]
    
    x *= sin(aa- (x/(pi/2)  ))
    y = y
    z *= cos(aa- (z/(pi/2)))

    return (x,y,z)

def getNormal(vec1,vec2,vec3):
    u = (vec2[0] - vec1[0],vec2[1] - vec1[1],vec2[2] - vec1[2])
    v = (vec3[0] - vec1[0],vec3[1] - vec1[1],vec3[2] - vec1[2])
    nx = (u[1]*v[2]) - (u[2]*v[1])
    ny = (u[2]*v[0]) - (u[0]*v[2])
    nz = (u[0]*v[1]) - (u[1]*v[0])

    return (nx,ny,nz)

def vectorPos(a):
    x = 0
    y = 0
    z = 0
    for vec in a:
        x+=vec[0]
        y+=vec[1]
        z+=vec[2]
    x = x / len(a)
    x = y / len(a)
    x = z / len(a)

    return (x,y,z)


def getCull(vec):
    x = 0
    y = 0
    z = 0
    if vec[0] != 0: x = int(vec[0] / abs(vec[0]))
    if vec[1] != 0: y = int(vec[1] / abs(vec[1]))
    if vec[2] != 0: z = int(vec[2] / abs(vec[2]))

    return (x,y,z)




            

def render(s):
    zBuffer = []
    for mesh in s:
        
        for tris in meshes[mesh["shape"]]:
            pos = mesh["position"]
            scl = mesh["scale"]
            point1 = translateVector(scaleVector(tris[0],scl),  pos   )
            point2 = translateVector(scaleVector(tris[1],scl),  pos   )
            point3 = translateVector(scaleVector(tris[2],scl),  pos   )

            
            

            facePos = vectorPos([point1,point2,point3])
            rnd = True
            
            normal = getNormal(point1,point2,point3)
            normal = float((normal[0] + normal[1] + normal[2])/3.0)/300.0
            

            shade = float(    max(min(255 - abs(normal),255),1)    )

            color = mesh["material"]["color"]


            r = color[0]
            g = color[1]
            b = color[2]

            r = int(r / (255/shade))
            g = int(g / (255/shade))
            b = int(b / (255/shade))

            color = (r,g,b)


            zBuffer.append([point1,point2,point3,facePos,color,mesh["material"]["wire"],mesh["material"]["map"]])
            
            
            '''
            point1 = project(point1)
            point2 = project(point2)
            point3 = project(point3)
            '''


            
            
            '''
            pg.draw.polygon(d,color,(point1,point2,point3))
            if(mesh["material"]["wire"]):
                pg.draw.line(d,(0,0,0), point1,point2 )
                pg.draw.line(d,(0,0,0), point2,point3 )
                pg.draw.line(d,(0,0,0), point3,point1 )
            '''
    for j in range(0,len(zBuffer)):
        for i in range(0,len(zBuffer)-1):
            zPos1 = [zBuffer[i][0],zBuffer[i][1],zBuffer[i][2]]
            zPos2 = [zBuffer[i+1][0],zBuffer[i+1][1],zBuffer[i+1][2]]
            zPos1 = vectorPos(zPos1)[2]
            zPos2 = vectorPos(zPos2)[2]
            if zPos1 > zPos2:
                store = zBuffer[i]
                zBuffer[i] = zBuffer[i+1]
                zBuffer[i+1] = store
   
    for i in range(0,len(zBuffer)):
        tri = zBuffer[i]
        gfxdraw.aapolygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])) , tri[4])
        if(not(tri[5])):
            if(tri[6] == "none"):
                gfxdraw.filled_polygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])) , tri[4])
            else:
                imgMap = pg.image.load(tri[6])
                offs = project(tri[0])
                sz = imgMap.get_size()
                if( min(project(tri[0])[0] , project(tri[1])[0] , project(tri[2])[0]  ) >= 0     ):
                    if( max(project(tri[0])[0] , project(tri[1])[0] , project(tri[2])[0]  ) <= w     ):
                        if( min(project(tri[0])[1] , project(tri[1])[1] , project(tri[2])[1]  ) >= 0     ):
                            if( max(project(tri[0])[1] , project(tri[1])[1] , project(tri[2])[1]  ) <= h     ):
                                gfxdraw.textured_polygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])),imgMap, int(offs[0]) % sz[0] , int(h-offs[1])  % sz[1] )

        
    
    


    




def col(mesh1,ss):
    isc = False
    fric = 1
    for msh in ss:
        if mesh1 != msh:
            pos1 = mesh1["position"]
            scl1 = mesh1["scale"]
            pos2 = msh["position"]
            scl2 = msh["scale"]

            if (pos1[0] > pos2[0] - (scl1[0] + scl2[0]) and pos1[0] < pos2[0] + (scl1[0] + scl2[0]) ) and (pos1[1] > pos2[1] - (scl1[1] + scl2[1]) and pos1[1] < pos2[1] + (scl1[1] + scl2[1]) ) and (pos1[2] > pos2[2] - (scl1[2] + scl2[2]) and pos1[2] < pos2[2] + (scl1[2] + scl2[2]) ):
                isc = True
                fric = msh["physics"]["friction"]

    return [isc,fric]


def simulate(s,w,k):
    scn = s
    for mesh in scn:
        if(mesh["physics"]["rigidBody"]):
            if(mesh["physics"]["control"]):
                maxSpeed = player["maxSpeed"]
                accel = player["accel"]
                jumpS = player["jumpStrength"]
                if(k[pg.K_w]):
                    vel = mesh["physics"]["velocity"]
                    mesh["physics"]["velocity"] = (vel[0],vel[1], max(-maxSpeed,vel[2]-accel) )
                if(k[pg.K_s]):
                    vel = mesh["physics"]["velocity"]
                    mesh["physics"]["velocity"] = (vel[0],vel[1], min(maxSpeed,vel[2]+accel) )
                if(k[pg.K_a]):
                    vel = mesh["physics"]["velocity"]
                    mesh["physics"]["velocity"] = (max(-maxSpeed,vel[0]-accel),vel[1], vel[2] )
                if(k[pg.K_d]):
                    vel = mesh["physics"]["velocity"]
                    mesh["physics"]["velocity"] = (min(maxSpeed,vel[0]+accel),vel[1], vel[2] )
                


            vel = mesh["physics"]["velocity"]
            mesh["physics"]["velocity"] = (vel[0],vel[1]-w["gravity"], vel[2])
            pos = mesh["position"]
            vel = mesh["physics"]["velocity"]
            mesh["position"] = (pos[0],pos[1]+vel[1],pos[2])
            cl = col(mesh,scn)
            if cl[0]:
                pos = mesh["position"]
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0],pos[1]-vel[1],pos[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0] * (1-cl[1]),-vel[1] * bnc,vel[2] * (1-cl[1]))
                if(k[pg.K_SPACE] and mesh["physics"]["control"]):
                    vel = mesh["physics"]["velocity"]
                    mesh["physics"]["velocity"] = (vel[0],jumpS, vel[2] )

            pos = mesh["position"]
            vel = mesh["physics"]["velocity"]
            mesh["position"] = (pos[0]+vel[0],pos[1],pos[2])
            cl = col(mesh,scn)
            if cl[0]:
                pos = mesh["position"]
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0]-vel[0],pos[1],pos[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0]*bnc,vel[1],vel[2])

            pos = mesh["position"]
            vel = mesh["physics"]["velocity"]
            mesh["position"] = (pos[0],pos[1],pos[2]+vel[2])
            cl = col(mesh,scn)
            if cl[0]:
                pos = mesh["position"]
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0],pos[1],pos[2]-vel[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0],vel[1],vel[2]*bnc)



    return scn
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def textdisplay(text,x,y,fff,ffs):
    largeText = pg.font.Font(fff,ffs)
    TextSurf, TextRect = text_objects(text, largeText)
    
    d.blit(TextSurf, (x,y))


class GUIButton():
    def __init__(self,xpos,ypos,textstr):
        self.x = xpos
        self.y = ypos
        self.w = 1
        self.h = 1
        self.text = textstr
        self.clicked = False
    def render(self,mx,my,mp):
        fnt = 'opensans.ttf'
        fntSize = 16
        lText = pg.font.Font(fnt,fntSize)
        tSurf, tRect = text_objects(self.text, lText)
        tSize = tSurf.get_size()
        self.w = tSize[0]+2
        self.h = tSize[1]+2
        pg.draw.rect(d,(0,0,0),(self.x,self.y,self.w,self.h) )
        if (mx > self.x and mx < self.x + self.w) and (my > self.y and my < self.y + self.h):
            if(mp):
                pg.draw.rect(d,(127,127,127),(self.x+1,self.y+1,self.w-2,self.h-2) )
                self.clicked = True
            else:
                pg.draw.rect(d,(200,200,200),(self.x+1,self.y+1,self.w-2,self.h-2) )
                self.clicked = False
        else:
            self.clicked = False
            pg.draw.rect(d,(255,255,255),(self.x+1,self.y+1,self.w-2,self.h-2) )
        textdisplay(self.text,self.x,self.y,fnt,fntSize)
        
def changeObject():
    sel+=1
    if(sel > len(scene)-1):
        sel = 0

def gui(mouseX,mouseY,mousePressed,msh,idx):
    nams = ["Cube","Pyramid","Octahedron","Sphere"]
    fnt = 'opensans.ttf'
    fntSize = 16
    buttons = guibuttons.buttons
    
    pg.draw.rect(d,(0,0,0),(0,0,256,h))

    
    pg.draw.rect(d,(255,255,255),(0,0,255,h))

    textdisplay("Object: " + str(nams[msh["shape"]]) + ' ' + str(idx),w - 200,8,fnt,fntSize )
    textdisplay("Position: " + str(msh["position"]),w - 200,28,fnt,fntSize )
    textdisplay("Scale: " + str(msh["scale"]),w - 200,48,fnt,fntSize )
    textdisplay("Color: " + str(msh["material"]["color"]  ),w - 200,68,fnt,fntSize )

    textdisplay("IsRigidBody: " + str(msh["physics"]["rigidBody"]  ),w - 200,88,fnt,fntSize )
    textdisplay("CharControl: " + str(msh["physics"]["control"]  ),w - 200,108,fnt,fntSize )

    textdisplay("Bounciness: " + str(msh["physics"]["bounce"]  ),w - 200,128,fnt,fntSize )

    textdisplay("Friction: " + str(msh["physics"]["friction"]  ),w - 200,148,fnt,fntSize )

    textdisplay("Texture: " + str(msh["material"]["map"]  ),w - 200,168,fnt,fntSize )

    textdisplay("Wireframe: " + str(msh["material"]["wire"]  ),w - 200,188,fnt,fntSize )

    for i in buttons:
        btn = GUIButton(i["x"],i["y"],i["name"] )
        btn.render(mouseX,mouseY,mousePressed)
        i["pressed"] = btn.clicked

    return buttons
    
    

meshes = shapes.meshes


keys = []
for i in range(0,1024):
    keys.append(False)

a = 0

sim = False
sel = 0

buff = ""


mouse = {
    "x":0,
    "y":0,
    "pressed":False
}

mapList = ["none"] + glob("maps/*.png")
mapT = 0

while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.MOUSEMOTION:
            ms = pg.mouse.get_pos()
            mouse["x"] = ms[0]
            mouse["y"] = ms[1]
        if e.type == pg.MOUSEBUTTONDOWN:
            mouse["pressed"] = True
        if e.type == pg.MOUSEBUTTONUP:
            mouse["pressed"] = False

        if e.type == pg.KEYDOWN:
            keys[e.key] = True
            if(e.key == pg.K_p):
                
                
                if(not(sim)):
                    buff = str(scene)
                else:
                    scene = eval(buff)
                sim = not(sim)
            
            
                    
        if e.type == pg.KEYUP:
            keys[e.key] = False
    d.fill(world["background"])


    
    if sim:
        scene = simulate(scene,world,keys)
        
    
    

    render(scene)
    if(not(sim)):
        pos = scene[sel]["position"]
        pg.draw.line(d,(255,0,0),project(pos),project(  (pos[0]+25,pos[1],pos[2])  ) ,4)
        pg.draw.line(d,(0,255,0),project(pos),project(  (pos[0] ,pos[1]+25,pos[2])  ) ,4)
        pg.draw.line(d,(0,0,255),project(pos),project(  (pos[0] ,pos[1],pos[2]+25)  ) ,4)


        guiEvents = gui(mouse["x"],mouse["y"],mouse["pressed"],scene[sel],sel)

        if(guiEvents[0]["pressed"]):
            sel+=1
            if(sel > len(scene)-1):
                sel = 0
            sleep(0.1)
        if(guiEvents[1]["pressed"]):
            scene[sel]["shape"]+=1
            if(scene[sel]["shape"] > len(shapes.meshes)-1):
                scene[sel]["shape"] = 0
            sleep(0.1)

        name = "position"
        if(guiEvents[2]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0]-4,pos[1],pos[2])
        if(guiEvents[3]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0]+4,pos[1],pos[2])
        if(guiEvents[4]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1]-4,pos[2])
        if(guiEvents[5]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1]+4,pos[2])
        if(guiEvents[6]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1],pos[2]-4)
        if(guiEvents[7]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1],pos[2]+4)

        name = "scale"
        
        if(guiEvents[8]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0]-4,pos[1],pos[2])
        if(guiEvents[9]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0]+4,pos[1],pos[2])
        if(guiEvents[10]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1]-4,pos[2])
        if(guiEvents[11]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1]+4,pos[2])
        if(guiEvents[12]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1],pos[2]-4)
        if(guiEvents[13]["pressed"]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1],pos[2]+4)


        if(guiEvents[14]["pressed"]):
            pos = scene[sel]["material"]["color"]
            scene[sel]["material"]["color"] = (pos[0]-4,pos[1],pos[2])
        if(guiEvents[15]["pressed"]):
            pos = scene[sel]["material"]["color"]
            scene[sel]["material"]["color"] = (pos[0]+4,pos[1],pos[2])
        if(guiEvents[16]["pressed"]):
            pos = scene[sel]["material"]["color"]
            scene[sel]["material"]["color"] = (pos[0],pos[1]-4,pos[2])
        if(guiEvents[17]["pressed"]):
            pos = scene[sel]["material"]["color"]
            scene[sel]["material"]["color"] = (pos[0],pos[1]+4,pos[2])
        if(guiEvents[18]["pressed"]):
            pos = scene[sel]["material"]["color"]
            scene[sel]["material"]["color"] = (pos[0],pos[1],pos[2]-4)
        if(guiEvents[19]["pressed"]):
            pos = scene[sel]["material"]["color"]
            scene[sel]["material"]["color"] = (pos[0],pos[1],pos[2]+4)

        if(guiEvents[20]["pressed"]):
            scene[sel]["physics"]["rigidBody"] = not(scene[sel]["physics"]["rigidBody"])
            sleep(0.1)
        if(guiEvents[21]["pressed"]):
            scene[sel]["physics"]["control"] = not(scene[sel]["physics"]["control"])
            sleep(0.1)
        if(guiEvents[22]["pressed"]):
            scene[sel]["physics"]["bounce"]-= 0.01
        if(guiEvents[23]["pressed"]):
            scene[sel]["physics"]["bounce"]+= 0.01

        if(guiEvents[24]["pressed"]):
            scene[sel]["physics"]["friction"]-= 0.01
        if(guiEvents[25]["pressed"]):
            scene[sel]["physics"]["friction"]+= 0.01

        if(guiEvents[26]["pressed"]):
            mapT+=1
            if(mapT >= len(mapList)):
                mapT = 0
            scene[sel]["material"]["map"] = mapList[mapT]
            sleep(0.1)
        if(guiEvents[27]["pressed"]):
            aaa = {
                "shape":0,

                "position":(0,0,0),
                "scale":(25,25,25),
                "material":{

                    "wire":False,
                    "color":(200,63,63),
                    "map":"none"
                },
                "physics": {
                    "rigidBody":False,
                    "velocity":(0,0,0),
                    "friction":0.05,
                    "bounce":0,
                    "control":False
                }

                }
            scene.append(aaa)
            sel = len(scene)-1
            sleep(0.1)
        if(guiEvents[28]["pressed"]):
            if(sel != 0):
                scene.pop(sel)
                sel = 0
                print("Removed Mesh.")
            else:
                easygui.msgbox(msg="Cannot Remove Mesh",title="Error:")
            sleep(0.1)
        if(guiEvents[29]["pressed"]):
            d.fill(world["background"])
            render(scene)
            # antialias()
            pg.image.save(d,"out.png")
            easygui.msgbox(msg="Rendered To out.png",title="Success!")
            sleep(0.1)
        if(guiEvents[30]["pressed"]):
            buff = str(scene)
            try:
                numFrames = int(easygui.enterbox("How Many Frames?"))
            except:
                easygui.msgbox(msg="Number Mus Be A Valid Integer",title="Error:")
                numFrames = 0
            for i in range(numFrames):
                scene = simulate(scene,world,keys)
                d.fill(world["background"])
                render(scene)
                pg.display.update()
                pg.image.save(d,"output/" + str(i) + ".png")
                print("Done " +str(i) +  "/" + str(numFrames))
                
            scene = eval(buff)
        if(guiEvents[31]["pressed"]):
            scene[sel]["material"]["wire"] = not(scene[sel]["material"]["wire"])
            sleep(0.1)
        if(guiEvents[32]["pressed"]):
            try:
                f = open(easygui.fileopenbox(default="scenes/",filetypes=["*.ivy","*.*"]),"r")
                buff = str(scene)
                try:
                    
                    scene = eval(f.read())
                except:
                    easygui.msgbox(msg="Invalid Input File",title="Error:")
                    scene = eval(buff)
                    
                f.close()
            except:
                print("Blank File")
        if(guiEvents[33]["pressed"]):
            try:
                f = open(easygui.filesavebox(default="scenes/",filetypes=["*.ivy","*.*"]),"w")
                f.write(str(scene))
                f.close()
            except:
                print("Blank File")
    clr = scene[sel]["material"]["color"]

    r = clr[0]
    g = clr[1]
    b = clr[2]

    r = max(min(r,255),0)
    g = max(min(g,255),0)
    b = max(min(b,255),0)
    scene[sel]["material"]["color"] = (r,g,b)

        
            

        
    
        
            
        
    


    
    pg.display.update()