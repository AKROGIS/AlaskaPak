# ---------------------------------------------------------------------------
# LongestAxis.py
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

#Create the geoprocessing objectf
gp = arcgisscripting.create(9.3)

# Input feature class
inFeatureClass = gp.GetParameterAsText(0)

#describe the input features (to get the spatial reference and the type of the idField)
inFcDescription = gp.Describe(inFeatureClass)
#inType = inFcDescription.ShapeType.upper()
#inShapeField = inFcDescription.ShapeFieldName

# Output feature class
outFeatureClass = gp.GetParameterAsText(1)
outPath, outName = os.path.split(outFeatureClass)

#validate output
#The user can control overwrite or not with Tools->Options->geoprocessing...
#ArcGIS (toolbox or command line) does not do any validation on the output workspace
if not gp.Exists(outPath):
    raise ValueError("Error: The output workspace does not exist.")

name = gp.GetParameterAsText(2)
if (name == None or name == ""):
    name = "MaxAxis"

def MaxAxis(geom):
    return max(geom.Extent.Width,geom.Extent.Height)

def AddMaxAxis(fc):
    features = gp.UpdateCursor(fc)
    feature = features.Next()
    while feature != None:
        axis = MaxAxis(feature.Shape)
        #gp.AddMessage("length = "+ str(axis))
        feature.SetValue(name,axis)
        features.UpdateRow(feature)
        feature = features.Next()

def MakeNewFC():
    #gp.CreateFeatureclass_management(outPath, outName, "POLYGON", inFeatureClass, "#", "SAME_AS_TEMPLATE")
    gp.CopyFeatures_management (inFeatureClass, outFeatureClass)
    gp.AddField_management(outFeatureClass, name, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
MakeNewFC()
AddMaxAxis(outFeatureClass)


#New Brute Force Algorithm:
#
# for poly in polygons:
#  n = number of vertices
#  max = 0;
#  for v1 = range(0 to n-4):
#   for v2 = range(v1+2 to n-1):
#    line = create line from v1 to v2
#    dist = length of line
#    if max < dist:
#     if line is completely within poly:
#      max = dist
#  store max as attribute in poly
   
# Checking for line within poly for every line is probably very very expensive,
# and cannot be done effectively in python.  Use arcobjects
