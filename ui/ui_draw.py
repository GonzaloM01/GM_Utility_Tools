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
    
    #Output folder selection
    export_box.prop(props, "export_folder_path", text="Output Folder")
    
    #File format selection
    file_format_row=export_box.row(align=True)
    file_format_row.prop(exp_settings, "export_formats_selection", expand=True)
    
    #Export operator
    export_box.operator("object.export_as_individual_files", icon="DISK_DRIVE_LARGE")
    
    #Options drop down menu
    row = export_box.row(align=True)
    
    sub_row=row.row(align=True)
    sub_row.alignment = "LEFT"
    
    sub_row.prop(exp_settings, "show_export_options",
        text="",
        icon="TRIA_DOWN" if exp_settings.show_export_options else "TRIA_RIGHT",
        emboss=False
    )
    
    sub_row.label(text="Export Options:")
    
    #Draw options only if drop down menu is open
    if exp_settings.show_export_options:
        sub_col = export_box.column(align=True)
        sub_col.emboss="NONE"
        
        #Common options
        common_options_col=sub_col.column(align=True)
        common_options_col.label(text="Common options:")
        
        
        #Specific options
        specific_options_col=sub_col.column(align=True)
        specific_options_col.label(text=f"{exp_settings.export_formats_selection.upper()} Format options:")
            
        
        if exp_settings.export_formats_selection == 'FBX':
            fbx_settings_draw(specific_options_col, context)
        elif exp_settings.export_formats_selection == 'OBJ':
            obj_settings_draw(specific_options_col, context)
        elif exp_settings.export_formats_selection == 'GLTF':
            gltf_settings_draw(specific_options_col,context)
    
    

#=================Properties menu=============
def fbx_settings_draw(layout, context):
    exp_settings = context.scene.export_settings
    
    layout.label(text="fbx")

def obj_settings_draw(layout, context):
    exp_settings = context.scene.export_settings
    
    layout.label(text="obj")
    
def gltf_settings_draw(layout, context):
    exp_settings = context.scene.export_settings
    
    layout.label(text="gtlf")



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



