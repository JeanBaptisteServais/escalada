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
    #localisation of saved paramaters
    data_position1 = "../info_data/trackbaretop.txt"
    data_position2 = "../info_data/trackbarebot.txt"

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

            Oinput = input("t for top b for bot")

            if Oinput == "t":
                data_position = data_position1
            else:
                data_position = data_position2

            liste.append([l_h, l_s, l_v, u_h, u_s, u_v])
            cv2.destroyAllWindows()

            with open(data_position, "w") as file:
                file.write(str(liste[-1]))

            print(liste)
            print(liste[-1])
            return False





if __name__ == "__main__":

    alert = "ALERTE parameters from this pictures are " +\
            "TOP :0 46 0 79 255 255 bot: 0 95 0 255 255 255"

    print(alert)

    oInput = input("Enter a picture. how? press 1")


    phrase = "Enter path, go explorer, go on you're picture," +\
             "copie url, add / add picture name + extension \n" +\
             "like: C:Jb/Dwonload/image.jpg"

    while True:

        if oInput == "1":
            oInput = input(phrase)

        try:
            print("Press Q for quit and save parameters")
            end = tracker(oInput)
        except:
            print("oups")

