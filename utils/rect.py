from numpy as np
class rect(object):
    def __init__(self, top_corner = None , width = 0, height = 0, ouverture = 60):
        if top_corner and width and height :
            self._x0 = top_corner[0]
            self._y0 = top_corner[1]
            self._width = width
            self._height = height
            self._ouverture = ouverture

        if width and height :
            self._width = width
            self._height = height
            self._x0 = width / 2
            self._y0 = height / 2
            self._ouverture = ouverture 

         
    def Compute4Corner1StRect(self):
        if (width != 0) and (height != 0):
            # point 1 - top left
            x1 = _x0 - self._width / 2
            y1 = _y0 + self._height / 2
            # point 2 - top right
            x2 = _x0 + self._width / 2
            y2 = _y0 + self._height / 2
            # point 3 - bottom right 
            x3 = _x0 + self._width / 2
            y3 = _y0 - self._height / 2
            # point 4 - bottom left
            x4 = _x0 - self._width / 2
            y4 = _y0 - self._heigth / 2

            self._tab_point_1st_rect = [Point(x1, y1), Point(x2, y2), 
                    Point(x3, y3), Point(x4, y4)]

    def Compute4Corner2NdRect(self, delta_width = 90, delta_heigth = 60):
        if (delta_width > 50) and (delta_heigth > 50):
            self._delta_width = delta_width
            self._delta_heigth = delta_heigth
        if (_tab_point_1st_rect.count() != 0):
            # point 1 - top left
            x1 = _x0 - self._delta_width / 2
            y1 = _y0 + self._delta_heigth / 2
            # point 2 - top right
            x2 = _x0 + self._delta_width / 2
            y2 = _y0 + self._delta_heigth / 2
            # point 3 - bottom right 
            x3 = _x0 + self._delta_heigth / 2
            y3 = _y0 - self._delta_heigth / 2
            # point 4 - bottom left
            x4 = _x0 - self._delta_width / 2
            y4 = _y0 - self._delta_heigth / 2
            
            self._tab_point_2nd_rect = [Point(x1, y1), Point(x2, y2),
                    Point(x3, y3), Point(x4, y4)]

    def ComputeABDroite(self, P1, P2):
        a = (P2.y - P1.y) / (P2.x - P1.x)
        b = P1.y - P1.y - P1.x * a

        return(a,b)

    def ComputePtOn2ndForCam(self, num_cam):
        num_corner = GiveAssociateCorner( num_cam)
        #get le sens of rotation
        ouverture = _ouverture * GiveRotationSens(num_cam)
        point_cam = _tab_point_2nd_rect[num_cam]
        point_corner = _tab_point_1st_rect[num_corner]
        a, b = ComputeABDroite(point_cam, point_corner)
        yp = _tab_point_2nd_rect[num_corner].y
        xp = (yp -b ) / a
        # compute transform xp,yp with rotation of aperture
        # with center point_cam
        # translation matrix
        T = np.matrix([[1, 0, -1*point_cam.x], [0, -1*point_cam.y, -1],
            [0, 0, 1]])
        # rotation matrix
        R = np.matrix(
                [[np.cos(np.radian(_ouverture)), -1 * np.sin(np.radian(_ouverture)), 0],
                [np.sin(np.radian(ouverture)), np.cos(np.radian(ouverture)), 0], 
                [0, 0, 1]])
        #compute Trt
        Trt = R * T
        # place point to transform in a matrix
        X = np.matrix(xp, yp, 1)
        Xrt = T * X
        point_tr = Point(Xrt[0,0], Xrt[0,1])
        # compute line equation of other support line of aperture
        atr, btr = ComputeABDroite(point_cam, point_tr)
        xpp = -1 * _tab_point_2nd_rect[num_cam].x
        ypp = atr * xpp + btr

        point_p = Point(xp, yp)
        point_pp = Point(xpp, ypp)
        cam_rtn = Cam(num_cam, point_p, point_pp)

        return cam_rtn
       
        
    def GiveAssociateCorner(self, num_cam):

        if num_cam = 1 :
            return 4
        if num_cam = 2 :
            return 3
        if num_cam = 3 :
            return 2
        if num_cam = 4 :
            return 1

    def GiveRotationSens(self, num_cam):

        if num_cam = 1 :
            return 1
        if num_cam = 2 :
            return -1
        if num_cam = 3 :
            return 1
        if num_cam = 4 :
            return -1


class Point(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

class Cam(object):
    def __init__(self, num_cam, p_plan, pp_plan):
        self._num_cam = num_cam
        self._p_plan = p_plan 
        self._pp_plan = pp_plan 

