# escalada

<p align="center">

<img src = "https://user-images.githubusercontent.com/54853371/68062611-ba164500-fd0b-11e9-858f-2552375650ef.jpg" >

</p>

<br><br>

Care there are some limits <a href="#Caution">Here</a>

<h1>Summary</h1>




<br><br>

<h1>What i need for this project</h1>

1) Python 3.x - https://www.python.org/downloads/

2) Download CV2 and Numpy with the command "pip install open-cv" and "pip install numpy"

3) Use git clone command or copy manually each document with the <strong>same composition</strong>


<br><br>

<h1>How the project functions ?</h1>

1) Lunch wall_parameters from <strong>wall_parameters/wall_parameters.py</strong> with f5 or Run/Run Module from the tool barre.

2) Lunch main and click on a key when picture appears.


<br><br>

<h1>Architecture</h1>

We have 4 folders:
  
  - picture for the wall picture with holds ! 
  
      - The picture for a detection need to be on <strong>pictures/wall_pieces/</strong>.
  
  - wall_parameters for delete the background.

     - put our absolute path for have acces to the app like: C:User/pictures/wall.jpg.

  - info_data who's contains parameters for the background delete.


  - Main
    
    - It call path and pictures_functions.
    
    <strong>path :</strong> In the path file or path.py you need to put our path

    <strong>pictures_functions :</strong> call basic operation like open a picture, create a picture show it and save it.


<br><br>



<br><br><br><br><br><br>






<h1>Wall_parameters</h1>

<strong>wall_parameters</strong> permet to modify parameters of the wall. With the file we can raise the background and recup the pieces.


We need to do it two times. <strong>One time on the top of picture (blue/black colors)</strong> and <strong>one time one bottom</strong> of picture (green). So we can have top and bot objects.

<strong>First we need parameters for the top.</strong> We detect most of all objects but not all. So we need to do it for the bottom.

<p align="center">
  <img width="600" height="200" src="https://user-images.githubusercontent.com/54853371/68077152-05d5f680-fdbf-11e9-8914-08c3172cd91f.png">
  
</p>

<strong>Second We want detect objects not detected by changing parameters.</strong>


<p align="center">
  <img width="600" height="200" src="https://user-images.githubusercontent.com/54853371/68077185-9f050d00-fdbf-11e9-952f-118b8091b73e.png">
  
</p>


In some, we need top black, bottom white. You just have to press "q" and parameters are save into a file.


<strong>NB: </strong>

#top [0, 46, 0, 79, 255, 255] <br>
#bot [0, 95, 0, 255, 255, 255] are the good parameters the current wall. With this light intensity (day intensity different night intensity)

<br><br><br><br><br><br><br><br>





<h1>Main</h1>

Now we have our wall parameters who's permet to identify objects. But we can see some noises. For that we must draw all contours and filter them.

<strong>Top</strong> 

  - We recuperate all contours, if the are of contours < 100 or the contours are > 1000 don't pass.
  
  - If the width + height of detection < 15 pass.
  

<strong>Bot</strong> 

  - We recup only the bottom of the picture.
  
  - We recuperate all contours from the bottom beetween area of 200 to 10000.
  
  - If the height of the detection is < 50 pass.


  

Finally we can superperpose top and bot of picture and have:

<p align="center">

<img  width="500" height="300" src="https://user-images.githubusercontent.com/54853371/68077313-d4125f00-fdc1-11e9-8e3c-83abe08a46d5.png">

</p>

<br><br><br><br><br><br>

<h1 id="Caution">Caution</h1>

But this is for the three first picture who's represent the same caracteristics of light. <strong>It show the importance of the wall parameters.</strong> (sorry can't do better)

So for each hours or a changement of light (like a cloud pass) <strong>the wall_parameters</strong> must be modify.





<p align="center">

<img  width="600" height="400" src="https://user-images.githubusercontent.com/54853371/68077347-56028800-fdc2-11e9-8202-d7c69b796214.png">

</p>




For the moment it must be manually, maybe it could be automatic.

Care it's not finish 100% because i need more picture with more holds on the wall !
