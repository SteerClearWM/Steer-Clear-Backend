import shapefile

import os
"""
SteerClearGISClient
-------------
Class for checking if a given lat/long coord is
within a polygon
"""
class SteerClearGISClient():

    """
    Creates a new SteerClearGIS instance

    :campus_map_filename: File path to the shapefile
                          containing the campus map GIS info
    """
    def __init__(self, campus_map_filename):
        # read shapefile data
        sf = shapefile.Reader(campus_map_filename)

        # get campus map shape
        shape = sf.shapes()[0]

        # save campus polygon
        self.campus_polygon = shape.points

    """
    is_on_campus
    ------------
    Checks if a given lat/long point is on campus

    :point: lat/long point tuple
    """
    def is_on_campus(self, point):
        x, y = point
        return self.point_in_poly(y, x, self.campus_polygon)

    """
    point_in_poly
    -------------
    Algorithm to solve the point in polygon problem

    :x:         longitude of point
    :y:         latitude of point
    :polygon:   list of lat/long pairs
    """
    def point_in_poly(self, x, y, poly):

        # check if point is a vertex
        if (x,y) in poly: 
            return True

        # check if point is on a boundary
        for i in range(len(poly)):
            p1 = None
            p2 = None
            if i==0:
                p1 = poly[0]
                p2 = poly[1]
            else:
                p1 = poly[i-1]
                p2 = poly[i]
            if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
                return True
            
        n = len(poly)
        inside = False

        # draws ray from outside polygon to the point
        # counts how many times the ray crosses the boundary of the polygon
        # if the number of crosses is odd, the point is inside the polygon
        # if the number of crosses is even, the point is outside the polygon
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside