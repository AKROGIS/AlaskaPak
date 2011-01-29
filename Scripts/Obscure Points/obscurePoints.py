# ---------------------------------------------------------------------------
# obscurePoints.py
# Created by: regan_sarwas@nps.gov
# Created on: 2010-08-30
# ---------------------------------------------------------------------------

# Problems:
#  * None yet.
# Import system modules
import sys, string, os, datetime
import random, math, time
import arcpy


# Maps the string returned by arcpy.Field.type to the string required by
# arcpy.AddField_management().
typeMap = {"SmallInteger" : "SHORT",
           "Integer"      : "LONG",
           "Single"       : "FLOAT",
           "Double"       : "DOUBLE",
           "String"       : "TEXT",
           "Date"         : "DATE",
           "OID"          : "LONG",
           "Geometry"     : "BLOB", 
           "BLOB"         : "BLOB"}

def ValidateFieldName(arcpy, name, workspace):
    """This mimics arcpy.ValidateFieldName(), but removes a bug (#NIM064306)
    If the workspace is a feature dataset, then the field name is not
    properly validated. The work around is to validate against the
    geodatabase."""
    if workspace != None:
        #avoid arcpy.describe() it is very expensive
        #desc = arcpy.Describe(workspace)
        #if desc.dataType == "FeatureDataSet":
        #    workspace = desc.path
        #this is a poor solution because '.mdb' and '.gdb' could
        #be anywhere in a valid path, and only by convention do they
        #identify a PGDB and FGDB. Nevertheless, it works most of the time.
        #it is faster to validate against the db than the featuredataset
        workspace = workspace.lower()
        if workspace.rfind(".mdb") > 0:
            workspace = workspace[:workspace.rfind(".mdb")+4]
        else:
            if workspace.rfind(".gdb") > 0:
                workspace = workspace[:workspace.rfind(".gdb")+4]
    return arcpy.ValidateFieldName(name, workspace)

def MakeFieldMap(arcpy, input, workspace):
    #create a simple field mapping from input to workspace
    fields = {}
    for field in input.fields:
        name = field.name
        if (name != input.shapeFieldName and
            name != input.oidFieldName and  #FIXME - we might want this
            name != "Shape_length" and name != "Shape_area" ):
        fields[name] = ValidateFieldName(arcpy, name, workspace)
    #FIXME, it is possible that there are duplicates
    #i.e. a shape file may have a field (not the oid) called OBJECTID
    return fields

def AddFields(arcpy, input, output, fields):
    for field in input.fields:
        arcpy.AddField_management(output, fields[field.name], field.type,
                       field.precision, field.scale, field.length, field.aliasName,
                       field.isNullable, field.required, field.domain)
    
def CopyAttributes(existingRow, newRow, fields):
    """existingRow is a row cursor in the existing table
    newRow is a row in an update cursor on the new table
    fields is a dictionary mapping names in existing to
    names in new"""
    for field in fields:
        newRow.setValue(fields[field], existingRow.getValue(field))

def validateInput():
    # Input feature class
    inFeatureClass = arcpy.GetParameterAsText(0)

    #describe the input features (to get the spatial reference and the type of the idField)
    inFcDescription = arcpy.Describe(inFeatureClass)
    inType = inFcDescription.ShapeType.upper()
    inShapeField = inFcDescription.ShapeFieldName

    # Output feature class
    outFeatureClass = arcpy.GetParameterAsText(1)
    outPath, outName = os.path.split(outFeatureClass)

    #validate output
    #The user can control overwrite or not with Tools->Options->geoprocessing...
    #ArcGIS (toolbox or command line) does not do any validation on the output workspace
    if not arcpy.Exists(outPath):
        raise ValueError("Error: The output workspace does not exist.")

    # Output type - validated as within ['Points','Circles'] by ArcGIS
    outType = arcpy.GetParameterAsText(2)

    minOffset = float(arcpy.GetParameterAsText(3))
    maxOffset = float(arcpy.GetParameterAsText(4))

    #validate min/max
    if (minOffset < 0):
        raise ValueError("Error: The minimum offset must be greater than zero.")
    if (maxOffset <= minOffset):
        raise ValueError("Error: The maximum offset must be greater than the minimum offset")

    nogoAreas = arcpy.GetParameterAsText(5).split(";")
    if nogoAreas[0] == "":
        nogoAreas = [];


def DoWorkxx(pts, max, min = 0, nogo = None, makeCircle = False):
    if nogo and len(nogo) > 0:
        v
    if pts == point
        DoWorkSinglePoint(pts, min, max, nogo, makeCircle)
        return
    if pts == multipoint
        DoWorkMultPoint(pts,  min, max, nogo, makeCircle)
        return
    raise invalid input

def DoWork(pts, min, max, nogo, makeCircle, isMulti):
    if nogo:
        if makeCircle:
            pass
        else:
            pass
    else:
        if makeCircle:
            pass
        else:
            pass



def CreatePoints(arcpy, existing, min, max):
    """existing is a point or multipoint feature class
    min = minimum distance of random point from source point in (0,max)
    max = maximum distance of random point from source point in (min,..)
    returns a feature class called "in_memory\temp". The caller 
    is responsible for deleting this feature class when they are done."""
    newpts = arcpy.FeatureclassToFeatureclass_conversion(existing, "in_memory", "temp")
    pts = arcpy.updateCursor(newpts)
    pt = pts.next()
    while pt != None:
        if multipoint:
            pt.shape = GetRandomizedMpoint(arcpy, pt.shape, min, max)
        else:
            pt.shape = GetRandomizedPoint(arcpy, pt.shape)
        pts.updateRow(pt)
        pt = pts.next()
    del pt, pts
    return newpts
        
def CreateCircles(arcpy, existing, min, max):
    """returns a polygon feature class called "in_memory\circles". The
    caller is responsible for deleting this feature class when they are
    done. See CreatePoints for more information."""
    newpts = CreatePoints(arcpy, existing, min, max)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max)
    arcpy.Delete_management(newpts)
    del newpts
    return circles

def GetRandomizedPoint(geom):
    """ The caller must ensure that point is a arcpy.Point object,
    or else an exception will surely be thrown.
    This routine will return the same point object with the
    X and Y randomly offset."""
    
    # A point can be an array of 1 point, or a single point
    # A multipoint is an array of n (where n > 1) points.
    
    if ((geom == None) or (geom.Type.lower() != "point")):
        return []
    
    arcpy.AddMessage("code pt 1.1.1 (point)")
    pnt = geom.getpart(0)
    arcpy.AddMessage("code pt 1.1.2")
    esri_pt =  arcpy.CreateObject("Point")
    arcpy.AddMessage("code pt 1.1.3")
    while True:
        arcpy.AddMessage("code pt 1.1.3.1")
        newpt = RandomizePoint(pnt.x, pnt.y,minOffset, maxOffset)
        esri_pt.X,esri_pt.Y = newpt
        pt_geom = arcpy.createobject("geometry", "point", esri_pt)
        arcpy.AddMessage("code pt 1.1.3.2")
        if (NotInNoGo(pt_geom,nogoAreas)):
            arcpy.AddMessage("break from 1.1.3.2")
            break
    
    return esri_pt

def GetRandomizedMpoint(geom):
    # A point can be an array of 1 point, or a single point
    # A multipoint is an array of n (where n > 1) points.
    
    if (geom == None) or (geom.Type.lower() not in ["point", "multipoint"]):
        return []
    
    #try:
    arcpy.AddMessage("code pt 1.1.1 (multipoint)")
    pts = arcpy.createobject("Array")
    arcpy.AddMessage("code pt 1.1.2")
    partnum = 0
    partcount = geom.partcount
    arcpy.AddMessage("   part count = " + str(partcount))
    while partnum < partcount:
        arcpy.AddMessage("code pt 1.1.3")
        pnt = geom.getpart(partnum)
        esri_pt =  arcpy.CreateObject("Point")
        arcpy.AddMessage("code pt 1.1.4")
        
        while True:
            newpt = RandomizePoint(pnt.x, pnt.y,minOffset, maxOffset)
            esri_pt.X,esri_pt.Y = newpt
            pt_geom = arcpy.createobject("geometry", "point", esri_pt)
            arcpy.AddMessage("code pt 1.1.4.1")
            if (NotInNoGo(pt_geom,nogoAreas)):
                arcpy.AddMessage("break from 1.1.4.1")
                break

        arcpy.AddMessage("code pt 1.1.5")
        pts.Add(esri_pt)
        arcpy.AddMessage("code pt 1.1.6")
        partnum += 1
    return pts

def RandomizePoint(x,y,r1,r2):
    r = random.uniform(r1,r2)
    phi = random.uniform(0,2*math.pi)
    x2 = x + r*math.cos(phi) 
    y2 = y + r*math.sin(phi)
    return (x2,y2)

if __name__ == '__main__':
    ObscurePoints()


#The rest is garbage    

#clip circles to nogo area
# this is a bad solution.  centroid in no go area will be mostly
# eliminated, leaveing a potentially very small part of the circle
# that is known to contain the "hidden" point.  Need to ensure
# centroid is not in no go area.

#no longer needed
def MakeCircle(pt, radius):
    x,y = RandomizePoint(pt.X,pt.Y,0,radius)
    ptgeom = arcpy.PointGeometry(arcpy.Point(x,y))
    empty = arcpy.geometry()
    circle = arcpy.Buffer_analysis(ptgeom,empty,str(radius))
    return circle
  
#not needed 
def MakeMultiCircle(pt, circle, minOffset, maxOffset, nogoAreas):
    arcpy.AddWarning("Unable to make multi circles from multipoint input")
    return None

def NotInNoGo(pt, FCList):
    arcpy.AddMessage("code pt 1.1.4.1.1")
    if (len(FCList) == 0):
        arcpy.AddMessage("code pt 1.1.4.1.2 - empty fc list")
        return true;
    for fc in FCList:
        arcpy.AddMessage("code pt 1.1.4.1.2")
        if PointInFC(pt, fc):
            arcpy.AddMessage("code pt 1.1.4.1.2 - false")
            return False
    arcpy.AddMessage("code pt 1.1.4.1.3")
    return True

def PointInFC(pt, fc):
    #Currently this is too expensive an operation to do with GP
    # so we ignore the no go area and say it is not in the no go area.
    return false

    outGeom = arcpy.createobject("geometry")
    arcpy.AddMessage("code pt 1.1.4.1.3.1")
    start = time.time()
    arcpy.AddMessage("fc = "+fc+" point = ("+str(pt.getpart(0).X)+","+str(pt.getpart(0).Y)+")")
    # Clip the point geometry object with the area FC.  The 
    #   resulting geometry is in the NewOutGeom list; outGeom is just a placeholder
    #   to indicate that expected output is a geometry object and not a FC
    # Vector Overlay tools:
    #  union, update, symetrical difference - do not accept points
    #  near, intersect - needs a fc not geometry.
    #  clip, spatialJoin - work, but are very slow (953 error problems)
    #  identity - works (very slowly ~1.3 second for 1 pt and 10 rectangles), but also always returns a result
    
    #newOutGeom = arcpy.clip_analysis(pt, fc, outGeom)
    #newOutGeom = arcpy.identity_analysis(pt, fc, outGeom)
    newOutGeom = arcpy.erase_analysis(pt, fc, outGeom)
    #newOutGeom = arcpy.SpatialJoin_analysis(pt, fc, outGeom, "JOIN_ONE_TO_ONE","KEEP_COMMON","#", "IS_WITHIN")
    #newOutGeom = arcpy.Near_analysis(pt, fc, "0")
    arcpy.AddMessage("erase took "+str(time.time() - start)+" sec.")
    arcpy.AddMessage("code pt 1.1.4.1.3.2")
    arcpy.AddMessage("Out Geom = " + str(newOutGeom))
    if (newOutGeom == None or len(newOutGeom) == 0):
        return False
    else:
        return True

def PointInPoly(pt,poly):
    pass


        


