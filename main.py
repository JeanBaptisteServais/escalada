import os
import cv2
import numpy as np

from pictures_function import open_picture
from pictures_function import show_picture
from pictures_function import blanck_picture

from path import save_parameters_wall_bot as para_bot

def first_operation_picture(path_picture):

    #Resize picture to 500x500.
    img = cv2.resize(open_picture(path_picture), (500, 500))

    #We delete the ground and the roof.
    height, width, channel = img.shape
    img = img[70:height-50, 0:width]

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


def draw_contours(mask, blanck, R, P, copy, position):
    
    contours, _ = cv2.findContours(mask, R, P)

    maxi = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxi:
            maxi = cv2.contourArea(cnt)

    for cnts in contours:
        if cv2.contourArea(cnts) > 10 and\
           cv2.contourArea(cnts) < 1000:

            cv2.drawContours(blanck,[cnts],-1,(255,255,255), 1)
            #cv2.fillPoly(blanck, pts =[cnts], color=(255, 255, 255))
            (x,y,w,h) = cv2.boundingRect(cnts)
            position.append([x, y, w, h])

            print("ici", w, h)
            cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 0, 255), 3)



    return copy, blanck





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

        #Recup parameters from wall_parameters
        from path import save_parameters_wall_top as para_top
        parameters = recup_parameters_HSV(para_top)
        #print(parameters)

        #Make a mask for delete background
        mask = HSV_mask(img, parameters[:3], parameters[3:])
        show_picture("mask", mask, 0, "")

        #Create new picture
        blanck = blanck_picture(img)

        #Draw contours for delete noise and recup pieces.
        copy, blanck =\
        draw_contours(mask, blanck, R, P, copy, position)

        show_picture("copy", copy, 0, "")
        show_picture("blanck", blanck, 0, "")













































        #bas
        l_b1 = np.array([76, 47, 0])
        u_b1 = np.array([98, 192, 255])
        mask1 = cv2.inRange(hsv, l_b1, u_b1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #show_picture("mask1", mask1, 0, "")
        



        blanck = blanck_picture(img);

        contours, _ = cv2.findContours(mask1, R, P)

        maxi = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > maxi:
                maxi = cv2.contourArea(cnt)


        for cnts in contours:

            if cv2.contourArea(cnts) == maxi:
                cv2.drawContours(blanck,[cnts],-1,(255,255,255), 1)
                #cv2.fillPoly(blanck, pts =[cnts], color=(255, 255, 255))
                (x,y,w,h) = cv2.boundingRect(cnts)
            else:
                cv2.drawContours(blanck,[cnts],-1,(255,255,255), 1)
                cv2.fillPoly(blanck, pts =[cnts], color=(255, 255, 255))

        

        blanck[0:y, x:x+w] = 0

        show_picture("blanck", blanck, 0, "")




        gray = cv2.cvtColor(blanck, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, R, P)
        blanck_bot = blanck_picture(img);

        for cnts in contours:
            if cv2.contourArea(cnts) > 200 and\
               cv2.contourArea(cnts) < 10000:

                cv2.drawContours(blanck_bot,[cnts],-1,(255,255,255), 1)

                (x,y,w,h) = cv2.boundingRect(cnts)
                if h < 50:
                    print(cv2.contourArea(cnts), w,h)
                    show_picture("blanck_bot", blanck_bot, 0, "")

                    try:
                        crop_mask = blanck[y-5:y+h+5, x-5:x+w+5]
                        show_picture("crop_mask", crop_mask, 0, "")
                    except:
                        pass


                    cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    show_picture("copy", copy, 0, "")


                    crop = img[y-5:y+h+5, x-5:x+w+5]






















