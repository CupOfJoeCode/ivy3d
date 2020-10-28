from loadobj import loadobj


arr = None

with open('terrainblank.obj','r') as fp:
    arr = loadobj(fp.read())

with open('out.txt','w') as fp:
    fp.write(str(arr[0]))