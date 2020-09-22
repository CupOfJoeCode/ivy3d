import pygame as pg
from math import *
import shapes
from sceneFile import scene,world,player
from random import randint
pg.init()

VERSION = "Beta 0.1"



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

def antialias():
    for x in range(0,w-1):
        for y in range(0,h-1):
            clr0 = d.get_at((x,y))
            clr1 = d.get_at((x+1,y))
            clr2 = d.get_at((x,y+1))
            clr3 = d.get_at((x+1,y+1))

            clr = ((clr0[0]+clr1[0]+clr2[0]+clr3[0])/4,(clr0[1]+clr1[1]+clr2[1]+clr3[1])/4,(clr0[2]+clr1[2]+clr2[2]+clr3[2])/4)
            pg.draw.rect(d,clr,(x,y,1,1))


            

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


            zBuffer.append([point1,point2,point3,facePos,color,mesh["material"]["wire"]])
            
            
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
        if(tri[5]):
            pg.draw.line(d,tri[4], project(tri[0]),project(tri[1]),2 )
            pg.draw.line(d,tri[4], project(tri[1]),project(tri[2]),2 )
            pg.draw.line(d,tri[4], project(tri[2]),project(tri[0]),2 )
        else:
            pg.draw.polygon(d,tri[4],( project(tri[0]) , project(tri[1]) , project(tri[2]) ))
    
    


    




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

meshes = shapes.meshes


keys = []
for i in range(0,1024):
    keys.append(False)

a = 0

sim = False
sel = 0

buff = ""

while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            keys[e.key] = True
            if(e.key == pg.K_p):
                
                
                if(not(sim)):
                    buff = str(scene)
                else:
                    scene = eval(buff)
                sim = not(sim)
            
            if(not(sim)):
                if(e.key == pg.K_m):
                    scene[sel]["shape"]+=1
                    if(scene[sel]["shape"] > len(shapes.meshes)-1):
                        scene[sel]["shape"] = 0
                if(e.key == pg.K_h):
                    scene[sel]["material"]["wire"] = not(scene[sel]["material"]["wire"])    
                    print("Wireframe Set To " + str(scene[sel]["material"]["wire"]))
                if(e.key == pg.K_i):
                    sel+=1
                    if(sel > len(scene)-1):
                        sel = 0
                if(e.key == pg.K_0):
                    d.fill(world["background"])
                    render(scene)
                    antialias()
                    pg.image.save(d,"out.png")
                    print("Rendered To out.png")
                if(e.key == pg.K_r):
                    scene[sel]["physics"]["rigidBody"] = not(scene[sel]["physics"]["rigidBody"])
                    print("RigidBody Set To " + str(scene[sel]["physics"]["rigidBody"]))
                if(e.key == pg.K_v):
                    scene[sel]["physics"]["control"] = not(scene[sel]["physics"]["control"])
                    print("Character Controller Set To " + str(scene[sel]["physics"]["control"]))
                if(e.key == pg.K_k):
                    if(sel != 0):
                        scene.pop(sel)
                        sel = 0
                        print("Removed Mesh.")
                    else:
                        print("Cannot Remove Mesh.")
                if(e.key == pg.K_n):
                    aaa = {
                            "shape":0,

                            "position":(0,0,0),
                            "scale":(25,25,25),
                            "material":{

                                "wire":False,
                                "color":(200,63,63)
                            },
                            "physics": {
                                "rigidBody":False,
                                "velocity":(0,0,0),
                                "friction":1,
                                "bounce":0,
                                "control":False
                            }

                    }
                    scene.append(aaa)
                    sel = len(scene)-1
                    print("Created New Mesh.")
                    
        if e.type == pg.KEYUP:
            keys[e.key] = False
    d.fill(world["background"])


    
    if sim:
        scene = simulate(scene,world,keys)
        pg.display.set_caption("Ivy3d v " + VERSION + ": Player")
    
    

    render(scene)
    if(not(sim)):
        
        
        pos = scene[sel]["position"]
        pg.draw.line(d,(255,0,0),project(pos),project(  (pos[0]+25,pos[1],pos[2])  ) ,4)
        pg.draw.line(d,(0,255,0),project(pos),project(  (pos[0] ,pos[1]+25,pos[2])  ) ,4)
        pg.draw.line(d,(0,0,255),project(pos),project(  (pos[0] ,pos[1],pos[2]+25)  ) ,4)
        if(keys[pg.K_g]):
            name = "scale"
        else:
            name = "position"
        meshNames = ["Cube","Pyramid","Octahedron","Sphere"]
        pg.display.set_caption("Ivy3d " + VERSION + ": " + str(sel) + ", " + meshNames[scene[sel]["shape"]] + ", " + str(scene[sel][name]))
        if(keys[pg.K_w]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1]+2,pos[2])
        if(keys[pg.K_s]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1]-2,pos[2])
        if(keys[pg.K_a]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0]-2,pos[1],pos[2])
        if(keys[pg.K_d]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0]+2,pos[1],pos[2])
        if(keys[pg.K_q]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1],pos[2]-2)
        if(keys[pg.K_e]):
            pos = scene[sel][name]
            scene[sel][name] = (pos[0],pos[1],pos[2]+2)

        if(keys[pg.K_9]):
            buff = str(scene)
            print("How Many Frames?")
            numFrames = int(raw_input())
            for i in range(numFrames):
                scene = simulate(scene,world,keys)
                d.fill(world["background"])
                render(scene)
                pg.display.update()
                pg.image.save(d,"output/" + str(i) + ".png")
                print("Done " +str(i) +  "/" + str(numFrames))
            scene = eval(buff)
        
        if(keys[pg.K_c]):
            print("Input Color:")
            scene[sel]["material"]["color"] = eval(raw_input())
        
        if(keys[pg.K_b]):
            print("Set Bounce Value (float 0-1)")
            scene[sel]["physics"]["bounce"] = float(raw_input())
        if(keys[pg.K_f]):
            print("Set Friction Value (float 0-1)")
            scene[sel]["physics"]["friction"] = float(raw_input())
        if(keys[pg.K_j]):
            print("Save As:")
            f = open("scenes/" + raw_input()+".pyr","w")
            f.write(str(scene))
            f.close()
        

        if(keys[pg.K_l]):
            print("Load From:")
            f = open("scenes/" + raw_input()+".pyr","r")
            scene = eval(f.read())
            f.close()
        if(keys[pg.K_y]):
            print("How Many Particles?")
            partnum = int(raw_input())
            for i in range(0,partnum):
                selc = scene[sel]
                aaa = {
                            "shape":selc["shape"],

                            "position":translateVector(selc["position"],(randint(-500,500),randint(-500,500),randint(-500,500)    )),
                            "scale":scaleVector(selc["scale"],(0.25,0.25,0.25)),
                            "material":selc["material"],
                            "physics": {
                                
                                
                                "rigidBody":True,
                                "velocity":(randint(-50,50)/100.0,randint(-50,50)/100.0,randint(-50,50)/100.0),
                                "friction":0,
                                "bounce":0.5,
                                "control":False
                            
                            }

                    }
                
                scene.append(aaa)
            
        
    


    
    pg.display.update()