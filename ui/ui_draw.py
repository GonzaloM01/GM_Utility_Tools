import bpy


#==============================MODELING TOOLS TAB DRAW=========================
def draw_modeling_tools(layout, context):
    scene = context.scene
    
    #Get custom properties
    props = scene.gm_props
    
    #Pivot tools
    pivot_box = layout.box()
    pivot_box.label(text="Pivot Tools")
    pivot_box.operator("object.quick_pivot_to_selection", icon="DOT")
    
    #Lattice tools
    lattice_box = layout.box()
    lattice_box.label(text="Lattice Tools")
    lattice_box.operator("object.quick_lattice_base", icon ="MESH_CUBE")
    #lattice_box.operator("object.fast_quick_lattice", icon ="MOD_LATTICE")
    #Lattice selector
    row = lattice_box.row()
    row.prop(props, "lattice_divisions", text="Lattice Points")
    
    
    
    """
    modifiers_box = layout.box()
    modifiers_box.label(text="Apply All modifiers from Selection")
    """

#==============================EXPORT TOOLS TAB DRAW=========================
def draw_export_tools(layout, context):
    scene = context.scene
    
    #Get custom properties
    props = scene.gm_props
    exp_settings = scene.export_settings
    
    
    export_box = layout.box()
    export_box.label(text="Export selection as multiple files")
    
    #File format selection
    file_format_row=export_box.row(align=True)
    file_format_row.prop(exp_settings, "export_formats_selection", expand=True)

    if exp_settings.export_formats_selection == 'FBX':
        fbx_settings(layout, context)
    elif exp_settings.export_formats_selection == 'OBJ':
        obj_settings(layout, context)
    elif exp_settings.export_formats_selection == 'GLTF':
        gltf_settings(layout,context)
    
    export_box.prop(props, "export_folder_path", text="Output Folder")
    export_box.operator("object.export_as_individual_files", icon="DISK_DRIVE_LARGE")

#=================Properties menu=============
def fbx_settings(layout, context):
    print("fbx")

def obj_settings(layout, context):
    print("obj")
    
def gltf_settings(layout, context):
    print("gltf")



#==============================OTHERS TOOLS TAB DRAW=========================
def draw_options_tools(layout, context):
    layout.label(text="Others:")



#===============================MAIN PANEL CREATION==============================
class GM_tools_main_panel(bpy.types.Panel):
    bl_label = "GM Utility Tools Panel"
    bl_idname = "GMTools_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GM Utility Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not hasattr(scene, "gm_props"):
            layout.label(text="Loading(properties not found")
            return
        
        props = scene.gm_props
        
        #Debug message
        print("GM_tools_panel: Showing panel") 

        row = layout.row(align=True)
        row.prop(props, "gm_active_tab", expand=True)

        if props.gm_active_tab == 'MODELING':
            draw_modeling_tools(layout, context)
        elif props.gm_active_tab == 'EXPORT':
            draw_export_tools(layout, context)
        elif props.gm_active_tab == 'OTHERS':
            draw_others_tools(layout,context)



