# BlendShell
A Blender plugin for making hollow models suitable for 3D printing.
It creates an inner shell within the model which is attached to the model making it hollow. The wall thickness can be specified. This brings down the cost of printing as less material is needed. It also cuts down the time for printing. Unlike the shell/solidify modifier, it does not deform the thin parts of the model. It is especially useful for sculpted organic models.
You can control the accuracy and density of the shell.
The addon has a utility to create drills and make holes in the hollow model.

**Intro Video**

https://www.youtube.com/watch?v=mFByQwsRA8U


**Installation**

Download the zip file from *Releases* page here. 
https://github.com/oormicreations/BlendShell/releases
Extract it. In Blender, go to Edit->Preferences->Addons and click Install. Choose the blendshell-xx.py file. Enable the Addon. You should see the UI in the vertical tabs in 3D view. (Visible only in *Object Mode*)

This addon is tested in Blender 2.80 and 2.81 on Linux Mint 19.2

**Usage**
* Create the seed shell by clicking the *Create Seed* button
* Adjust the size and position of the seed so that it sits inside your model.
* Click *Create Shell* button
* Click *Flip & Attach* button to finish.

**Parameters**
* *Seed Size* : Drag or enter the value to change the size of the seed. Ideally it should be big enough to fit inside the broadest part of the model. The seed should not come out of the model from any side. Also leave a margin that is somewhat greater than the wall thickness.
* *Seed Divisions* : Number of subdivisions in the seed mesh. A value of 2 or 3 should work. Very high values may crash Blender, if you try to darg it. Some big models may need high number of initial subdivisions.
* *Minimum Thickness* : This is the thickness of the wall. Any part of the model thinner than this value remains untouched.
* *Step* : Smaller values produce more accurate results, but will slow it down. This is the distance the shell grows in each iteration.
* *Redraw Delay* : Controls how often the screen is refreshed.
* *Max Triangle Area* : The seed mesh expands, and so do the triangles. When they reach this area, they are subdivided. A smaller value will produce a dense mesh. A larger value will produce a low poly shell.
* *Iterations* : The number of times the expansion of the seed happens. A low value may leave some volume unfilled. In that case simply click the *Create Shell* button again, it expands the existing shell. A high value may cause the shell to fold within itself, which is not good.
* *Drill Count* : Number of drills (Cylinders) you need. Usually specified by the 3D printer. Bigger models need more holes.
* *Hole size* : The diameter of the holes. Usually specified by the 3D printer. Bigger models need bigger holes.
* *Drill length* : Keep it more than twice the wall thickness, so that you can see them and they penetrate the wall completely.
* *Drill Sides* : Sides or vertices of the cap of the cylinders. 

**Sample Model**
A sample blend file is provided with the addon to test it out. This tool is highly dependent on the geometry and size of the models. You will need to adjust the parameters for each model. Units may also affect the working of this tool. The sample file has everything set right for use with default parameters.

**Known Issues**
* Very low poly objects (such as a cube with 6 polys) are not suitable here. The collisions are not detected and the seed grows through the object.
* If some part of the seed remains outside the object, it keeps growing outside till the number of iterations are over. This can be very time consuming and annoying because it cannot be stopped. Kill blender if it happens.
* You need to select the model when you do any action. The addon will remind you to select the model first, but for some actions, it simply throws an error message. If it happens, just select the model and try again.
* Too many seed divisions will crash or freeze blender. Especially if you drag out the value. A new seed is created for each change and if there are too many subdivisions, blender cannot keep up. Try entering the required value directly by typing in and keep it as low as possible.

**Other uses**
It can be used as a remeshing tool if you set the wall thickness very low (e.g. 0.1). A low poly replica of the high poly model can be obtained.
