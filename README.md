<h1>Main</h1>

Now we have our wall parameters who's permet to identify objects. But we can see some noises. For that we must draw all contours and filter them.

Top 

  - We recuperate all contours, if the are of contours < 100 or the contours are > 1000 don't pass.
  
  - If the width + height of detection < 15 pass.
  

Bot

  - We recup only the bottom of the picture.
  
  - We recuperate all contours from the bottom beetween area of 200 to 10000.
  
  - If the height of the detection is < 50 pass.


  

Finally we can have:




<br><br><br><br><br><br>

<h1 id="Caution">Caution</h1>

But this is for the three first picture who's represent the same caracteristics of light. It show the importance of the wall parameters.

So for each hours or a changement of light (like a cloud pass) <strong>the wall_parameters</strong> must be modify.

For the moment it must be manually, maybe it could be automatic.

Care it's not finish 100% because i need more picture with more holds on the wall !
