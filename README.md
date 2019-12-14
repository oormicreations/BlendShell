# BlendShell
A Blender plugin for making hollow models suitable for 3D printing.
It creates an inner shell within the model which is attached to the model making it hollow. The wall thickness can be specified. This brings down the cost of printing as less material is needed. It also cuts down the time for printing. Unlike the shell/solidify modifier, it does not deform the thin parts of the model. It is especially useful for sculpted organic models.
You can control the accuracy and density of the shell.
The addon has a utility to create drills and make holes in the hollow model.

**Intro Video**

https://www.youtube.com/watch?v=uURBobfasxk


**Installation**

Download the zip file from *Releases* page here. 
https://github.com/oormicreations/BlendShell/releases

Extract it. In Blender, go to Edit->Preferences->Addons and click Install. Choose the blendshell-xx.py file. Enable the Addon. You should see the UI in the vertical tabs in 3D view. (Visible only in *Object Mode*)

This addon is tested in Blender 2.80 and 2.81 on Linux Mint 19.2

**Usage**

* Create the seed shell by clicking the *Create Seed* button.
* Adjust the size and position of the seed so that it sits inside your model.
* Pick your model from the drop down box.
* Click *Create Shell* button.
* Click *Flip & Attach* button to finish.

*It is recommended to test this addon on the provided blend file to get a feel of how the parameters work.*

**Parameters**

* *Seed Size* : Drag or enter the value to change the size of the seed. Ideally it should be big enough to fit inside the broadest part of the model. The seed should not come out of the model from any side. Also leave a margin that is somewhat greater than the wall thickness.
*Warning: Clicking the Create Seed button or changing the seed size or divisions after creating the shell will reset the seed and you will lose the shell*

* *Seed Divisions* : Number of subdivisions in the seed mesh. A value of 2 or 3 should work. Some big models may need high number of initial subdivisions.
*Warning: Very high number of divisions may crash blender. While dragging the value it will be limited to 4, but you can enter a greater number via keyboard*

* *Target Object* : Pick the model you wish to hollow out from the drop down list.

* *Minimum Thickness* : This is the thickness of the wall. Any part of the model thinner than this value remains untouched.

* *Step* : This is the distance the shell grows in each iteration.
*Note: Smaller values produce more accurate results, but will slow it down. This value should be less than the minimum thickness, lets say about a tenth of it.*

* *Redraw Delay* : Controls how often the screen is refreshed.

* *Max Triangle Area* : The seed mesh expands, and so do the triangles. When they reach this area, they are subdivided. A smaller value will produce a dense mesh. A larger value will produce a low poly shell.

* *Iterations* : The number of times the expansion of the seed happens. 
*Note : A low value may leave some volume unfilled. In that case simply click the *Create Shell* button again, it expands the existing shell. A high value may cause the shell to fold within itself, which is not good.*

* *Drill Count* : Number of drills (Cylinders) you need. Usually specified by the 3D printer. Bigger models need more holes.

* *Hole size* : The diameter of the holes. Usually specified by the 3D printer. Bigger models need bigger holes.

* *Drill length* : Keep it more than twice the wall thickness, so that you can see them and they penetrate the wall completely.

* *Drill Sides* : Sides or vertices of the cap of the cylinders. 

* *Delete Drills* : Deletes the drills after making holes.

* *Help|Source|Updates* : Brings you here.


**Actions**

* *Create Seed* : Creates a sphere, which is the seed that expands to fill the model volume.

* *Create Shell* : Creates the shell. You can keep clicking this button till the seed fills the target model. You can also change the thickness or triangle area and click this button again to refine the shell.

* *Flip & Attach* : Flips the normals of shell and joins it with your model. This effectively makes it hollow.

* *Create Drills* : Creates cylinders with specified dimensions.

* *Drill Holes* : Creates boolean of your model with the drills. In other words, drills the holes. Holes are needed to drain out the supporting material from inside of the printed model. The number of holes and their dia are specified by the printer and depends on the material.

**Info Panel**

The info panel displays some useful info such as dimensions, volume and units in use.

The addon depends on correct unit settings. You can set the units from the *Scene Properties* tab in Properties window. If you are using Metric units and want to display dimensions in mm, you should set the unit scale to 0.001. For cm it should be 0.01 etc.

**Sample Model**

A sample blend file is provided with the addon to test it out. This tool is highly dependent on the geometry and size of the models. You will need to adjust the parameters for each model. Units may also affect the working of this tool. The sample file has everything set right for use with default parameters.

**Known Issues**

* Blender may report a wrong volume when very low poly objects (such as a cube with 6 polys) are hollowed out.  
* If some part of the seed remains outside the object, it keeps growing outside till the number of iterations are over. It should stop as soon as the volume of the seed is greater than the volume of the object.
* If there is no active object, it can throw an error or can disable a button. This can happen for example when you delete something and no object is active. Just select your model and continue.

**Other uses**

It can be used as a remeshing tool if you set the wall thickness very low (e.g. 0.1). A low poly replica of the high poly model can be obtained.

**Misc Info**

This plugin has been released under MIT license, which means it is free for any kind of use and modification, but has no warranties or liabilities. Please read the license before you download and use it. 

**About**


---

A FOSS Project by Oormi Creations

http://oormi.in

oormicreations@gmail.com


![logo](https://oormi.in/software/cbp/images/OormiLogo.png)

December 2019.
