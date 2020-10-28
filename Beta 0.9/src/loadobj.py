def cleanFace(a):
    
    if '/' in a:
        nearest = 0
        scan = True
        i = 0
        while i < len(a) and scan:
            if a[i] == '/': scan = False
            i+=1
        nearest = i
        return a[0:nearest-1]
    else: return a
def loadobj(obj):
    lines = obj.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].split(' ')
    
    verts = []
    shape = []
    oName = "OBJ"
    for i in lines:
        if i[0] == 'v':
            verts.append( (float(i[1]),float(i[2]),float(i[3]) ) )
        if i[0] == 'f':
            shape.append( [ verts[ int(  cleanFace(i[1])  )-1 ] ,verts[ int(   cleanFace(i[2])   )-1 ] ,verts[ int(   cleanFace(i[3])   )-1 ] ]  )
        if i[0] == 'o':
            oName = i[1]
    return [shape,oName]

def saveobj(mesh):
    outobj = """# Ivy3D OBJ File:
# https://sites.google.com/view/joejanicki
o """ + mesh['name']
    geom = mesh['shape']
    verts = []
    for tri in geom:
        for v in tri:
            if v not in verts:
                verts.append(v)
    for v in verts:
        outobj += "\nv " + str(v[0]/25) + ' ' + str(v[1]/25) + ' ' + str(v[2]/25)
    for f in geom:
        outobj += "\nf " + str(verts.index(f[0]) + 1) + ' ' + str(verts.index(f[1]) + 1) + ' ' + str(verts.index(f[2]) + 1)


    return outobj
    
#from loadobj import cleanFace