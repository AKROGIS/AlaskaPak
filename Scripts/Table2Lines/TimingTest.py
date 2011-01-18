#Out of process results (run from the DOS command line)
#  with 100 points in a shapefile on local hard drive
#    average of 5 runs, tossing high and low
#    dict: .025sec
#    cursor: 1.078sec (43x slower)
#
#  with 1000 points in a shapefile on local hard drive
#    average of 5 runs, tossing high and low
#    dict: .077sec
#    cursor: 11.620sec (151x slower)
#
#  with 100 points in a FGDB on local hard drive
#    average of 5 runs, tossing high and low
#    dict: .992sec
#    cursor: 71.70sec (72x slower)
#
#  with 1000 points in a FGDB on local hard drive
#    1 run
#    dict: .93sec
#    cursor: 711.18sec (765x slower)
#    *results for a FGDB indicate most of the time is in building the cursor,
#     specific testing indicated that to build a cursor against a 1000 pt
#     feature class in a local FGDB, took about .38 seconds, regardless of the
#     where, fields, sort, etc parameters, and regardles of the number of rows
#     in the cursor.
#
#  with 100 points in a PGDB on local hard drive
#    time to build a cursor, regardless of parameters .86sec
#    time to iterate the cursor .002 sec
#    cached solution: 2.4sec
#    cursor solution: 160sec
#
#  with 1000 points in a PGDB on local hard drive
#    time to build a cursor, regardless of parameters 2.05sec
#    time to iterate the cursor .02 sec
#    cached solution: 2.37sec
#    cursor solution: not run
#
# Results for all dataset were similar for an inprocess run
#
# Times for building/iterating a cursor (in process) for the following datasets
#
#   Size | shapefile |   FGDB   |   PGDB
#  ------|-----------|----------|---------
#    100 | .006/.004 | .38/.003 | .89/.003
#   1000 | .007/.037 | .55/.030 | .89/.023
#  10000 | .007/.363 | .37/.301 | .89/.215
#
# Conclusion, if you need to do multiple search cursors on a dataset, it is faster
# to do one cursor, cache the results, and run subsequent queries against the cache.
# This will fail if the dataset is too large for the memory of the python process 


import os, arcgisscripting
import sys,random,time

#I use one search cursor and cache all the points in a dictionary.
#This avoids creating a search cursor for each point as lines are processed
#Assumes Python is more efficient and faster than ArcGIS.  Should be tested.
def GetPoints(gp, pointFC, pointIdField):
    points = {}
    pointDescription = gp.Describe(pointFC)
    pointShapeField = pointDescription.ShapeFieldName
    pointIdFieldDelimited = gp.AddFieldDelimiters(pointFC, pointIdField)
    where = pointIdFieldDelimited + " is not null"
    spatialRef = ""
    fields = pointIdField +"; " + pointShapeField
    sort = ""
    pts = gp.SearchCursor(pointFC, where, spatialRef, fields, sort)
    pt = pts.Next()
    while pt != None:
        points[pt.GetValue(pointIdField)] = pt.Shape.getPart()
        pt = pts.Next()
    return points

def MakeFC(gp, pointFC, count):
    outPath, outName = os.path.split(pointFC)
    gp.CreateFeatureclass_management(outPath, outName, "POINT")
    pts = gp.InsertCursor(pointFC)
    pt = gp.createobject("Point")
    for i in range(count):
        feat = pts.NewRow()
        pt.X = random.uniform(-1000,1000)
        pt.Y  = random.uniform(-1000,1000)
        feat.Shape = pt
        pts.insertRow(feat)
    #close the cursor objects to release the locks
    del feat
    del pts

def Method0(gp, pointFC, count):
    startTime = time.time()
    gp.SearchCursor(pointFC, "", "", "", "")
    elapsedTime = (time.time() - startTime)
    return elapsedTime

def Method0b(gp, pointFC, count):
    pts = gp.SearchCursor(pointFC, "", "", "", "")
    startTime = time.time()
    pt = pts.Next()
    while pt != None:
        a = pt.Shape
        pt = pts.Next()
    elapsedTime = (time.time() - startTime)
    return elapsedTime

def Method1(gp, pointFC, count):
    startTime = time.time()
    points = GetPoints(gp, pointFC,gp.Describe(pointFC).OIDFieldName)
    for i in range(count):
        id = random.randrange(1,count)
        pt = points[id]
        #print id,pt.X,pt.Y       
    elapsedTime = (time.time() - startTime)
    return elapsedTime
    
def Method2(gp, pointFC, count):
    startTime = time.time()
    for i in range(count):
        id = random.randrange(1,count)
        idName = gp.AddFieldDelimiters(pointFC, gp.Describe(pointFC).OIDFieldName)
        where = idName + " = " + str(id)
        fields = "" # pointIdField +"; " + pointShapeField
        pt = gp.SearchCursor(pointFC, where, "", fields, "").Next().Shape.GetPart()
        #print id,pt.X,pt.Y        
    elapsedTime = (time.time() - startTime)
    return elapsedTime
    
def Main():
    gp = arcgisscripting.create(9.3)
    gp.Overwriteoutput = 1
    pointFC = gp.GetParameterAsText(0)
    count = int(gp.GetParameterAsText(1))
    gp.AddMessage("Count = " + str(count))
    MakeFC(gp, pointFC, count)
    gp.AddMessage("Build = " + str(Method0(gp, pointFC, count)) + " seconds")
    gp.AddMessage("iterate = " + str(Method0b(gp, pointFC, count)) + " seconds")
    #gp.AddMessage("Cache = " + str(Method1(gp, pointFC, count)) + " seconds")
    #gp.AddMessage("Cursor = " + str(Method2(gp, pointFC, count)) + " seconds")

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "Usage: " + sys.argv[0] + " NumberOfPoints tempPointFC"
    else:
        Main()
    
    
