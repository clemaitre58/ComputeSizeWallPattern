from utils import *

#construction objet rect
mon_rect = rect(width = 170, heigth = 100, ouverture = 60)
mon_rect.Compute4Corner1StRect()
mon_rect.Compute4Corner2NdRect(90,60)

list_cam = []

for i in range(4):
    list_cam.append(ComputePtOn2ndForCam(i))

