from copy import deepcopy as dpc
from shapes import meshes

    
blankanim = []
for i in range(15):
    blankanim.append(0)


blankmesh = {
        "shape":meshes[0],
        "name":"cube",

        "position":(0,0,0),
        "scale":(25,25,25),
        "rotation":(0,0),
        "bounds":(0,0,0),
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
            
        },
        'animation': {
            'xpos':dpc(blankanim),
            'ypos':dpc(blankanim),
            'zpos':dpc(blankanim),
            'xrot':dpc(blankanim),
            'yrot':dpc(blankanim),
            'xscale':dpc(blankanim),
            'yscale':dpc(blankanim),
            'zscale':dpc(blankanim)
        }

    }

world = {
    "gravity":0.01,
    "background":(127,127,127),
    "projection":1,
    "image":'none'
}

player = {
    "jumpStrength":2,
    "maxSpeed":2,
    "accel":0.05
}
ppe = []


scene = [
    {
        "shape":meshes[4],
        "name":"PlaneXZ",

        "position":(0,-100,0),
        "scale":(100,1,100),
        "rotation":(0,0),
        "bounds":(0,0,0),
        "material":{

            "wire":False,
            "color":(63,63,200),
            "metal":1,
            "map":"none",
            "alpha":255
        },
        "physics": {
            "rigidBody":False,
            "velocity":(0,0,0),
            "friction":0.05,
            "bounce":0,
            "control":False
            
        },

        'animation': {
            'xpos':dpc(blankanim),
            'ypos':dpc(blankanim),
            'zpos':dpc(blankanim),
            'xrot':dpc(blankanim),
            'yrot':dpc(blankanim),
            'xscale':dpc(blankanim),
            'yscale':dpc(blankanim),
            'zscale':dpc(blankanim)
        }

    },
    {
        "shape":meshes[0],
        "name":"Cube",

        "position":(0,0,0),
        "scale":(25,25,25),
        "rotation":(0,0),
        "bounds":(0,0,0),
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
            
        },
        'animation': {
            'xpos':dpc(blankanim),
            'ypos':dpc(blankanim),
            'zpos':dpc(blankanim),
            'xrot':dpc(blankanim),
            'yrot':dpc(blankanim),
            'xscale':dpc(blankanim),
            'yscale':dpc(blankanim),
            'zscale':dpc(blankanim)
        }

    },
    
    
    

    
    
    
]
