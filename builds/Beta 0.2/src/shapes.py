

CUBE = [  

    [(-1,1,-1),(-1,-1,-1),(1,-1,-1)],[(-1,1,-1),(1,1,-1),(1,-1,-1)], #back

    [(1,1,1),(1,1,-1),(1,-1,-1)],[(1,1,1),(1,-1,1),(1,-1,-1)], #right

    [(-1,1,1),(-1,1,-1),(-1,-1,-1)],[(-1,1,1),(-1,-1,1),(-1,-1,-1)], #left

    [(-1,1,1),(-1,1,-1),(1,1,1)],[(1,1,-1),(-1,1,-1),(1,1,1)], #top

    [(-1,-1,1),(-1,-1,-1),(1,-1,1)],[(1,-1,-1),(-1,-1,-1),(1,-1,1)], #bottom

    [(-1,1,1),(-1,-1,1),(1,-1,1)],[(-1,1,1),(1,1,1),(1,-1,1)], #front
    
    ]

PYRAMID = [

    [(-1,-1,-1),(0,-1,1),(0,1,0)],
    [(1,-1,-1),(0,-1,1),(0,1,0)],
    [(-1,-1,-1),(1,-1,-1),(0,1,0)],
    [(-1,-1,-1),(1,-1,-1),(0,-1,1)]
]


OCTAHEDRON = [
    [(0,1,0),(-1,0,1),(1,0,1)],
    [(0,-1,0),(-1,0,1),(1,0,1)],
    [(0,1,0),(-1,0,-1),(1,0,-1)],
    [(0,-1,0),(-1,0,-1),(1,0,-1)],

    [(0,1,0),(1,0,-1),(1,0,1)],
    [(0,-1,0),(1,0,-1),(1,0,1)],

    [(0,1,0),(-1,0,-1),(-1,0,1)],
    [(0,-1,0),(-1,0,-1),(-1,0,1)],
    

]

SPHERE = OCTAHEDRON


meshes = [CUBE,PYRAMID,OCTAHEDRON,SPHERE]