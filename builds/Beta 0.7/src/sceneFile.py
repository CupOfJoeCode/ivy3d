world = {
    "gravity":0.01,
    "background":(127,127,127),
    "projection":1
}

player = {
    "jumpStrength":2,
    "maxSpeed":2,
    "accel":0.05
}


scene = [
    {
        "shape":4,

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
            
        }

    },
    {
        "shape":0,

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
            
        }

    },
    
    
    

    
    
    
]
