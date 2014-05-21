#! /usr/bin/env python
import numpy as np
boxl = 33.1224947209582 # unit cell dimention for simulation box

def fold_two_vector_with_image(vector1,vector2):
	"""@todo: Docstring for fold_two_vector_with_image.

	:vector1 and vector2: input vectors
	:returns: make sure directions of two vectors are within same simulation box 

	"""
	if len(vector1) != len(vector2):
		raise Exception("Error:two input vector1 and vector2 have different size")	
	for (index,value) in enumerate(vector1):
		while True:
			difference = vector2[index]-value
			if difference < -boxl*0.5:
				vector2[index] = vector2[index] + boxl
			elif difference >= boxl*0.5:
				vector2[index] = vector2[index] - boxl
			else:
				break
	return (vector1,vector2)
def minimum_image(vector1,vector2):
	"""@todo: Docstring for minimum_image.

	:vector1: reference vector
	:vector2: vector to be modified
	:returns: @todo

	"""
	if len(vector1) != len(vector2):
		raise Exception("Error:two input vector1 and vector2 have different size")	
	for (index,value) in enumerate(vector1):
		vector2[index] = vector2[index] - boxl*intround((vector2[index]-value)/boxl)
	return (vector1,vector2)

def angle_between_two_vector(vector1, vector2):
    """@todo: Docstring for angle_between_two_vector.

    :vector1: vector1
    :vector2: vector2
    :ret`urns: return angles between vector1 and vector2 in degree

    """
    if not isinstance(vector1, np.ndarray):
        vector1 = np.asarray(vector1)
    if not isinstance(vector2, np.ndarray):
        vector2 = np.asarray(vector2)
    cosang = np.dot(vector1, vector2)
    sinang = np.linalg.norm(np.cross(vector1, vector2))
    ang_in_radian = np.arctan2(sinang, cosang)
    return np.rad2deg(ang_in_radian)


def relative_position_within_three_point(point0, point1, point2):
    """@todo: Docstring for relative_position_within_three_point.
    calculate the relative position of point0 on the projection to line formed by point1 and point2
    within the plane formed by all three_points
    :point0: external point
    :point1: point1
    :point2: point2
    :returns: 1-by-2 numpy array with x to be the relative x-coordinate of point0 to middle-point of point1 and point2
                                 with y to be the relative y-coordinate(vertical distance of point0 to line of point1 and point2)

    """
    if not isinstance(point0, np.ndarray):
        point0 = np.asarray(point0)
    if not isinstance(point1, np.ndarray):
        point1 = np.asarray(point1)
    if not isinstance(point2, np.ndarray):
        point2 = np.asarray(point2)
    ydist = np.linalg.norm(np.cross((point0 - point1), (
        point0 - point2)))/np.linalg.norm(point2 - point1)
    mid_point12 = (point1 + point2)/2
    mid_0_distance = np.sqrt(np.sum((mid_point12 - point0)**2))
    xdist = np.sqrt(mid_0_distance**2 - ydist**2)
    angle_bw_12_mid0 = angle_between_two_vector(
        (point2 - point1), (point0 - mid_point12))
    if 0 <= angle_bw_12_mid0 <= 90:
        return (xdist, ydist)
    elif 90 < angle_bw_12_mid0 <= 180:
        return (-xdist, ydist)
    elif 180 <= angle_bw_12_mid0 < 270:
        return (-xdist, -ydist)
    else:
        return (xdist, -ydist)


def intround(float_data):
    """@todo: Docstring for intround.

    :float_data: @todo
    :returns: @todo

    """
    y = round(float_data)-0.5
    return int(y) + (y > 0.5)
if __name__ == '__main__':
    # ormal(size=(3, 3))
    # coup #1,line 4
    l = 33.1224947209582
    points = [[-21.19598,       -5.00070,       -30.15988],
              [-24.95235,        -4.80013,       -30.24322],
              [-21.19598,        -5.00070,       -30.15988]
              ]
    points = [[-15.95037,        -1.61843,        28.47131],
              [-24.95235,        -4.80013,       -30.24322],
              [-21.19598,        -5.00070,       -30.15988]
              ]
# coup 201,line 203
#	points = [[-26.75702,       -19.91551,        -3.46400  ],
#		  [-24.95235,        -4.80013,       -30.24322],
#		  [-21.19598,        -5.00070,       -30.15988]
#		 ]
#
#	points = [[ -26.07582,        20.72822,        29.35980],
#		  [-24.95235,        -4.80013,       -30.24322],
#		  [-21.19598,        -5.00070,       -30.15988]
#		 ]
    (x, y) = relative_position_within_three_point(
        points[0], points[1], points[2])
    #(points[1],points[0]) = fold_two_vector_with_image(points[1],points[0])
    (points[1],points[0]) = minimum_image(points[1],points[0])
    print points
    #(points[2],points[0]) = fold_two_vector_with_image(points[2],points[0])
    (points[2],points[0]) = minimum_image(points[2],points[0])
    print points
    (x, y) = relative_position_within_three_point(
        points[0], points[1], points[2])
    print x, y
