# ---------------------------------------------------------------------------
# obscurePoints.py
# Created by: regan_sarwas@nps.gov
# Created on: 2010-08-30
# ---------------------------------------------------------------------------

# Problems:
#  * None yet.

#Matches string as returned by Field.Type to the type code desired by gp.AddField()
typeMap = {"SmallInteger" : "SHORT",
           "Integer" : "LONG",
           "Single" : "FLOAT",
           "Double" : "DOUBLE",
           "String" : "TEXT",
           "Date" : "DATE",
           "OID" : "LONG",      #Not usually creatable with AddField() - use with Caution
           "Geometry" : "BLOB", #Not usually creatable with AddField() - use with Caution
           "BLOB" : "BLOB"}

# Import system modules
import sys, string, os, arcgisscripting, datetime
import random, math
import time
import arcpy

#Create the geoprocessing objectf
gp = arcgisscripting.create(9.3)

arcpy.GetParameterAsText(0);

# Input feature class
inFeatureClass = gp.GetParameterAsText(0)

#describe the input features (to get the spatial reference and the type of the idField)
inFcDescription = gp.Describe(inFeatureClass)
inType = inFcDescription.ShapeType.upper()
inShapeField = inFcDescription.ShapeFieldName

# Output feature class
outFeatureClass = gp.GetParameterAsText(1)
outPath, outName = os.path.split(outFeatureClass)

#validate output
#The user can control overwrite or not with Tools->Options->geoprocessing...
#ArcGIS (toolbox or command line) does not do any validation on the output workspace
if not gp.Exists(outPath):
    raise ValueError("Error: The output workspace does not exist.")

# Output type - validated as within ['Points','Circles'] by ArcGIS
outType = gp.GetParameterAsText(2)

minOffset = float(gp.GetParameterAsText(3))
maxOffset = float(gp.GetParameterAsText(4))

#validate min/max
if (minOffset < 0):
    raise ValueError("Error: The minimum offset must be greater than zero.")
if (maxOffset <= minOffset):
    raise ValueError("Error: The maximum offset must be greater than the minimum offset")

nogoAreas = gp.GetParameterAsText(5).split(";")
if nogoAreas[0] == "":
    nogoAreas = [];


def FixPoint(pt, minOffset, maxOffset, nogoAreas):
    gp.AddMessage("code pt 1.1")
    if (pt.Shape.Type.lower() == "point"):
        array = GetRandomizedPoint(pt.Shape)
        pt.Shape = array
    if (pt.Shape.Type.lower() == "multipoint"):
        array = GetRandomizedArray(pt.Shape)
        pt.Shape = array
    gp.AddMessage("code pt 1.2")
    
def MakeCircle(pt, circle, minOffset, maxOffset, nogoAreas):
    # Add the new attributes to the feature.
    # tweak point geometry
    # create buffer on point
    # copy all attributes from pt to circle
    pass

def RandomizePoint(x,y,r1,r2):
    r = random.uniform(r1,r2)
    phi = random.uniform(0,2*math.pi)
    x2 = x + r*math.cos(phi) 
    y2 = y + r*math.sin(phi)
    return (x2,y2)

def GetRandomizedPoint(geom):
    # A point can be an array of 1 point, or a single point
    # A multipoint is an array of n (where n > 1) points.
    
    if ((geom == None) or (geom.Type.lower() != "point")):
        return []
    
    gp.AddMessage("code pt 1.1.1 (point)")
    pnt = geom.getpart(0)
    gp.AddMessage("code pt 1.1.2")
    esri_pt =  gp.CreateObject("Point")
    gp.AddMessage("code pt 1.1.3")
    while True:
        gp.AddMessage("code pt 1.1.3.1")
        newpt = RandomizePoint(pnt.x, pnt.y,minOffset, maxOffset)
        esri_pt.X,esri_pt.Y = newpt
        pt_geom = gp.createobject("geometry", "point", esri_pt)
        gp.AddMessage("code pt 1.1.3.2")
        if (NotInNoGo(pt_geom,nogoAreas)):
            gp.AddMessage("break from 1.1.3.2")
            break
    
    return esri_pt

def GetRandomizedArray(geom):
    # A point can be an array of 1 point, or a single point
    # A multipoint is an array of n (where n > 1) points.
    
    if (geom == None) or (geom.Type.lower() not in ["point", "multipoint"]):
        return []
    
    #try:
    gp.AddMessage("code pt 1.1.1 (multipoint)")
    pts = gp.createobject("Array")
    gp.AddMessage("code pt 1.1.2")
    partnum = 0
    partcount = geom.partcount
    gp.AddMessage("   part count = " + str(partcount))
    while partnum < partcount:
        gp.AddMessage("code pt 1.1.3")
        pnt = geom.getpart(partnum)
        esri_pt =  gp.CreateObject("Point")
        gp.AddMessage("code pt 1.1.4")
        
        while True:
            newpt = RandomizePoint(pnt.x, pnt.y,minOffset, maxOffset)
            esri_pt.X,esri_pt.Y = newpt
            pt_geom = gp.createobject("geometry", "point", esri_pt)
            gp.AddMessage("code pt 1.1.4.1")
            if (NotInNoGo(pt_geom,nogoAreas)):
                gp.AddMessage("break from 1.1.4.1")
                break

        gp.AddMessage("code pt 1.1.5")
        pts.Add(esri_pt)
        gp.AddMessage("code pt 1.1.6")
        partnum += 1
    return pts

def NotInNoGo(pt, FCList):
    gp.AddMessage("code pt 1.1.4.1.1")
    if (len(FCList) == 0):
        gp.AddMessage("code pt 1.1.4.1.2 - empty fc list")
        return true;
    for fc in FCList:
        gp.AddMessage("code pt 1.1.4.1.2")
        if PointInFC(pt, fc):
            gp.AddMessage("code pt 1.1.4.1.2 - false")
            return False
    gp.AddMessage("code pt 1.1.4.1.3")
    return True

def PointInFC(pt, fc):
    outGeom = gp.createobject("geometry")
    gp.AddMessage("code pt 1.1.4.1.3.1")
    start = time.time()
    gp.AddMessage("fc = "+fc+" point = ("+str(pt.getpart(0).X)+","+str(pt.getpart(0).Y)+")")
    # Clip the point geometry object with the area FC.  The 
    #   resulting geometry is in the NewOutGeom list; outGeom is just a placeholder
    #   to indicate that expected output is a geometry object and not a FC
    # Vector Overlay tools:
    #  union, update, symetrical difference - do not accept points
    #  near, intersect - needs a fc not geometry.
    #  clip, spatialJoin - work, but are very slow (953 error problems)
    #  identity - works (very slowly ~1.3 second for 1 pt and 10 rectangles), but also always returns a result
    
    #newOutGeom = gp.clip_analysis(pt, fc, outGeom)
    #newOutGeom = gp.identity_analysis(pt, fc, outGeom)
    newOutGeom = gp.erase_analysis(pt, fc, outGeom)
    #newOutGeom = gp.SpatialJoin_analysis(pt, fc, outGeom, "JOIN_ONE_TO_ONE","KEEP_COMMON","#", "IS_WITHIN")
    #newOutGeom = gp.Near_analysis(pt, fc, "0")
    gp.AddMessage("erase took "+str(time.time() - start)+" sec.")
    gp.AddMessage("code pt 1.1.4.1.3.2")
    gp.AddMessage("Out Geom = " + str(newOutGeom))
    if (newOutGeom == None or len(newOutGeom) == 0):
        return False
    else:
        return True

def PointInPoly(pt,poly):
    pass


        
#raise ValueError("Info: ShapeType = " + inType)

if (outType == 'Points'):
    gp.FeatureclassToFeatureclass_conversion(inFeatureClass, outPath, outName)
    outFCdesc = gp.describe(outFeatureClass)
    outShapeField = outFCdesc.ShapeFieldName
    
    pts = gp.UpdateCursor(outFeatureClass)
    pt = pts.Next()
    while pt != None:
        gp.AddMessage("code pt 1")
        FixPoint(pt, minOffset, maxOffset, nogoAreas)
        gp.AddMessage("code pt 2")
        pts.UpdateRow(pt)
        gp.AddMessage("code pt 3")
        pt = pts.Next()
        gp.AddMessage("code pt 4")
    #remove locks
    del pt
    del pts
    
else:
    gp.CreateFeatureclass_management(outPath, outName, "POLYGON", inFeatureClass, "#", "SAME_AS_TEMPLATE")
    outFCdesc = gp.describe(outFeatureClass)
    outShapeField = outFCdesc.ShapeFieldName

    pts = gp.SearchCursor(inFeatureClass)
    circles = gp.InsertCursor(outFeatureClass)
    pt = pts.Next()
    while pt != None:
        circle = circles.NewRow()
        MakeCircle(pt, circle, minOffset, maxOffset, nogoAreas)
        circles.InsertRow(circle)
        pt = pts.Next()
    #remove locks
    del pt
    del pts
    del circle
    del circles
