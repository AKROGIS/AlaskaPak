# -*- coding: utf-8 -*-
"""
Create a feature class by building the geometry from a table and points.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import arcpy

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
else:
    # for use as a module and Python toolboxes (*.pyt)
    from . import utils


def get_points(featureclass, id_field):
    """Return the coordinate pairs of the points in `feature class`, keyed to
    the id in `id_field`.

    Args:
        featureclass (str): An ArcGIS datasource or layerview path to a table
            of points
        id_field (str): The column of the table that contains the unique
            identifier for the coordinates in that row of the table.

    Returns:
        dict[any, (double, double)]: A lookup table to an (x,y) coordinate pair
        given a point id.  The point id can be a string or int, or even date

    Notes:
        It is faster to search the points once and cache the results, than to
        search the points feature class for each geometry created.
    """
    points = {}
    fields = [id_field, "SHAPE@XY"]
    with arcpy.da.SearchCursor(featureclass, fields) as cursor:
        for row in cursor:
            pt_id = row[0]
            xy_pair = row[1]
            if pt_id is not None:
                points[pt_id] = xy_pair
    return points


def make_shape(shape_type, points):
    """Creates an ArcGIS `shape_type` geometry with `points` as vertices.

    Args:
        shape_type (str): An ArcGIS geometry type; one of `polygon`, `polyline`,
            or `multipoint`
        points (list[(double,double)]): An ordered list of coordinate pairs.

    Returns:
        arcpy.Geometry: A new geometry object, or None if an unknown shape_type
            or an empty points list are provided.

    Raises:
        arcpy.ExecuteError: If it cannot build the requested geometry from the
            list of points.
    """
    # Geometry constructors need an arcpy object not a python list
    points = arcpy.Array([arcpy.Point(*coords) for coords in points])
    if not points:
        return None
    if shape_type == "multipoint":
        return arcpy.Multipoint(points)
    if shape_type == "polyline":
        return arcpy.Polyline(points)
    if shape_type == "polygon":
        return arcpy.Polygon(points)
    return None


def parameter_fixer(args):
    """Validates and transforms the command line arguments for the task.

    1) Converts text values from old style toolbox (*.tbx) parameters (or the
       command line) to the python object arguments expected by the primary task
       of the script, and as provided by the new style toolbox (*.pyt).
    2) Validates the correct number of arguments.
    3) Provides default values for command line options provided as "#"
       or missing from the end of the command line.
    4) Provides additional validation for command line parameters to match the
       validation done by the toolbox interface.  This isn't required when
       called by an old style toolbox, but it isn't possible to tell it is
       called by the toolbox or by the command line.

    Args:
        args (list[text]): A list of commands arguments, Usually obtained
        from the sys.argv or arcpy.GetParameterAsText().  Provide "#" as
        placeholder for an unspecified intermediate argument.

    Returns:
        A list of validated arguments expected by the task being called.
        Exits with an error message if the args cannot be transformed.
    """

    if len(args) != 6:
        usage = (
            "Usage: {0} shape_table vertex_list point_features "
            "point_id_name shape_type output_features"
        )
        utils.die(usage.format(sys.argv[0]))

    table = args[0]
    vertex_list = args[1]
    point_feature_class = args[2]
    point_id_field = args[3]
    shape_type = args[4]
    out_feature_class = args[5]

    # validate table
    if not arcpy.Exists(table):
        msg = "shape_table ({0}) does not exist."
        utils.die(msg.format(table))

    # nothing to do with vertex_list

    # validate shape_type
    shape_type = shape_type.lower()
    if shape_type == "#":
        utils.info("Building a the default shape type of 'polyline'.")
        shape_type = "polyline"
    if shape_type not in ["polyline", "polygon", "multipoint"]:
        msg = (
            "shape_type of '{0}' not understood. Use one of "
            "'Polyline', 'Polygon', 'Multipoint', or '#'"
        )
        utils.die(msg.format(shape_type))

    # validate point_feature_class
    if not arcpy.Exists(point_feature_class):
        msg = "point_features ({0}) does not exist."
        utils.die(msg.format(point_feature_class))

    shape = arcpy.Describe(point_feature_class).shapeType
    if shape.lower() != "point":
        msg = "{0} is a {1} not a point feature class."
        utils.die(msg.format(point_feature_class, shape))

    # validate point_id_field
    point_field_names = [field.name for field in arcpy.ListFields(point_feature_class)]
    if point_id_field not in point_field_names:
        msg = "point_id_name ({0}) is not a field in {1}."
        utils.die(msg.format(point_id_field, point_feature_class))

    # validate out_feature_class
    workspace, _ = os.path.split(out_feature_class)
    if not workspace:
        workspace = os.getcwd()
        out_feature_class = os.path.join(workspace, out_feature_class)
    if not arcpy.Exists(workspace):
        msg = "The destination workspace '{0}' does not exist."
        utils.die(msg.format(workspace))
        sys.exit()

    return [
        table,
        vertex_list,
        point_feature_class,
        point_id_field,
        shape_type,
        out_feature_class,
    ]


def get_vertex_names(vertex_list, shape_type, sep=";"):
    """Returns an ordered list of field names holding vertex ids.

    Args:
        vertex_list (str): The field names separated by sep. The items in the
            list do not need to be unique.
        shape_type (str): If shape_type is "polygon", then the polygon is closed.
            i.e. the last item is the same as the first item.
        sep (str, optional): The character separating the individual
            values in the string. Defaults to ";".

    Returns:
        list[str]: A list of field names.
    """
    vertex_names = vertex_list.split(sep)
    # remove empty ids i.e. ";;"
    vertex_names = list(filter(lambda x: x, vertex_names))
    if vertex_names and shape_type == "polygon":
        closed = vertex_names[0] == vertex_names[-1]
        if not closed:
            # close it
            vertex_names.append(vertex_names[0])
    return vertex_names


def verify_vertex_count(vertex_names, shape_type):
    """Exit with an error message if the vertex count is not correct.

    The minimum number of unique vertices is 1 for Multipoint (strange but
    allowed), 2 for Polyline, and 3 for Polygon.

    Args:
        vertex_names (list[str]): An ordered list of field names holding vertex ids.
        shape_type (str): An ArcGIS geometry type; one of `polygon`, `polyline`,
            or `multipoint`.

    Returns:
        None
    """

    unique_vertex_count = len(set(vertex_names))
    if shape_type == "polygon" and unique_vertex_count < 3:
        utils.die("Polygons must have at least three unique vertices")
    if shape_type == "polyline" and unique_vertex_count < 2:
        utils.die("Polylines must have at least two vertices")
    if shape_type == "multipoint" and unique_vertex_count < 1:
        utils.die("Multipoints must have at least one vertex")


def verify_vertex_names(vertex_names, table):
    """Exit with an error message if the vertex names are not valid.

    A valid vertex name must exist as a column name in table.

    Args:
        vertex_names (list[str]): An ordered list of field names holding vertex ids.
        table (str): An ArcGIS path to an existing table view.

    Returns:
        None
    """
    # verify vertex names exist in input table
    table_field_names = [field.name for field in arcpy.ListFields(table)]
    missing_ids = set(vertex_names) - set(table_field_names)
    if missing_ids:
        msg = "The following fields {0} were not found in {1}."
        utils.die(msg.format(missing_ids, table))


def verify_vertex_types(vertex_names, table, point_feature_class, point_id_field):
    """Exit with an error message if the vertex types are not valid.

    All types of all vertex fields in table must be the same and must
    match the type of the `point_id_field` in the `point_feature_class`.

    Args:
        vertex_names (list[str]): An ordered list of field names holding vertex ids.
        table (str): An ArcGIS path to an existing table view.
        point_feature_class (str): An ArcGIS path to an existing point feature class.
        point_id_field (str): The name of a field in `point_feature_class`.

    Returns:
        None
    """
    point_fields = arcpy.ListFields(point_feature_class)
    point_id_types = [
        field.type for field in point_fields if field.name == point_id_field
    ]
    if not point_id_types:
        msg = "The point id field '{0}' was not found in {1}."
        utils.die(msg.format(point_id_field, point_feature_class))
    table_fields = arcpy.ListFields(table)
    vertex_field_types = [
        field.type for field in table_fields if field.name in vertex_names
    ]
    unique_field_types = set(vertex_field_types)
    if len(unique_field_types) != 1:
        msg = "All vertex types '{0}' must be the same."
        utils.die(msg.format(unique_field_types))
    if point_id_types[0] != vertex_field_types[0]:
        msg = "All point id type '{0}' must match the vertex field type {1}."
        utils.die(msg.format(point_id_types[0], vertex_field_types[0]))


def table_to_shape(
    table,
    vertex_list,
    point_feature_class,
    point_id_field,
    shape_type,
    out_feature_class,
    validate=False,
):
    """Creates a feature class by building the geometry from the table and points.

    Args:
        table (str): An ArcGIS path to an existing table view
        vertex_list (str): A semicolon separated list of vertex field names.
            A vertex name is a column name in `table` the value in the column
            is a vertex id in the `point_id_field` column of `point_feature_class`
            The shape `point_feature_class` provides one of the vertices in the
            generated geometry.
        point_feature_class (str): An ArcGIS path to an existing point feature class.
        point_id_field (str): The name of the field in `point_feature_class`
            that contains the vertex id.
        out_feature_class (str): An ArcGIS data source path where the generated
            feature class will be stored.
        shape_type (str): Specifies the type of geometry to create. One of
            `polygon`, `polyline`, or `multipoint`
        validate (bool, optional): If `True` additional validation will be
            performed before starting the work.  This can be useful to ensure
            up front that the input parameters meet expectations.  However it
            does take more time, and can produce false positives. Defaults to
            `False`.

    Returns:
        None
    """

    # pylint: disable=too-many-arguments,too-many-locals

    vertex_names = get_vertex_names(vertex_list, shape_type)
    if validate:
        verify_vertex_count(vertex_names, shape_type)
        verify_vertex_names(vertex_names, table)
        verify_vertex_types(vertex_names, table, point_feature_class, point_id_field)

    # Create an in memory feature class for the output.
    spatial_reference = arcpy.Describe(point_feature_class).SpatialReference
    temp_fc = arcpy.CreateFeatureclass_management(
        "in_memory",
        "temp_fc",
        shape_type,
        "",
        "DISABLED",
        "DISABLED",
        spatial_reference,
    )

    # Need the database to verify the field name is valid
    database = utils.get_database(out_feature_class)
    # create matching lists of input and output field names.
    # need field lists for the search and insert cursors.
    in_field_names = []
    out_field_names = []
    for field in arcpy.ListFields(table):
        name = field.name
        if (
            # field.type not in ["OID", "Geometry", "GlobalID", "Blob", "Raster"]
            field.type not in ["OID", "Geometry"]
            and name not in vertex_names
            and field.editable  # skip un-editable fields like Shape_Length
        ):
            new_name = utils.valid_field_name(name, database)
            # Schema lock is not required for an in-memory feature class
            arcpy.AddField_management(
                temp_fc,
                new_name,
                utils.type_map[field.type],
                field.precision,
                field.scale,
                field.length,
                field.aliasName,
                field.isNullable,
                field.required,
                field.domain,
            )
            in_field_names.append(name)
            out_field_names.append(new_name)

    utils.info("Reading Points database")
    points = get_points(point_feature_class, point_id_field)

    utils.info("Reading table")
    table_fields = vertex_names + in_field_names
    out_fields = ["SHAPE@"] + out_field_names
    vertex_count = len(vertex_names)
    out_cursor = arcpy.da.InsertCursor(temp_fc, out_fields)
    with arcpy.da.SearchCursor(table, table_fields) as cursor:
        for row in cursor:
            vertex_ids = row[:vertex_count]
            attributes = row[vertex_count:]
            try:
                geom_pts = [points[pt_id] for pt_id in vertex_ids]
                geometry = make_shape(shape_type, geom_pts)
            except KeyError:
                utils.warn("Invalid point id, skipping")
                geometry = None
            except arcpy.ExecuteError:
                utils.warn("Unable to create geometry, skipping")
                geometry = None
            if geometry is None:
                msg = "  Vertex info: {0} = {1}"
                utils.warn(msg.format(vertex_names, vertex_ids))
            else:
                # arcpy.da row is a tuple, not a list
                new_row = (geometry,) + attributes
                out_cursor.insertRow(new_row)

    del out_cursor

    utils.info("Saving in memory feature class to {0}".format(out_feature_class))
    # feature_set = arcpy.FeatureSet(temp_fc)
    feature_set = arcpy.FeatureSet()
    feature_set.load(temp_fc)
    feature_set.save(out_feature_class)
    utils.info("Done.")


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["TODO: develop test case"]
    utils.execute(table_to_shape, parameter_fixer)
