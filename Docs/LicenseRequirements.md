# License Level Requirements

ArcGIS comes in three license levels: Basic, Standard and Advanced. These
use to be called ArcView, ArcEditor and ArcInfo. You may see references
to these older names in the comments in the code.  The following has been
checked for Desktop 10.3+ and Pro 2.6+

## Add-In Tools

The following commands require more than a Basic license. For each command I
have referenced the builtin geo processing tool(s) responsible for the license
escalation.

### Conversions/Point To Polygon

* license: **Advanced**
* class file: `PointToPolygon.cs`
* python tool: `Point2Poly.py`

### Conversions/Polygon To Point

* license: **Advanced**
* class file: `PolygonToPoint.cs`
* builtin: `FeatureVerticesToPoints_management`

### Grids/Generate Grid Points

* license: **Advanced**
* class file: `GenerateGridPoints.cs`
* builtin: `FeatureToPoint_management`

### Randomize/Obscure Points

* license: **Advanced** (only if using `No Go` or `Must Go` areas)
* class file: `ObscurePoints.cs`
* python tool: `ObscurePoints.py`

### Randomize/Random Points

* license: **Advanced** or **Spatial Analyst**, or **3D Analyst**
* class file: `RandomPoints.cs`
* builtin: `CreateRandomPoints_management`

## Python Tools

For each script/tool I have listed any builtin geo processing commands that it
calls and the license level for those builtin commands.


### `AddArea.py`

* license: **Basic**
* builtin: `AddField_management`: **Basic**
* builtin: `CalculateField_management`: **Basic**

### `AddID.py`

* license: **Basic**
* builtin: `AddField_management`: **Basic**

### `AddLength.py`

* license: **Basic**
* builtin: `AddField_management`: **Basic**
* builtin: `CalculateField_management`: **Basic**

### `Line2Rect.py`

* license: **Basic**
* builtin: `CreateFeatureclass_management`: **Basic**

### `ObscurePoints.py`

* license: **Advanced** (only if using `No Go` or `Must Go` areas)
* builtin: `FeatureClassToFeatureClass_conversion`: **Basic**
* builtin: `Delete_management`: **Basic**
* builtin: `Buffer_analysis`: **Basic** (as used in script)
* builtin: `Clip_analysis`: **Basic**
* builtin: `DeleteField_management`: **Basic**
* builtin: `JoinField_management`: **Basic**

In the `CreateLimitedPoints` function:

* builtin: `Erase_analysis`: **Advanced**
* builtin: `CreateRandomPoints_management`: **Advanced** or
  **Spatial Analyst**, or **3D Analyst**

### `Point2Poly.py`

* license: **Advanced**
* builtin: `PointsToLine_management`: **Basic**
* builtin: `FeatureToPolygon_management`: **Advanced**

### `Point2Poly2.py` (and `Point2Poly3.py`)

* license: **Basic**
* builtin: `CreateFeatureclass_management`: **Basic**
* builtin: `AddField_management`: **Basic**
* builtin: `Delete_management`: **Basic**

### `RandomTransects.py`

* license: **Basic**
* builtin: `CreateFeatureclass_management`: **Basic**

### `SquareBuilding.py`

* license: **Basic**
* builtin: `CopyFeatures_management`: **Basic**
* builtin: `AddField_management`: **Basic**
* builtin: `CalculateField_management`: **Basic**
* builtin: `DeleteField_management`: **Basic**
* python tool: `Line2Rect.py` **Basic**

### `Table2Shape.py`

* license: **Basic**
* builtin: `CreateFeatureclass_management`: **Basic**
* builtin: `AddField_management`: **Basic**
