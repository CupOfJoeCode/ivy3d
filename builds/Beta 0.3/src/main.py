#Import Modules
import pygame as pg
from pygame import gfxdraw
from math import *
from random import randint
from time import sleep
from glob import glob
import easygui
import types
#Custom Modules
from sceneFile import scene,world,player
import guibuttons
import shapes


pg.init() #Initialize pygame

VERSION = "Beta 0.3" # Version

textFont = "font/opensans.ttf" # set default font

w = 800 # Screen size
h = 600
translate = (w/2,h/2)




d = pg.display.set_mode((w,h)) # Initialize the display
pg.display.set_caption("Ivy3d v " + VERSION)
pg.display.set_icon(pg.image.load("favicon.png"))

running = True

#Projects 3d Point To 2d Point
def project(point):
    zscale = 400. #Z scaling constant
    x = point[0]
    y = point[1]
    z = point[2]
    return (x*(2**(z/zscale)) + translate[0],-y*(2**(z/zscale)) + translate[1]) #x = x1*2^z1, y = y1*2^z1


#Multiplies two vectors
def scaleVector(vec,vec2):
    a = list(vec) # Convert tuple to list so it can be assigned to
    for i in range(0,len(a)):
        a[i]*=vec2[i]
    return tuple(a) # Converting list back to tuple


def translateVector(vec,vec2):
    a = list(vec) # Convert tuple to list so it can be assigned to
    for i in range(0,len(a)):
        a[i]+=vec2[i]
    return tuple(a) # Converting list back to tuple

# wip
# def rotateVector(vec,aa):
#     x = vec[0]
#     y = vec[1]
#     z = vec[2]
    
#     x *= sin(aa- (x/(pi/2)  ))
#     y = y
#     z *= cos(aa- (z/(pi/2)))

#     return (x,y,z)



# Calculates the normals for three vectors
def getNormal(vec1,vec2,vec3):
    u = (vec2[0] - vec1[0],vec2[1] - vec1[1],vec2[2] - vec1[2])
    v = (vec3[0] - vec1[0],vec3[1] - vec1[1],vec3[2] - vec1[2])
    nx = (u[1]*v[2]) - (u[2]*v[1])
    ny = (u[2]*v[0]) - (u[0]*v[2])
    nz = (u[0]*v[1]) - (u[1]*v[0])

    return (nx,ny,nz)


# Gets the average of a list of vectors
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




            
# Rendering function takes in scene as a list of dictionaries (see example in sceneFile.py)
def render(s):
    
    zBuffer = [] # Z buffer for rendering triangles in correct order
    for mesh in s:
        
        for tris in meshes[mesh["shape"]]:

            pos = mesh["position"] # Gets position of mesh
            scl = mesh["scale"] # Gets scale of mesh
            point1 = translateVector(scaleVector(tris[0],scl),  pos   ) # Scales and translates each vector according to the position and scale of the mesh
            point2 = translateVector(scaleVector(tris[1],scl),  pos   )
            point3 = translateVector(scaleVector(tris[2],scl),  pos   )

            
            

            facePos = vectorPos([point1,point2,point3]) # Average of all three vector positions to add to the z buffer

            
            normal = getNormal(point1,point2,point3) # Gets normal for face
            normal = float((normal[0] + normal[1] + normal[2])/3.0)/300.0 # Gets average normal
            

            shade = float(    max(min(255 - abs(normal),255),1)    ) # Calculates shading from normal

            color = mesh["material"]["color"] # Gets meshes color


            r = color[0] # Gets each channel from color
            g = color[1]
            b = color[2]

            r = int(r / (255/shade)) # Applies shading to each channel
            g = int(g / (255/shade))
            b = int(b / (255/shade))

            color = (r,g,b) # Applies shaded rgb back to color


            zBuffer.append([point1,point2,point3,facePos,color,mesh["material"]["wire"],mesh["material"]["map"]]) #Adds the triangle data to the z buffer
            
            
    #Sorts the z buffer (bubble sort is not the best solution, but I don't really care it's easy to implement)
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
   

   #Renders the triangles from the z buffer in the correct order
    for i in range(0,len(zBuffer)):
        tri = zBuffer[i]
        gfxdraw.aapolygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])) , tri[4]) # Draws anti-aliased outline around the triangle

        if(not(tri[5])): # Checks to see if the triangle is wireframe
            if(tri[6] == "none"):
                gfxdraw.filled_polygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])) , tri[4]) # Draws solid color triangle if there is no texture
            else:
                imgMap = pg.image.load(tri[6]) # loads texture
                offs = project(tri[0]) # Calculates image offset
                sz = imgMap.get_size() # Gets the size of the image


                if( min(project(tri[0])[0] , project(tri[1])[0] , project(tri[2])[0]  ) >= 0     ): # Checks to see if the triangle is within the bounds of the screen(pygame crashes otherwise)
                    if( max(project(tri[0])[0] , project(tri[1])[0] , project(tri[2])[0]  ) <= w     ):
                        if( min(project(tri[0])[1] , project(tri[1])[1] , project(tri[2])[1]  ) >= 0     ):
                            if( max(project(tri[0])[1] , project(tri[1])[1] , project(tri[2])[1]  ) <= h     ):

                                # Draw textured polygon with offset we calculated before
                                gfxdraw.textured_polygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])),imgMap, int(offs[0]) % sz[0] , int(h-offs[1])  % sz[1] )

        
    
    


    



#Gets collision for physics
def col(mesh1,ss):
    isc = False # Set collision to false
    fric = 1 # Set default fricion
    for msh in ss: # Checks every mesh in the scene
        if mesh1 != msh: # Checking to see if the mesh isn't itself
            pos1 = mesh1["position"]
            scl1 = mesh1["scale"]
            pos2 = msh["position"]
            scl2 = msh["scale"]

            # Checks if the two meshes aren't clipping
            if (pos1[0] > pos2[0] - (scl1[0] + scl2[0]) and pos1[0] < pos2[0] + (scl1[0] + scl2[0]) ) and (pos1[1] > pos2[1] - (scl1[1] + scl2[1]) and pos1[1] < pos2[1] + (scl1[1] + scl2[1]) ) and (pos1[2] > pos2[2] - (scl1[2] + scl2[2]) and pos1[2] < pos2[2] + (scl1[2] + scl2[2]) ):
                # If they are, set the collision to true and the friction to the object's fricion value
                isc = True
                fric = msh["physics"]["friction"]

    return [isc,fric] # Return values



# Calculates all of the physics
def simulate(s,w,k):
    scn = s
    for mesh in scn: # Checks every mesh in the scene
        if(mesh["physics"]["rigidBody"]): # Checks to see if rigidBody is true for the mesh
            if(mesh["physics"]["control"]): # If the mesh has the CharacterController enabled
                maxSpeed = player["maxSpeed"] # Gets max speed, acceleration, and jump strength
                accel = player["accel"]
                jumpS = player["jumpStrength"]

                #movement script
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
            mesh["position"] = (pos[0],pos[1]+vel[1],pos[2]) # Move mesh in the y direction by the y velocity



            cl = col(mesh,scn) # Check for collision

            if cl[0]: # If there is collision, move back and multiply the y-velocity by the bounce value
                pos = mesh["position"]
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0],pos[1]-vel[1],pos[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0] * (1-cl[1]),-vel[1] * bnc,vel[2] * (1-cl[1]))

                if(k[pg.K_SPACE] and mesh["physics"]["control"]): # If the space key is pressed, jump
                    vel = mesh["physics"]["velocity"]
                    mesh["physics"]["velocity"] = (vel[0],jumpS, vel[2] )

            pos = mesh["position"]
            vel = mesh["physics"]["velocity"]
            mesh["position"] = (pos[0]+vel[0],pos[1],pos[2]) # Move mesh in the x direction 

            cl = col(mesh,scn) # Check for Collision
            if cl[0]:
                pos = mesh["position"] # If there is collision, move back and bounce back
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0]-vel[0],pos[1],pos[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0]*bnc,vel[1],vel[2])

            pos = mesh["position"]
            vel = mesh["physics"]["velocity"]
            mesh["position"] = (pos[0],pos[1],pos[2]+vel[2]) # Move mesh in the x direction 
            cl = col(mesh,scn) # If there is collision, move back and bounce back


            if cl[0]: # If there is collision, move back and bounce back
                pos = mesh["position"]
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0],pos[1],pos[2]-vel[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0],vel[1],vel[2]*bnc)



    return scn




# Return a text surface
def text_objects(text, font):
    
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

# Display text
def textdisplay(text,x,y,fff,ffs):
    largeText = pg.font.Font(fff,ffs)
    TextSurf, TextRect = text_objects(text, largeText)
    
    d.blit(TextSurf, (x,y))


# Class for dealing with buttons
class GUIButton():

    def __init__(self,xpos,ypos,textstr): # Initialize variables
        self.x = xpos
        self.y = ypos
        self.w = 1
        self.h = 1
        self.text = textstr
        self.clicked = False


    def render(self,mx,my,mp): # Render the button and process the mouse
        fnt = textFont
        fntSize = 12
        lText = pg.font.Font(fnt,fntSize)
        tSurf, tRect = text_objects(self.text, lText)
        tSize = tSurf.get_size()
        self.w = tSize[0]+2
        self.h = tSize[1]+2
        pg.draw.rect(d,(0,0,0),(self.x,self.y,self.w,self.h) ) # draw button outline

        if (mx > self.x and mx < self.x + self.w) and (my > self.y and my < self.y + self.h): # If mouse is within the bounds of the button
            if(mp): # If mouse is pressed
                pg.draw.rect(d,(127,127,127),(self.x+1,self.y+1,self.w-2,self.h-2) ) # Draw dark button
                self.clicked = True
            else:
                pg.draw.rect(d,(200,200,200),(self.x+1,self.y+1,self.w-2,self.h-2) ) # Draw slightly dark button
                self.clicked = False
        else:
            self.clicked = False
            pg.draw.rect(d,(255,255,255),(self.x+1,self.y+1,self.w-2,self.h-2) ) # Draw white button


        textdisplay(self.text,self.x,self.y,fnt,fntSize) # Draw text
        


def gui(mouseX,mouseY,mousePressed,msh,idx):
    nams = ["Cube","Pyramid","Octahedron","Sphere","PlaneXZ","PlaneXY","PlaneYZ"] # Names of shapes
    fnt = textFont # Set font and font size
    fntSize = 16
    buttons = guibuttons.buttons # Get buttons
    
    pg.draw.rect(d,(0,0,0),(0,0,256,h)) # Draw GUI outline

    
    pg.draw.rect(d,(255,255,255),(0,0,255,h)) # Draw GUI background


    # Draw object data
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


    # Check if each button is pressed
    for i in buttons:
        btn = GUIButton(i["x"],i["y"],i["name"] )
        btn.render(mouseX,mouseY,mousePressed)
        i["pressed"] = btn.clicked

    return buttons
    
    

meshes = shapes.meshes # Get meshes from shapes.py


keys = [] # List of keys and if they are pressed
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
} # Mouse dictionary with x position, y position, and if the mouse is pressed



while running: # Loop while program is running
    for e in pg.event.get(): # Get all events


        if e.type == pg.QUIT: # if program is closed, stop running
            running = False


        if e.type == pg.MOUSEMOTION: # Get mouse motion
            ms = pg.mouse.get_pos()
            mouse["x"] = ms[0]
            mouse["y"] = ms[1]
        if e.type == pg.MOUSEBUTTONDOWN: # Get mouse button
            mouse["pressed"] = True
        if e.type == pg.MOUSEBUTTONUP:
            mouse["pressed"] = False

        if e.type == pg.KEYDOWN: # Get keydown
            keys[e.key] = True
            if(e.key == pg.K_p):
                
                
                if(not(sim)):
                    buff = str(scene)
                else:
                    scene = eval(buff)
                sim = not(sim)
            
            
                    
        if e.type == pg.KEYUP:
            keys[e.key] = False

    # Clear screen
    d.fill(world["background"])


    
    if sim: # Simulate
        scene = simulate(scene,world,keys)
        
    
    

    render(scene) #Render
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
            inText = easygui.fileopenbox(default="maps/",filetypes=["*.png","*.jpg","*.jpeg","*.gif","*.*"])
            if type(inText) == type(" "):
                scene[sel]["material"]["map"] = inText
            else:
                scene[sel]["material"]["map"] = "none"

            
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
                easygui.msgbox(msg="Number Must Be A Valid Integer",title="Error:")
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