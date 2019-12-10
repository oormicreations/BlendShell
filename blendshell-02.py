# Mesh hollow automation by oormi creations
# Creates a hollow mesh as per specifictions of minimum thickness.
# Reduces the cost of 3D Print.
# Most useful for high poly organic models. Sculpted models.


bl_info = {
    "name": "BlendShell",
    "description": "Mesh hollow automation by oormi creations",
    "author": "Oormi Creations",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > BlendShell",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
import bmesh
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

import os
from bpy import context
import time


# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

def ShowMessageBox(message = "", title = "BlendShell Says...", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
    
def printconsole(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT") 

def Create_Seed(div, dia):
    seed = bpy.data.objects.get("Seed.001")
    if seed is not None:
        bpy.ops.object.select_all(action='DESELECT')
        seed.select_set(True)
        bpy.ops.object.delete()
        
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=div, radius=dia/2.0)
    seed = bpy.context.selected_objects[0]
    seed.name = "Seed.001"
    #printconsole("Seed created")
    
def On_Seedsz_Changed(self, context):
    bstool = context.scene.bs_tool
    Create_Seed(bstool.bs_seeddiv, bstool.bs_seedsz)

class CSH_OT_CCreateShell(bpy.types.Operator):
    bl_idname = "bscreate.shell"
    bl_label = "Create Shell"
    bl_description = "Create the hollow shell"
    
    def execute(self, context):
        #########   Remove ######
        #bpy.ops.object.delete() #
        #########################
        scene = context.scene
        bstool = scene.bs_tool
        
        seedsz = bstool.bs_seedsz#5.0
        seeddiv = bstool.bs_seeddiv#2
        thickness = bstool.bs_thickness#3.5
        dv = bstool.bs_dv#0.1
        rdelay = bstool.bs_rdelay#10
        pszmax = bstool.bs_pszmax#4
        itrs = bstool.bs_itrs#600

        seed = bpy.data.objects.get("Seed.001")
        if seed == None:
            ShowMessageBox("Please create a seed, position it inside your model and try again") 
            return{'FINISHED'}


        target = bpy.context.object
        if target == None or target == seed:
            ShowMessageBox("Please select your model first and try again") 
            return{'FINISHED'}
        
        #seed.show_wire = True
        #seed.show_all_edges = True
        #save old origin
        oldloc0 = target.location[0]
        oldloc1 = target.location[1]
        oldloc2 = target.location[2]
        #printconsole(oldloc2)
        #return{'FINISHED'} 
    
        #fix origin
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = target
        target.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.context.scene.cursor.location = seed.location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = seed
        seed.select_set(True)
        
        #return{'FINISHED'} 
        
        start_time = time.time()
        redrw = 0
        unmovable = []

        for it in range(0,itrs):
            #redraw view
            redrw = redrw + 1
            if redrw > rdelay:
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                redrw = 0
                print ("Itr = ", it)
                
            #expand seed
            for v in seed.data.vertices:
                if (v.index in unmovable) == False:
                    (hit, loc, norm, face_index) = target.closest_point_on_mesh(v.co)
                    if hit:
                        dist = (loc - v.co).length
                        if dist > thickness:
                            v.co += dv * v.normal
                        else:
                            unmovable.append(v.index)

        #'''              
            #divide large polys
            bpy.ops.object.mode_set(mode='EDIT')

            bm = bmesh.from_edit_mesh(seed.data)
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()

            flist = []
            for p in bm.faces: 
                p.select = True
                if p.calc_area() > pszmax:
                    #p.select = True
                    flist.append(p)    

            bmesh.ops.poke(bm, faces = flist)
            bmesh.update_edit_mesh(seed.data)
            bpy.ops.mesh.beautify_fill()
            bpy.ops.object.mode_set(mode='OBJECT')

        #'''

        bpy.ops.object.modifier_add(type='SMOOTH')
        bpy.context.object.modifiers["Smooth"].iterations = 4
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")

        printconsole ("Shell created !")    
        printconsole((time.time() - start_time))
        printconsole("--- seconds ---")        
        bpy.context.scene.cursor.location[0] = oldloc0
        bpy.context.scene.cursor.location[1] = oldloc1
        bpy.context.scene.cursor.location[2] = oldloc2
                        
        return{'FINISHED'} 

class CFA_OT_CFlipAttach(bpy.types.Operator):
    bl_idname = "bsflip.attach"
    bl_label = "Flip Attach"
    bl_description = "Flips the normals and joins to model"
    
    def execute(self, context):

        scene = context.scene
        bstool = scene.bs_tool
        
        seed = bpy.data.objects.get("Seed.001")
        if seed == None:
            ShowMessageBox("Seed not found!") 
            return{'FINISHED'}

        target = bpy.context.object
        if target == None or target == bpy.data.objects['Seed.001']:
            ShowMessageBox("Please select your model first and try again") 
            return{'FINISHED'}
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = seed
        seed.select_set(True)
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode='OBJECT')
        target.select_set(True)
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.join()
        
        #reset location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.context.selected_objects[0].location = [0,0,0]
        bpy.context.scene.cursor.location[1] = 0
        bpy.context.scene.cursor.location[2] = 0
        bpy.context.scene.cursor.location[0] = 0

        printconsole ("Flipped & Attached!")    
        return{'FINISHED'}             
    

class CDH_OT_CDrillHoles(bpy.types.Operator):
    bl_idname = "bsdrill.holes"
    bl_label = "Drill Holes"
    bl_description = "Make holes in hollow model"
    
    def execute(self, context):

        scene = context.scene
        bstool = scene.bs_tool
        
        target = bpy.context.selected_objects[0]      
        if target == None:
            ShowMessageBox("Please select your model first and try again") 
            return{'FINISHED'}
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = target
        target.select_set(True)
        
        drills = [obj for obj in bpy.data.objects if obj.name.startswith("Drill")]
        
        for d in drills:
            printconsole(d.name)
            bpy.ops.object.modifier_add(type='BOOLEAN')
            bpy.context.object.modifiers["Boolean"].object = d
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

        printconsole ("Holes Drilled!")    
        return{'FINISHED'}          
    

class CCD_OT_CCreateDrills(bpy.types.Operator):
    bl_idname = "bscreate.drills"
    bl_label = "Create Drills"
    bl_description = "Create cylindrical drills for making holes"
    
    def execute(self, context):

        scene = context.scene
        bstool = scene.bs_tool
        rad=bstool.bs_drilldia/2
        
        for i in range(0, bstool.bs_ndrills):
            bpy.ops.mesh.primitive_cylinder_add(vertices=bstool.bs_drillsides, radius=rad, \
            depth=bstool.bs_drillsz, location=(i*bstool.bs_drilldia, 0, 0))
            drill = bpy.context.selected_objects[0]
            drill.name = "Drill.001"
        
        printconsole ("Drills Created!")    
        return{'FINISHED'}              

class CCS_OT_CCreateSeed(bpy.types.Operator):
    bl_idname = "bscreate.seed"
    bl_label = "Create Seed"
    bl_description = "Create seed mesh to fill the model"
    
    def execute(self, context):
        bstool = context.scene.bs_tool
        Create_Seed(bstool.bs_seeddiv, bstool.bs_seedsz)
        printconsole ("Seed Created")    
        return{'FINISHED'}    

############################ Panels ############################################## 
        
class OBJECT_PT_BlendShellPanel(Panel):
    bl_label = "BlendShell 0.1"
    bl_idname = "OBJECT_PT_Bs_Panel"
    bl_category = "BlendShell"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"

#    @classmethod
#    def poll(self,context):
#        return context.object is not None
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        bstool = scene.bs_tool
        
        layout.prop(bstool, "bs_seedsz")
        layout.prop(bstool, "bs_seeddiv")
        layout.operator("bscreate.seed", text = "Create Seed", icon='MESH_UVSPHERE')
        layout.prop(bstool, "bs_thickness")        
        layout.prop(bstool, "bs_dv")
        layout.prop(bstool, "bs_rdelay")
        layout.prop(bstool, "bs_pszmax")
        layout.prop(bstool, "bs_itrs")
        layout.operator("bscreate.shell", text = "Create Shell", icon='TRIA_RIGHT')        
        row = layout.row(align=True)

class OBJECT_PT_BlendShellPostPanel(bpy.types.Panel):

    bl_label = "Prepare for Print"
    bl_idname = "OBJECT_PT_BlendShell_PostPanel"
    bl_category = "BlendShell"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        bstool = scene.bs_tool
        
        layout.operator("bsflip.attach", text = "Flip & Attach", icon='TRIA_RIGHT')
        layout.prop(bstool, "bs_ndrills")
        layout.prop(bstool, "bs_drilldia")
        layout.prop(bstool, "bs_drillsz")
        layout.prop(bstool, "bs_drillsides")
        layout.operator("bscreate.drills", text = "Create Drills", icon='MESH_CYLINDER')
        layout.operator("bsdrill.holes", text = "Drill Holes", icon='TRIA_RIGHT')
        
        row = layout.row()
        row.operator("wm.url_open", text="Help | Source | Updates", icon='QUESTION').url = "https://github.com/oormicreations/blendshell"
        
class CCProperties(PropertyGroup):
    
    bs_thickness: FloatProperty(
        name = "Min Thickness",
        description = "Minimum thickness of the shell",
        default = 3.5,
        min=0.01,
        max=10000.0        
      )
    bs_seedsz: FloatProperty(
        name = "Seed Size",
        description = "Initial size of the seed shell",
        default = 5.0,
        min=0.01,
        max=10000.0,
        update=On_Seedsz_Changed        
      )
    bs_seeddiv: IntProperty(
        name = "Seed Divisions",
        description = "Number of initial divisions of seed",
        default = 2,
        min=1,
        max=8,
        update=On_Seedsz_Changed  
      )
    bs_dv: FloatProperty(
        name = "Step",
        description = "Step size for each iteration of seed expansion",
        default = 0.1,
        min=0.01,
        max=100.0        
      )
    bs_rdelay: IntProperty(
        name = "Redraw Delay",
        description = "Redraw views faster or slower",
        default = 10,
        min=1,
        max=100        
      )
    bs_pszmax: FloatProperty(
        name = "Max Triangle Area",
        description = "Maximum triangle area after which it gets subdivided",
        default = 4.0,
        min=0.1,
        max=10000.0        
      )
    bs_itrs: IntProperty(
        name = "Iterations",
        description = "Maximum number of iterations",
        default = 600,
        min=1,
        max=100000        
      )
    bs_ndrills: IntProperty(
        name = "Drill Count",
        description = "Number of drills, Number of holes",
        default = 2,
        min=1,
        max=20        
      )
    bs_drilldia: FloatProperty(
        name = "Hole size",
        description = "Dia of the holes, size of drills",
        default = 5.0,
        min=0.1,
        max=1000.0
      )
    bs_drillsz: FloatProperty(
        name = "Drill Length",
        description = "Length of the drills",
        default = 10.0,
        min=1.0,
        max=1000.0
      )
    bs_drillsides: IntProperty(
        name = "Drill Sides",
        description = "Number of sides or vertices of cap",
        default = 32,
        min=3,
        max=128
    )
       
    
# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    CCS_OT_CCreateSeed,
    CSH_OT_CCreateShell,
    CFA_OT_CFlipAttach,
    CCD_OT_CCreateDrills,
    CDH_OT_CDrillHoles,
    CCProperties,
    OBJECT_PT_BlendShellPanel,
    OBJECT_PT_BlendShellPostPanel
)

def register():
    bl_info['blender'] = getattr(bpy.app, "version")
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.bs_tool = PointerProperty(type=CCProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.bs_tool


if __name__ == "__main__":
    register()