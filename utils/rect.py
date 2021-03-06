from __future__ import division, print_function
import numpy as np


def compute_line(p1, p2):
    """Compute a line passing by 2 Points

    Parameters
    ----------
    p1 : Point,
        First point.

    p2 : Point,
        Second point.

    Returns
    -------
    a : float,
        Slope.

    b : float,
        Intercept.

    """
    a = (p2.y - p1.y) / (p2.x - p1.x)
    b = p1.y - p1.y - p1.x * a

    return a, b


class Rect(object):
    """A rectangle class

    Parameters
    ----------
    center : Point or None, optional (default=None)
        A 2d point representing the center of the rectangle.

    width : float, optional (default=0)
        The width of the rectangle.

    height : float, optional (default=0)
        The height of the rectangle.

    ouverture : float, optional (default=60)
        The opening of the rectangle

    Attributes
    ----------
    """

    def __init__(self, center=None, width=0, height=0, ouverture=60):
        if center is None:
            self._width = float(width)
            self._height = float(height)
            self._center = Point(self._width / 2, self._height / 2)
            self._ouverture = float(ouverture)
        else:
            self._center = center
            self._width = float(width)
            self._height = float(height)
            self._ouverture = float(ouverture)

    def _compute_corners(self, width, height):
        """Compute the corners of the rectangle given width and height

        Parameters
        ----------
        width : float,
            Width.

        height : float,
            Height

        Returns
        -------
        corners : list of 4 Points,
            The list of corners: top-left, top-right, bottom-right, and
            bottom-left

        """
        if width > 0 and height > 0:
            # top-left
            p1 = self._center + Point(-width / 2, height / 2)
            # top-right
            p2 = self._center + Point(width / 2, height / 2)
            # bottom-right
            p3 = self._center + Point(width / 2, -height / 2)
            # bottom-left
            p4 = self._center + Point(-width / 2, -height / 2)
        else:
            raise ValueError('width and height should > 0, got'
                             ' width={} / height={}'.format(self.width,
                                                            self.height))
        return [p1, p2, p3, p4]

    def compute_corners_rect_1(self):
        """Compute the first rectangle

        Parameters
        ----------

        Returns
        -------

        """

        self._corners_rect_1 = self._compute_corners(self._width, self._height)

        return self._corners_rect_1

    def compute_corners_rect_2(self, delta_width=90, delta_height=90):
        """Compute the second rectangle

        Parameters
        ----------
        delta_height : float, optional (default=90)
            Delta height.

        delta_width : float, optional (default=90)
            Delta width.

        Returns
        -------

        """
        if delta_width > 50 and delta_width > 50:
            p1 = Point(
                    self._corners_rect_1[0].x - delta_width,
                    self._corners_rect_1[0].y + delta_height,
                    )

            p2 = Point(
                    self._corners_rect_1[1].x + delta_width,
                    self._corners_rect_1[1].y + delta_height,
                    )

            p3 = Point(
                    self._corners_rect_1[2].x + delta_width,
                    self._corners_rect_1[2].y - delta_height,
                    )

            p4 = Point(
                    self._corners_rect_1[3].x - delta_width,
                    self._corners_rect_1[3].y - delta_height,
                    )

        self._corners_rect_2 = [p1, p2, p3, p4]
        return self._corners_rect_2

    def ComputePtOn2ndForCam(self, num_cam):
        num_corner = self.GiveAssociateCorner(num_cam)
        #get le sens of rotation
        ouverture = int(self._ouverture) * int(self.GiveRotationSens(num_cam))
        point_cam = self._corners_rect_2[num_cam-1]
        point_corner = self._corners_rect_1[num_corner-1]
        a, b = compute_line(point_cam, point_corner)
        yp = self._corners_rect_2[num_corner-1].y
        xp = (yp -b ) / a
        # compute transform xp,yp with rotation of aperture
        # with center point_cam
        # translation matrix
        T_moins = np.matrix([[1, 0, -point_cam.x], [0, 1, -point_cam.y],
            [0, 0, 1]])
        T_plus = np.matrix([[1, 0, point_cam.x], [0, 1, point_cam.y],
            [0, 0, 1]])
        # rotation matrix
        R = np.matrix(
                [[np.cos(np.radians(ouverture)), -1
                    * np.sin(np.radians(ouverture)), 0],
                [np.sin(np.radians(ouverture)),
                    np.cos(np.radians(ouverture)), 0],
                [0, 0, 1]])
        #compute Trt
        Trt = T_plus * R * T_moins

        # place point to transform in a matrix
        X = np.matrix([[xp], [yp], [1]])
        Xrt = Trt * X
        point_tr = Point(Xrt[0, 0], Xrt[1, 0])
        # compute line equation of other support line of aperture
        atr, btr = compute_line(point_cam, point_tr)
        xpp = -1 * self._corners_rect_2[num_cam-1].x
        ypp = atr * xpp + btr

        point_p = Point(xp, yp)
        point_pp = Point(xpp, ypp)
        cam_rtn = Cam(num_cam, point_cam, point_p, point_pp)
        cam_rtn.a = a
        cam_rtn.b = b
        cam_rtn.ap = atr
        cam_rtn.bp = btr
        return cam_rtn


    def GiveAssociateCorner(self, num_cam):

        if num_cam == 1:
            return 4
        if num_cam == 2:
            return 3
        if num_cam == 3:
            return 2
        if num_cam == 4:
            return 1

    def GiveRotationSens(self, num_cam):

        if num_cam == 1:
            return 1
        if num_cam == 2:
            return -1
        if num_cam == 3:
            return 1
        if num_cam == 4:
            return -1


class Point(object):
    """Define a 2d point

    Parameters
    ----------
    x : float,
        x coordinate.

    y : float,
        y coordinate.

    Attributes
    ----------
    """
    def __init__(self, x, y):
        """Constructor by default"""
        self._x = float(x)
        self._y = float(y)

    @classmethod
    def from_point(cls, point):
        """Constructor using a Point

        You can construct a point with `p = Point.from_point(Point(1, 1))`
        """
        cls._x = point.x
        cls._y = point.y

    @property
    def x(self):
        """Getter for x

        Since that _x is kinda of protected, this is property to have
        read-only access on _x. So you can do p.x to read but you cannot
        not do p.x = 1.
        """
        return self._x

    @property
    def y(self):
        """Getter for y"""
        return self._y

    def __add__(self, other):
        """This is the add operator"""
        if isinstance(other, Point):
            return Point(self._x + other.x, self._y + other.y)
        else:
            NotImplemented

    def __sub__(self, other):
        """This is the subtract operator"""
        if isinstance(other, Point):
            return Point(self._x - other.x, self._y - other.y)
        else:
            NotImplemented

    def __repr__(self):
        """This the representation if you put `p` in command line"""
        return '({}, {})'.format(self._x, self._y)

    def __str__(self):
        """This the string which is shown while `print(p)`"""
        return 'Point: (x={}, y={})'.format(self._x, self._y)


class Cam(object):
    def __init__(self, num_cam, p_cam, p_plan, pp_plan):
        self._num_cam = num_cam
        self._p_cam = p_cam
        self._p_plan = p_plan
        self._pp_plan = pp_plan
        self._a = 0.0
        self._b = 0.0
        self._bp = 0.0
        self._ap = 0.0

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def ap(self):
        return self._ap

    @property
    def bp(self):
        return self._bp
    @property
    def num_cam(self):
        return self._num_cam

    @property
    def p_cam(self):
        return self._p_cam

    @a.setter
    def a(self, value):
        self._a = value

    @b.setter
    def b(self, value):
        self._b = value

    @ap.setter
    def ap(self, value):
        self._ap = value
        
    @bp.setter
    def bp(self, value):
        self._bp = value
    
    @num_cam.setter
    def num_cam(self, value):
        self._num_cam = value
    
    @p_cam.setter
    def p_cam(self, value):
        self._p_cam = value
