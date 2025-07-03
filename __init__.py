import bpy
from bpy.props import EnumProperty, IntProperty, StringProperty, PointerProperty
import importlib
import os
import traceback

#Import other modules
from . import ui
from . import op

#UI Classes import
from .ui.ui_draw import GM_tools_main_panel

#OP Classes import
from .op.quick_pivot import quick_pivot_to_selection
from .op.export_as_single_fbx import single_file_exporter
from .op.quick_lattice import fast_quick_lattice, quick_lattice_base



#========================ADDON INFO========================
bl_info = {
    "name" : "GM's Utility Tools Panel",
    "author" : "Gonzalo Mundi",
    "version" : (0,1),
    "blender" : (4,4,0),
    "location" : "View3D > Sidebar",
    "description" : "Adds a viewport panel with different tools I use for my workflow",
    "category" : "GM Utility Tools"
}

############################################
#PROPERTY CLASS
############################################

class GM_Addon_Properties(bpy.types.PropertyGroup):
    #Tabs property
    gm_active_tab: EnumProperty(
        name="GM Tabs",
        items=[
            ('MODELING', "Modeling", "Modeling Tools"),
            ('EXPORT', "Export", "Export Tools"),
            ('OTHERS', "Others", "Others"),
        ],
        default="MODELING"
    )
    
    #Lattice divisions property
    lattice_divisions: IntProperty(
        name="Lattice Divisions",
        description="Lattice divisions number for quick lattice tools",
        default=3,
        min=2,
        max=20
    )
    
    #Export folder path property
    export_folder_path: StringProperty(
        name="Export Folder",
        description="Select the folder where the fbx files will be exported",
        subtype="DIR_PATH",
        default=""
    )

#========================EXPORT OPTIONS PROPERTIES======================
class export_formats(bpy.types.PropertyGroup):
    export_formats_selection: bpy.props.EnumProperty(
        name="Export formats",
        items=[
            ("OBJ", "OBJ", "Export in OBJ format"),
            ("FBX", "FBX", "Export in FBX format"),
            ("GLTF", "GLTF", "Export in GLTF format"),
        ],
        default="FBX"
    )



#========================CLASSES TO REGISTER========================
classes = (
    GM_Addon_Properties, #Should be first
    export_formats, 
    single_file_exporter,
    quick_pivot_to_selection,
    quick_lattice_base,
    fast_quick_lattice,
    #Main panel should be last
    GM_tools_main_panel,
)



#========================REGISTER========================
def register():
    #first, try to unregister, so it doesn't cause problems while debugging and working on the addon
    try:
        unregister()
    except Exception:
        pass
    
    #=================RECHARGE MODULES FOR DEBUGGING===================
    if "bpy" in locals():
        try:
            #folders
            importlib.reload(ui)
            importlib.reload(op)
            #specific modules
            importlib.reload(ui.ui_draw)
            importlib.reload(op.quick_pivot)
            importlib.reload(op.export_as_single_fbx)
            importlib.reload(op.quick_lattice)
            
            
        except Exception as e:
            print(f"GM_Utility_Tools, Error reloading modules: {e}")
            traceback.print_exc()
    
    
    #REGISTER ALL CLASSES
    try:
        for cls in classes:
            try:
                bpy.utils.register_class(cls)
            except Exception as e:
                print(f"GM_Utility_Tools, ERROR while registering class {cls.__name__}: {e}")
                traceback.print_exc()
        
            ########################
            #REGISTER CLASS PROPERTIES
            ########################
        bpy.types.Scene.gm_props = PointerProperty(type=GM_Addon_Properties)
        bpy.types.Scene.export_settings = PointerProperty(type=export_formats)
            



    except Exception as e: 
        print(f"--- GM_Utility_Tools: ERROR WHILE REGISTER {e} ---")
        traceback.print_exc()
        try:
            unregister()
        except Exception:
            pass

#========================UNREGISTER========================       
def unregister():
    try:
        #Desregister pointer property
        if hasattr(bpy.types.Scene, "gm_props"):
            del bpy.types.Scene.gm_props
        if hasattr(bpy.types.Scene, "export_settings"):
            del bpy.types.Scene.export_settings
        
        #Desregister all classes
        for cls in reversed(classes):
            try:
                bpy.utils.unregister_class(cls)
            except RuntimeError:
                pass
            except Exception as e: 
                print(f"GM_Utility_Tools: ERROR while unregistering class {cls.__name__}: {e}")
                traceback.print_exc()

    except Exception as e: 
        print(f"--- GM_Utility_Tools: ERROR while unregister {e} ---")
        traceback.print_exc()

