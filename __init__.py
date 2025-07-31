import bpy
from bpy.props import PointerProperty
import importlib
import os
import traceback



#Import other modules
from . import ui
from . import op

#Utils import
from .utils import general_properties, export_as_single_files_properties

#UI import
from .ui.ui_draw import GM_tools_main_panel
from .ui import modeling_ui_draw
from .ui import materials_ui_draw
from .ui import export_ui_draw

#OP Modeling import
from .op.modeling_quick_pivot import quick_pivot_to_selection
from .op.modeling_quick_lattice import quick_lattice_base

#OP Export import
from .op.export_single_files import single_file_exporter
from .op.export_quick_rename import mesh_renamer, mesh_add_prefix, mesh_add_suffix, selected_mesh_name_replace, match_mesh_data_and_obj_names, reset_rename_text_boxes

#OP Materials import
from .op.materials_quick_vertex_color import quick_random_vertex_color




#========================ADDON INFO========================
bl_info = {
    "name" : "GM's Utility Tools Panel",
    "author" : "Gonzalo Mundi",
    "version" : (0,3),
    "blender" : (4,2,0),
    "location" : "View3D > Sidebar",
    "description" : "Adds a viewport panel with different tools I use for my workflow",
    "category" : "GM Utility Tools"
}


########################################################################
#========================CLASSES TO REGISTER========================
########################################################################
classes = (
    #First, import properties from utils
    general_properties.GM_Addon_Properties,
    export_as_single_files_properties.export_formats,
    #Then, import classes 
    single_file_exporter,
    quick_pivot_to_selection,
    quick_lattice_base,
    quick_random_vertex_color,
    mesh_renamer,
    mesh_add_prefix,
    mesh_add_suffix,
    selected_mesh_name_replace,
    match_mesh_data_and_obj_names,
    reset_rename_text_boxes,
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
            importlib.reload(general_properties)
            importlib.reload(export_as_single_files_properties)
            
            #ui modules
            importlib.reload(ui.ui_draw)
            importlib.reload(modeling_ui_draw)
            importlib.reload(materials_ui_draw)
            importlib.reload(export_ui_draw)
            
            #op modules
            importlib.reload(op.modeling_quick_pivot)
            importlib.reload(op.export_single_files)
            importlib.reload(op.modeling_quick_lattice)
            importlib.reload(op.materials_quick_vertex_color)
            importlib.reload(op.export_quick_rename)
            
            
            
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
        bpy.types.Scene.gm_props = PointerProperty(type=general_properties.GM_Addon_Properties)
        bpy.types.Scene.export_settings = PointerProperty(type=export_as_single_files_properties.export_formats)
            



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

