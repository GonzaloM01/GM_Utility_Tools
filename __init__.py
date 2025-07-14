import bpy
from bpy.props import EnumProperty, IntProperty, StringProperty, PointerProperty, BoolProperty, FloatProperty
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
    
    #Show info
    show_addon_info: BoolProperty(
        name="Show Contact Info",
        description="Toggle visibility Feedback/Contact info",
        default=False
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

    show_export_options: BoolProperty(
        name="Show Export Options",
        description="Toggle visibility of advanced export options",
        default=True
    )
###########################GENERAL OPTIONS###########################
    export_scale: FloatProperty(
        name="Export Scale %",
        description= "Select the export scale for all the meshes (uses %, so 100 will be the default scale)",
        default = 100,
        min = 0.01,
        max = 100000
        )
        
    apply_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply Modifiers, Apply modifiers to mesh objects",
        default=True
    )
    
    use_triangles: BoolProperty(
        name="Triangulate Meshes",
        description="Triangulate Faces, Convert all faces to triangles",
        default=False
    )
    
    

##########################FBX ONLY OPTIONS##########################
    apply_unit_scale: BoolProperty(
        name="Apply Unit Scale",
        description="When active, FBX format will take into account Blender's scene units",
        default=True
    )
    
    use_space_transform: BoolProperty(
        name="Use Space Transform",
        description="Use Space Transform, Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is",
        default=True
    )
    
    bake_space_transform: BoolProperty(
        name="Bake Space Transform",
        description="Apply Transform, Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender’s space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)",
        default=False
    )
    
    apply_scale_option: EnumProperty(
        name="Apply Scale Option",
        items=[
            ("FBX_SCALE_NONE", "All local", "Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0."),
            ("FBX_SCALE_UNITS", "FBX Units Scale", "Apply custom scaling to each object transformation, and units scaling to FBX scale."),
            ("FBX_SCALE_CUSTOM", "FBX Custom Scale", "Apply custom scaling to FBX scale, and units scaling to each object transformation."),
            ("FBX_SCALE_ALL", "FBX All", "Apply custom scaling and units scaling to FBX scale."),
        ],
        default="FBX_SCALE_NONE"
    )
    
    mesh_smooth_type: EnumProperty(
        name="Mesh Smoothing Type",
        items=[
            ("OFF", "Normals Only", "Export only normals instead of writing edge or face smoothing data."),
            ("FACE", "Face", "Write face smoothing."),
            ("EDGE", "Edge", "Write edge smoothing."),
        ],
        default="OFF"
    )
    
    vertex_color: EnumProperty(
        name="Export Vertex Color",
        items=[
            ("NONE", "Don't Export", "Do not export color attributes"),
            ("SRGB", "sRGB", "Export colors in sRGB color space"),
            ("LINEAR", "Linear", "Export colors in linear color space"),
        ],
        default="LINEAR"
    )
    
    fbx_up_axis: EnumProperty(
        name="Up axis",
        description="Select Up Axis",
        items=[
            ("Z","Z","Z Up"),
            ("-Z","-Z","-Z Up"),
            ("X","X","X Up"),
            ("-X","-X","-X Up"),
            ("Y","Y","Y Up"),
            ("-Y","-Y","-Y Up"),
        ],
        default="-Z"
    )
    fbx_forward_axis: EnumProperty(
        name="Up axis",
        description="Select Forward Axis",
        items=[
            ("Z","Z","Z Forward"),
            ("-Z","-Z","-Z Forward"),
            ("X","X","X Forward"),
            ("-X","-X","-X Forward"),
            ("Y","Y","Y Forward"),
            ("-Y","-Y","-Y Forward"),
        ],
        default="Y"
    )


##########################GLTF ONLY OPTIONS##########################
    use_gltfpack_compression: BoolProperty(
        name="Use GLTFPack Compression",
        description="Use gltfpack to simplify the mesh",
        default=False
    )
    
    export_format: EnumProperty(
        name="Export Format",
        items=[
            ("GLB","Binary file (.glb)","Creates a .glb file per mesh, that contains everything (geometry, materials..."),
            ("GLTF_SEPARATE","Gltf Separate","Creates a .gltf file per mesh, with separate texture files"),
        ],
        default="GLTF_SEPARATE"
    )
    
    export_gltf_materials: EnumProperty(
        name="Export Materials",
        items=[
            ("EXPORT","Export","Export all materials used by included objects."),
            ("PLACEHOLDER","Placeholder","Do not export materials, but write multiple primitive groups per mesh, keeping material slot information."),
            ("NONE","Don't export","Do not export materials, and combine mesh primitive groups, losing material slot information."),
        ],
        default="EXPORT"
    )
    
    export_vertex_color: EnumProperty(
        name="Export Vertex Color",
        items=[
            ("ACTIVE","Active","Export all vertex color, independent if it's used or not"),
            ("MATERIAL","Material","Export vertex color only where it's used by a material"),
            ("NONE","Don't Export","Don't export vertex color"),
        ],
        default="ACTIVE"
    )
    
    gltf_y_up: BoolProperty(
        name="Y Up",
        description="Export Y axis Up, following the glTF convention",
        default=True
    )


##########################OBJ ONLY OPTIONS#########################
    obj_export_vc: BoolProperty(
        name="Export Vertex Color",
        description="Export per-vertex colors",
        default=True
    )
    
    export_obj_materials: BoolProperty(
        name= "Export MTL library",
        description="Export Materials, Export MTL library. There must be a Principled-BSDF node for image textures to be exported to the MTL file",
        default=False
    )
    
    obj_up_axis: EnumProperty(
        name="Up axis",
        description="Select Up Axis",
        items=[
            ("Z","Z","Z Up"),
            ("NEGATIVE_Z","-Z","-Z Up"),
            ("X","X","X Up"),
            ("NEGATIVE_X","-X","-X Up"),
            ("Y","Y","Y Up"),
            ("NEGATIVE_Y","-Y","-Y Up"),
        ],
        default="NEGATIVE_Z"
    )
    obj_forward_axis: EnumProperty(
        name="Up axis",
        description="Select Forward Axis",
        items=[
            ("Z","Z","Z Forward"),
            ("NEGATIVE_Z","-Z","-Z Forward"),
            ("X","X","X Forward"),
            ("NEGATIVE_X","-X","-X Forward"),
            ("Y","Y","Y Forward"),
            ("NEGATIVE_Y","-Y","-Y Forward"),
        ],
        default="Y"
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

