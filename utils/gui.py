from skimage.draw import line
import skimage.io as io
from utils.rect import Rect, Point, Cam
import numpy as np
import matplotlib.pyplot as plt
def draw_all_cam(cam, width, height):
    coul_line = ['b-', 'r-', 'g-', 'c-']
    coul_circle = ['b', 'r', 'g', 'c']
    i = 0
    for elt in cam :
        x0 = elt.p_cam.x
        y0 = elt.p_cam.y
        x1 = elt._p_plan.x
        y1 = elt._p_plan.y
        x2 = elt._pp_plan.x
        y2 = elt._pp_plan.y
        #print "x1 : " + str(x1) + " x2 : " + str(y1) + " x0 : " + str(x0) + "y0 : " + str(y0)
        plt.plot([x0, x1], [y0, y1], coul_line[i], lw=2)
        plt.plot([x0, x2], [y0, y2], coul_line[i], lw=2)
#        circ_cam = plt.Circle((x0, y0), 2, coul_line[i])
        cir_cam = plt.Circle((x0, y0), width/10, color = coul_circle[i])
        i = i+1
        ax = plt.gca()
        ax.add_artist(cir_cam)
    plt.show()
