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
    for i in lines:
        if i[0] == 'v':
            verts.append( (float(i[1]),float(i[2]),float(i[3]) ) )
        if i[0] == 'f':
            shape.append( [ verts[ int(  cleanFace(i[1])  )-1 ] ,verts[ int(   cleanFace(i[2])   )-1 ] ,verts[ int(   cleanFace(i[3])   )-1 ] ]  )

    return shape

#from loadobj import cleanFace