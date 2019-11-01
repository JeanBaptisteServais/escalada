"""Here there are a trackbarre. It's here you can
visualize the objects without the wall !

If you want quit it, you just have to press "q"

It'll write into a file and save it
"""

#os for operation on files
import os

#CV2 is a library for picture treatment
import cv2

#Numpy here is for transform picture to array
import numpy as np





def tracker(image):

    def nothing(x):
        pass

    #Window with commands.
    cv2.namedWindow("Tracking")
    cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

    #Save parameters into list
    liste = []

    
    while True:


        #read and resize picture.
        img = cv2.resize(cv2.imread(image), (500, 500))



        #Transform picture BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)



        #Parameters in action on picture
        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")
        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")



        #By array modify pixels
        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])



        #Make a picture white and black with last parameters
        mask = cv2.inRange(hsv, l_b, u_b)
        #Last parameters in action on the current img
        res = cv2.bitwise_and(img, img, mask=mask)


        #Display all pictures.
        cv2.imshow("frame", img)
        cv2.imshow("mask", mask)
        cv2.imshow("res", res)


        #Here it actualise all seconds.
        #Press q and save parameters in file.
        #here -> info_data/trackabrre.py
        key = cv2.waitKey(1) & 0xff == ord('q')
        if key:
            liste.append([l_h, l_s, l_v, u_h, u_s, u_v])
            cv2.destroyAllWindows()

            with open("info_data/trackbare.py", "w") as file:
                file.write("liste = " + str(liste[-1]))
            return False





if __name__ == "__main__":

    oInput = input("Enter a picture. how? press 1")


    phrase = "Enter path, go explorer, go on you're picture," +\
             "copie url, add picture name + extension"

    while True:

        if oInput == "1":
            oInput = input(phrase)
        else:
            print("Picture pls... ")
            oInput = input("Enter a picture. how? press 1")

        try:
            end = tracker(oInput)
        except:
            pass





















