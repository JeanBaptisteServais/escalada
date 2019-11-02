import os
import cv2
"""
-        On this picture, we have two backgrounds. The bottom of the
    picture and the top of the picture. It is because the wall have 2
    differents colors. The blue and the green.

-        We try to delete the background  and recup only the holds
    by the wall_parameters parameters.

    For this we are based on contours. We delete the big and litlle
    contours for the top side.

    For the bottom we recup the max contour who's moutains pics of
    the picture and re-operate the filtering of contours.

"""



import numpy as np

from pictures_function import open_picture
from pictures_function import show_picture
from pictures_function import blanck_picture


def first_operation_picture(path_picture):

    #Resize picture to 500x500.
    img = cv2.resize(open_picture(path_picture), (500, 500))
    #show_picture("img", img, 0, "")

    #We delete the ground and the roof.
    height, width, channel = img.shape
    img = img[70:height-50, 0:width]
    #show_picture("picture_crop", img, 0, "")

    return img


def recup_parameters_HSV(file):

    #[0, 46, 0, 79, 255, 255]
    #[0, 95, 0, 255, 255, 255]

    #Open file who's contains parameters.
    with open(file, "r") as file:
        liste = [i for i in file]
    #print(liste)

    #Treat and recup data
    data = ""
    for i in liste:
        for j in i:
            if j not in ("]", "["):
                data += j

    #print(data)

    #Split it
    data = data.split(",")
    data = [int(i) for i in data]
    #print(data)

    return data




def HSV_mask(img, parameter1, parameter2):
    """Quote: Wall parameters are parameters we take"""

    #Transform picture BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_b = np.array(parameter1)
    u_b = np.array(parameter2)
    mask = cv2.inRange(hsv, l_b, u_b)

    return mask


def delimitate_contours(cnts, minimum, maximum, blanck):

    #Delete litle and big contours.
    if cv2.contourArea(cnts) > minimum and\
       cv2.contourArea(cnts) < maximum:

        #Recuperate area of detections.
        cv2.drawContours(blanck,[cnts],-1,(255,255,255), 1)
        (x,y,w,h) = cv2.boundingRect(cnts)

        return (x, y, w, h)



def recup_top_points(blanck, copy, pts, position):
    """Here we draw contours for eliminate noise
    or massive area of pixels like light."""

    #Convert tuple position into variables
    x=pts[0]; y=pts[1]; w=pts[2]; h=pts[3];

    #the detection isn't a noise.
    if w+h > 15:

        #print(w+h)
        #Display detection on the picture.
        cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 0, 255), 3)

        #Recuperate points in case.
        position.append(pts)

        #show_picture("blanck", blanck, 0, "")
        #show_picture("copy", copy, 0, "")

    return copy


def recup_bot_points(blanck, copy, pts, position):

    #Convert tuple position into variables
    x=pts[0]; y=pts[1]; w=pts[2]; h=pts[3];

    #the detection isn't a noise (a chain in this case).
    if h < 50:

        #print(h)
        #Display detection on the picture.
        cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 0, 255), 3)

        #Recuperate points in case.
        position.append(pts)

        #show_picture("copy", copy, 0, "")
        #show_picture("blanck_bot", blanck_bot, 0, "")

    return copy


def recuperate_max_contours(contours):
    """Here we recuperate the maximum contours.
    If contour is superior of the current contour
    make this contours the max.
    """

    maxi = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxi:
            maxi = cv2.contourArea(cnt)
  
    return maxi



def draw_contours_bot(contours, blanck, maxi):
    """We recuperate all contours into the max contour"""


    for cnts in contours:
        #The current contour is the max contour
        if cv2.contourArea(cnts) == maxi:

            #We draw it.
            cv2.drawContours(blanck,[cnts],-1,(255,255,255), 1)
            #We recuperate his area.
            (x,y,w,h) = cv2.boundingRect(cnts)

        else:
            #Draw others contours into the max contours.
            cv2.drawContours(blanck,[cnts],-1,(255,255,255), 1)
            cv2.fillPoly(blanck, pts =[cnts], color=(255, 255, 255))

    #Make the rest (outside max contour) black.
    blanck[0:y, x:x+w] = 0

    #show_picture("blanck", blanck, 0, "")

    return blanck



def top_side_picture(img, copy, position):
    """Here we recuperate, delete and display
    our detections from the top of the picture"""

    #Recup parameters from wall_parameters.
    from path import save_parameters_wall_top as para_top
    parameters = recup_parameters_HSV(para_top)
    #print(parameters)

    #Make a mask for delete background.
    mask = HSV_mask(img, parameters[:3], parameters[3:])
    #show_picture("mask", mask, 0, "y")

    #Create new picture.
    blanck = blanck_picture(img)

    #Recuperate contours.
    contours, _ = cv2.findContours(mask, R, P)
    for cnts in contours:

        #Draw contours, estimate them, delete noise and recup pieces.
        pts = delimitate_contours(cnts, 10, 1000, blanck)
        #print(pts)

        if pts:
            #We displaying the detections and recuperate points.
            copy = recup_top_points(blanck, copy, pts, position)

            show_picture("detections", copy, 0, "")



def bot_side_picture(img, copy, position):
    """Here we recuperate, delete and display
    our detections of the bottom of the picture"""
 
    #Recuperate parameters from wall parameters bot.
    from path import save_parameters_wall_bot as para_bot
    parameters = recup_parameters_HSV(para_bot)
    #print(parameters)

    #Create a HSV mask.
    mask = HSV_mask(img, parameters[:3], parameters[3:])
    #show_picture("mask", mask, 0, "y")

    #Create new black picture.
    blanck = blanck_picture(img)

    #Recuperate contours.
    contours, _ = cv2.findContours(mask, R, P)

    #Recuperate the max contour.
    maxi = recuperate_max_contours(contours)
    blanck = draw_contours_bot(contours, blanck, maxi)

    #Filter the blanck picture.
    gray = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)

    #Recuperate contours from the max contour.
    contours, _ = cv2.findContours(gray, R, P)

    #Create new black picture.
    blanck_bot = blanck_picture(img)

    #Recuperate contours on the max contour.
    for cnts in contours:

        #Filter the noise and no interesting contours.
        pts = delimitate_contours(cnts, 200, 10000, blanck_bot)

        if pts:
            #Recuperate position and display it if points exists.
            copy = recup_bot_points(blanck, copy, pts, position)

            show_picture("detections", copy, 0, "")






#Directory of wall with pieces
from path import wall_pieces as wp
liste_wall_pieces = os.listdir(wp)

#Parameters for contours
R = cv2.RETR_TREE
P = cv2.CHAIN_APPROX_NONE

#For position detections
position = []



if __name__ == "__main__":


    for i in liste_wall_pieces:


        #Resize + delete ground and roof
        img = first_operation_picture(wp + i)

        #Make a copy of original
        copy = img.copy()

        """---Top of picture---"""

        print("TOPSIDE")

        top_side_picture(img, copy, position)


        """---Bot of picture---"""

        print("BOTSIDE")

        bot_side_picture(img, copy, position)

        #Here are position of pieces.
        print("All our detection are :\n\n")
        for pos in position:
            print(pos)

        print("")



