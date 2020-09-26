#Import Modules
import pygame as pg
from pygame import gfxdraw
from math import *
from random import randint
from time import sleep
from glob import glob
import easygui
import types
import copy
#Custom Modules
from sceneFile import scene,world,player
import guibuttons
import shapes


pg.init() #Initialize pygame

VERSION = "Beta 0.5" # Version

textFont = "font/opensans.ttf" # set default font

w = 800 # Screen size
h = 600
translate = (w/2,h/2)

perspective = True


d = pg.display.set_mode((w,h)) # Initialize the display
pg.display.set_caption("Ivy3d v " + VERSION)
pg.display.set_icon(pg.image.load("favicon.png"))

running = True

#Projects 3d Point To 2d Point
def project(point):
    zscale = 400.0 #Z scaling constant
    x = point[0]
    y = point[1]
    z = point[2]
    if perspective:
        return (x*(2**(z/zscale)) + translate[0],-y*(2**(z/zscale)) + translate[1]) #x = x1*2^z1, y = y1*2^z1 ; Perspective Projection
    else:
        return (x+translate[0],-y+translate[1]) # Orthographhic Projection


#Multiplies two vectors
def scaleVector(vec,vec2):
    a = list(vec) # Convert tuple to list so it can be assigned to
    for i in range(0,len(a)):
        a[i]*=vec2[i]
    return tuple(a) # Converting list back to tuple


#Adds two vectors
def translateVector(vec,vec2):
    a = list(vec) # Convert tuple to list so it can be assigned to
    for i in range(0,len(a)):
        a[i]+=vec2[i]
    return tuple(a) # Converting list back to tuple


#Rotates vector by another vector
def rotateVector(vec,vec2):
    x1 = vec[0]
    y1 = vec[1]
    z1 = vec[2]

    xr = vec2[0]
    yr = vec2[1]

    # X-Axis 
   
    x1 = x1
    y1 = y1*cos(xr)-z1*sin(xr)
    z1 = y1*sin(xr)+z1*cos(xr)

    # Y-Axis 
    
    x1 = z1*sin(yr)+x1*cos(yr)
    y1 = y1
    z1 = z1*cos(yr)-x1*sin(yr)

    
    return (x1,y1,z1)



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





def qsort(inlist):
    if inlist == []: 
        return []
    else:
        pivot = inlist[0]
        lesser = qsort([x for x in inlist[1:] if x < pivot])
        greater = qsort([x for x in inlist[1:] if x >= pivot])
        return lesser + [pivot] + greater


def linInterp(a,b,x):
    return (float(b)-float(a))/(255)*float(x) + float(a)
            
# Rendering function takes in scene as a list of dictionaries (see example in sceneFile.py)
def render(s):
    
    zBuffer = [] # Z buffer for rendering triangles in correct order
    for mesh in s:
        
        for tris in meshes[mesh["shape"]]:

            pos = mesh["position"] # Gets position of mesh
            scl = mesh["scale"] # Gets scale of mesh
            rot = mesh["rotation"] # Gets rotation of mesh
            point1 = translateVector( rotateVector( scaleVector( tris[0],scl ) ,rot) , pos) # Rotates, scales, and translates each vector according to the position and scale of the mesh
            point2 = translateVector( rotateVector( scaleVector( tris[1],scl ) ,rot) , pos)
            point3 = translateVector( rotateVector( scaleVector( tris[2],scl ) ,rot) , pos)

            
            

            facePos = vectorPos([point1,point2,point3]) # Average of all three vector positions to add to the z buffer

            
            normal = getNormal(point1,point2,point3) # Gets normal for face
            normal = float((normal[0] + normal[1] + normal[2])/3.0)/(300.0*mesh["material"]["metal"]) # Gets average normal
            

            shade = float(    max(min(255 - abs(normal),255),1)    ) # Calculates shading from normal

            color = mesh["material"]["color"] # Gets meshes color


            r = color[0] # Gets each channel from color
            g = color[1]
            b = color[2]

            r = r / (255/ shade) # Applies shading to each channel
            g = g / (255/ shade)
            b = b / (255/ shade)

            r = linInterp(r,255,shade/8.0) # add specular
            g = linInterp(g,255,shade/8.0)
            b = linInterp(b,255,shade/8.0)

            r = max(min(255,int(r)),0) # makes valid color argument
            g = max(min(255,int(g)),0)
            b = max(min(255,int(b)),0)


            color = (r,g,b) # Applies shaded rgb back to color
            alpha = mesh["material"]["alpha"] # Gets alpha from material

            zBuffer.append([point1,point2,point3,facePos,color + (alpha,) ,mesh["material"]["wire"],mesh["material"]["map"]]) #Adds the triangle data to the z buffer
            
            
    
    zs = [] 
    for i in zBuffer:
        zs.append(i[3][2]) # Get all face z positions(for sorting)
    
    
    # Sorts the indices of the z buffer based on the z positions of the z buffer
    inds = [x for _,x in sorted(zip(zs,range(len(zBuffer))))]

    

   #Renders the triangles from the z buffer in the correct order
    for i in range(0,len(zBuffer)):
        tri = zBuffer[inds[i]] # Gets correct face based on sorted indices

        

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
        else:
            gfxdraw.aapolygon(d, (project(tri[0]) , project(tri[1]) , project(tri[2])) , tri[4]) # Draws anti-aliased outline around the triangle
        
    
    


    



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
                mesh["physics"]["velocity"] = (vel[0]*-bnc,vel[1],vel[2])

            pos = mesh["position"]
            vel = mesh["physics"]["velocity"]
            mesh["position"] = (pos[0],pos[1],pos[2]+vel[2]) # Move mesh in the z direction 
            cl = col(mesh,scn) # If there is collision, move back and bounce back


            if cl[0]: # If there is collision, move back and bounce back
                pos = mesh["position"]
                vel = mesh["physics"]["velocity"]
                mesh["position"] = (pos[0],pos[1],pos[2]-vel[2])
                vel = mesh["physics"]["velocity"]
                bnc = mesh["physics"]["bounce"]
                mesh["physics"]["velocity"] = (vel[0],vel[1],vel[2]*-bnc)



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

    def __init__(self,xpos,ypos,textstr): # Constructor
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
        


def gui(mouseX,mouseY,mousePressed,msh,idx): # Function for dealing with GUI
    nams = ["Cube","Pyramid","Octahedron","Sphere","PlaneXZ","PlaneXY","PlaneYZ","BlenderMonkey"] # Names of shapes
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
    rtt = msh["rotation"]
    rtt = ( degrees(rtt[0]),degrees(rtt[1]) )
    textdisplay("Rotation: " + str(  (round(rtt[0],3),round(rtt[1],3))  ),w - 200,208,fnt,fntSize )
    textdisplay("Metalness: " + str( msh["material"]["metal"] ),w - 200,228,fnt,fntSize )
    textdisplay("Alpha: " + str( msh["material"]["alpha"] ),w - 200,248,fnt,fntSize )


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
                    buff = copy.deepcopy(scene)
                else:
                    scene = copy.deepcopy(buff)
                sim = not(sim)
            
            
                    
        if e.type == pg.KEYUP:
            keys[e.key] = False

    # Clear screen
    d.fill(world["background"])

    # Set Projection Mode
    perspective = world['projection']

    
    if sim: # Simulate
        scene = simulate(scene,world,keys)
        
    
    

    render(scene) #Render
    if(not(sim)):
        pos = scene[sel]["position"]
        pg.draw.line(d,(255,0,0),project(pos),project(  (pos[0]+25,pos[1],pos[2])  ) ,4) #Draw axies at position
        pg.draw.line(d,(0,255,0),project(pos),project(  (pos[0] ,pos[1]+25,pos[2])  ) ,4)
        pg.draw.line(d,(0,0,255),project(pos),project(  (pos[0] ,pos[1],pos[2]+25)  ) ,4)


        guiEvents = gui(mouse["x"],mouse["y"],mouse["pressed"],scene[sel],sel) #Get all button

        if guiEvents[0]["pressed"]:
            sel+=1
            sel%=len(scene)
            sleep(0.1)
        elif guiEvents[1]["pressed"]:
            scene[sel]["shape"]+=1
            scene[sel]["shape"]%=len(meshes)
            sleep(0.1)
        elif guiEvents[2]["pressed"]:
            posit = easygui.multenterbox("Translation:","Translation",['X:','Y:','Z:'], list(scene[sel]["position"])  )
            if posit != None:
                try:
                    for i in range(len(posit)):
                        posit[i] = float(posit[i])
                    scene[sel]["position"] = tuple(posit)
                except:
                    easygui.msgbox("Options Must Be Valid Numbers","Error")
        elif guiEvents[3]["pressed"]:
            posit = easygui.multenterbox("Scale:","Scale",['X:','Y:','Z:'], list(scene[sel]["scale"])  )
            if posit != None:
                try:
                    for i in range(len(posit)):
                        posit[i] = float(posit[i])
                    scene[sel]["scale"] = tuple(posit)
                except:
                    easygui.msgbox("Options Must Be Valid Numbers","Error")
        elif guiEvents[4]["pressed"]:
            rt = list(scene[sel]["rotation"])
            rt[0] = degrees(rt[0])
            rt[1] = degrees(rt[1])
            posit = easygui.multenterbox("Rotation:","Rotation",['X:','Y:'], rt  )
            if posit != None:
                try:
                    for i in range(len(posit)):
                        posit[i] = radians(float(posit[i]))
                    scene[sel]["rotation"] = tuple(posit)
                except:
                    easygui.msgbox("Options Must Be Valid Numbers","Error")
        elif guiEvents[5]["pressed"]:
            mats = easygui.multenterbox("Material:","Material",['Color:','Wireframe:','Metalness:','Alpha:'], [str(scene[sel]["material"]['color']).replace('(','').replace(')',''),scene[sel]["material"]["wire"],scene[sel]["material"]["metal"],scene[sel]["material"]["alpha"]]  )
            if mats != None:
                try:
                    clr = mats[0].split(',')
                    for i in range(3):
                        clr[i] = max(min(255,int(clr[i])),0)
                    wf = mats[1]
                    met = mats[2]
                    aph = mats[3]
                    scene[sel]["material"]["color"] = tuple(clr)
                    if wf.lower() in ['true','1']:
                        scene[sel]["material"]["wire"] = True
                    else:
                        scene[sel]["material"]["wire"] = False
                    scene[sel]["material"]["metal"] = float(met)
                    scene[sel]["material"]["alpha"] = max(min(int(aph),255),0)
                except:
                    easygui.msgbox("Invalid Value(s)","Error")
        elif guiEvents[6]["pressed"]:
            rbody = scene[sel]["physics"]["rigidBody"]
            initv = str(scene[sel]["physics"]["velocity"]).replace('(','').replace(')','')
            fric = scene[sel]['physics']['friction']
            bonc = scene[sel]['physics']['bounce']
            ccont = scene[sel]['physics']['control']
            phys = easygui.multenterbox("Physics:","Physics",['Rigid Body:','Initial Velocity (XYZ):','Friction:','Bounciness:','Character Control:'],[rbody,initv,fric,bonc,ccont])
            
            if phys != None:
                try:
                    rbdy = phys[0]
                    intv = phys[1].split(',')
                    for i in range(3):
                        intv[i] = float(intv[i])
                    frc = phys[2]
                    bnc = phys[3]
                    cnt = phys[4]
                    if rbdy.lower() in ['true','1']:
                        scene[sel]['physics']['rigidBody'] = True
                    else:
                        scene[sel]['physics']['rigidBody'] = False
                    scene[sel]['physics']['velocity'] = tuple(intv)
                    scene[sel]['physics']['friction'] = float(frc)
                    scene[sel]['physics']['bounce'] = float(bnc)
                    if cnt.lower() in ['true','1']:
                        scene[sel]['physics']['control'] = True
                    else:
                        scene[sel]['physics']['control'] = False
                except:
                    easygui.msgbox("Invalid Value(s)","Error")
        elif guiEvents[7]["pressed"]:
            blankMesh = {
                "shape":0,
                "position":(0,0,0),
                "scale":(25,25,25),
                "rotation":(0,0),
                "material":{
                    "wire":False,
                    "color":(200,63,63),
                    "metal":1,
                    "map":"none",
                    "alpha":255
                },
                "physics": {
                    "rigidBody":True,
                    "velocity":(0,0,0),
                    "friction":0.05,
                    "bounce":0,
                    "control":False
                    }
                }
            scene.append(blankMesh)
            sel = len(scene)-1
            sleep(0.1)
        elif guiEvents[8]["pressed"]:
            if sel != 0:
                scene.pop(sel)
                sel-=1
            else:
                easygui.msgbox("Cannot Remove Mesh","Error")
            sleep(0.1)
        elif guiEvents[9]["pressed"]:
            d.fill(world["background"])
            render(scene)
            pg.image.save(d,easygui.filesavebox(filetypes=['*.png','*.jpg','*.*']))
        elif guiEvents[10]["pressed"]:
            try:
                opts = easygui.multenterbox("Number Of Frames","Export Video",["Start:","End:"],[0,100])
                dr = easygui.diropenbox()
                ssn = copy.deepcopy(scene)
                for i in range(int(opts[1])):
                    for j in range(2):
                        ssn = simulate(ssn,world,keys)
                    if i >= int(opts[0]):
                        d.fill(world["background"])
                        render(ssn)
                        pg.image.save(d,  dr + '/' + str(i-int(opts[0])) + '.png'  )
                easygui.msgbox("Saved to " + dr,"Success")
                
            except:
                easygui.msgbox("Invalid Integer Value","Error")
        elif guiEvents[11]["pressed"]:
            fnam = easygui.fileopenbox(default="maps/")
            if fnam == None:
                scene[sel]["material"]["map"] = 'none'
            else:
                scene[sel]["material"]["map"] = fnam
        elif guiEvents[12]["pressed"]:
            opts = easygui.multenterbox("World:","World",["Gravity:","Bakground Color:","Projection(0:Orth,1:Persp):"],[ world['gravity'], str(world['background']).replace('(','').replace(')',''),world['projection'] ])
            if opts != None:
                try:
                    world['gravity'] = float(opts[0])
                    colrs = opts[1].split(',')
                    for i in range(3):
                        colrs[i] = max(0,min(255,int(colrs[i])))
                    world['background'] = tuple(colrs)
                    world['projection'] = max(0,min(1,int(opts[2])))
                except:
                    easygui.msgbox("Invalid Value(s)","Error")
        elif guiEvents[13]["pressed"]:
            opts = easygui.multenterbox("Player:","Player",["Jump Strength:","Max Speed:","Acceleration:"],[ player["jumpStrength"],player['maxSpeed'],player['accel'] ])
            if opts != None:
                try:
                    player['jumpStrength'] = float(opts[0])
                    player['maxSpeed'] = float(opts[1])
                    player['accel'] = float(opts[2])
                except:
                    easygui.msgbox("Invalid Value(s)","Error")
        elif guiEvents[14]['pressed']:
            fnam = easygui.fileopenbox(default="scenes/", filetypes=['*.ivy','*.*'])
            if fnam != None:
                try:
                    f = open(fnam,'r')
                    inpScene = eval(f.read())
                    f.close()
                    scene = inpScene['scene']
                    world = inpScene['world']
                    player = inpScene['player']
                except:
                    easygui.msgbox('Invalid File','Error')
        elif guiEvents[15]['pressed']:
            fnam = easygui.filesavebox(default="scenes/", filetypes=['*.ivy','*.*'])
            if fnam != None:
                try:
                    f = open(fnam,'w')
                    outDict = {
                        'scene':copy.deepcopy(scene),
                        'world':copy.deepcopy(world),
                        'player':copy.deepcopy(player)
                    }
                    f.write(str(outDict))
                    f.close()
                except:
                    easygui.msgbox('Unknown Error','Error')
        

            

    pg.display.update() # Update Screen