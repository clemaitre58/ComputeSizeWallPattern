from utils.rect import Point, Rect, Cam
import numpy as np
# construction objet rect
centre = Point(0, 0)
mon_rect = Rect(centre, width = 170, height = 100, ouverture = 60)
mon_rect.compute_corners_rect_1()
mon_rect.compute_corners_rect_2(90, 60)

list_cam = []

for i in range(4):
    list_cam.append(mon_rect.ComputePtOn2ndForCam(i+1))

for i in range(4):
    if i < 3:
        if i % 2 == 0:
            distance = np.abs(list_cam[i]._p_plan.x - list_cam[i+1]._p_plan.x)
        else :
            distance = np.abs(list_cam[i]._p_plan.y - list_cam[i+1]._p_plan.y)
        print "Couple de camera : " + str(i) + "-" + str(i+1) + " distance : " + str(distance)
    if i == 3:
        distance = np.abs(list_cam[i]._p_plan.y - list_cam[0]._p_plan.y)
        print "Couple de camera : " + str(i) + "-" + str(0) + " distance : " + str(distance)
