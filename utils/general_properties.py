import bpy
from bpy.props import EnumProperty, IntProperty, StringProperty, PointerProperty, BoolProperty, FloatProperty



class GM_Addon_Properties(bpy.types.PropertyGroup):
    #Tabs property
    gm_active_tab: EnumProperty(
        name="GM Tabs",
        items=[
            ('MODELING', "Modeling", "Modeling Tools"),
            ('MATERIALS', "Materials", "Materials Tools"),
            ('EXPORT', "Export", "Export Tools"),
        ],
        default="MODELING"
    )
    
    #################################
    #MODELING PANEL PROPERTIES
    #################################
    
    #Lattice divisions property
    lattice_divisions: IntProperty(
        name="Lattice Divisions",
        description="Lattice divisions number for quick lattice tools",
        default=3,
        min=2,
        max=20
    )
    
    
    #################################
    #INFO PANEL PROPERTIES
    #################################
    
    
    #Show info
    show_addon_info: BoolProperty(
        name="Show Contact Info",
        description="Toggle visibility Feedback/Contact info",
        default=False
    )
    
    #################################
    #EXPORT PANEL PROPERTIES
    #################################
    
    #Export folder path property
    export_folder_path: StringProperty(
        name="Export Folder",
        description="Select the folder where the fbx files will be exported",
        subtype="DIR_PATH",
        default=""
    )
    
    #=====================MESH RENAME PROPERTIES===============================
    
    selected_meshes_general_rename: StringProperty(
        name="Rename Selected Meshes",
        description="Rename selected meshes. If you enter a int value, will continue counting from that number. If a string is entered, will change the meshes name to that string",
        subtype="NONE",
        default=""
    )
    
    selected_meshes_prefix: StringProperty(
        name="Add Prefix",
        description="Add written prefix to all selected meshes",
        subtype="NONE",
        default=""
    )
    
    selected_meshes_suffix: StringProperty(
        name="Add Suffix",
        description="Add written suffix to all selected meshes",
        subtype="NONE",
        default=""
    )
    
    replaced_text_from_name: StringProperty(
        name="Replaced text",
        description="Will search this text, and replace with the replacement written by the user. Take CAPITALIZATION into account",
        subtype="NONE",
        default=""
    )
    
    replacement_text_for_name: StringProperty(
        name="Replacement text",
        description="Will replace the previously written text for this. (Leaving this box in blank will delete the text-to-be-replaced)",
        subtype="NONE",
        default=""
    )
    
    filter_non_meshes: BoolProperty(
        name="Filter non-Mesh selected objects",
        description="If active, the rename-related tools will ignore every object that isn't a mesh",
        default=True
    )
    
    rename_affect_all: BoolProperty(
        name="Affect All, not Only Selected",
        description="If active, the rename-related tools will affect all objects in the scene, not only the selected ones",
        default=False
    )