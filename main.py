from utils.rect import Rect

#construction objet rect
mon_rect = Rect(width = 170, height = 100, ouverture = 60)
mon_rect.compute_corners_rect_1()
mon_rect.compute_corners_rect_2(90, 60)

list_cam = []

for i in range(4):
    list_cam.append(mon_rect.ComputePtOn2ndForCam(i+1))

