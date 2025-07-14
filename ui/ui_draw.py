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
        
        #############################
        #EXPORT SETTINGS
        #############################
        common_options_box = sub_col.box()
        
        if exp_settings.export_formats_selection == "FBX" or exp_settings.export_formats_selection == "OBJ":
            #Scale
            scale_row = common_options_box.row(align=True)
            scale_row.prop(exp_settings, "export_scale", text="Export scale %")
        
        #Apply modifiers?
        apply_modifiers_row=common_options_box.row(align=True)
        apply_modifiers_row.prop(exp_settings, "apply_modifiers")
        
        if exp_settings.export_formats_selection == "FBX" or exp_settings.export_formats_selection == "OBJ":
            #Triangulate (added to apply modifiers row)
            apply_modifiers_row.prop(exp_settings,"use_triangles")
        
        #OBJ and FBX Axis order
        if exp_settings.export_formats_selection == "FBX": 
            #Forward and Up Axis
            fbx_axis_row=common_options_box.row(align=True)
            #Split up
            split_fbx_up_axis=fbx_axis_row.split(factor=0.2, align=True)
            split_fbx_up_axis.label(text="Up")
            split_fbx_up_axis.prop(exp_settings, "fbx_up_axis", text="")
            #Split forward
            split_fbx_forward_axis=fbx_axis_row.split(factor=0.6, align=True)
            split_fbx_forward_axis.label(text="     Forward")
            split_fbx_forward_axis.prop(exp_settings, "fbx_forward_axis", text="")
            
        if exp_settings.export_formats_selection == "OBJ":
            #Forward and Up Axis
            obj_axis_row=common_options_box.row(align=True)
            #Split up
            split_obj_up_axis=obj_axis_row.split(factor=0.2, align=True)
            split_obj_up_axis.label(text="Up")
            split_obj_up_axis.prop(exp_settings, "obj_up_axis", text="")
            #Split forward
            split_obj_forward_axis=obj_axis_row.split(factor=0.6, align=True)
            split_obj_forward_axis.label(text="     Forward")
            split_obj_forward_axis.prop(exp_settings, "obj_forward_axis", text="")


        
        #GLTF Y Option
        if exp_settings.export_formats_selection == "GLTF":
            #export Y up
            yup_gltf_row=common_options_box.row(align=True)
            yup_gltf_row.prop(exp_settings, "gltf_y_up")
        
        #FBX Only Options 
        if exp_settings.export_formats_selection == 'FBX':
            apply_unit_scale_row=common_options_box.row(align=True)
            apply_unit_scale_row.prop(exp_settings, "apply_unit_scale")
            
            #Use space transform
            use_space_transform_row=common_options_box.row(align=True)
            use_space_transform_row.prop(exp_settings, "use_space_transform")
            
            #bake space transform
            bake_space_transform_row=common_options_box.row(align=True)
            bake_space_transform_row.prop(exp_settings, "bake_space_transform")
            
            #Apply scale option
            apply_scale_option_row=common_options_box.row(align=True)
            #Split, for better reading
            split_scale_option=apply_scale_option_row.split(factor= 0.45, align=True)
            split_scale_option.label(text="Apply Scale Option")
            split_scale_option.prop(exp_settings, "apply_scale_option", text="")
            
            #Mesh smooth type
            mesh_smooth_type_row=common_options_box.row(align=True)
            #Split for better reading
            split_smooth_type=mesh_smooth_type_row.split(factor= 0.45, align=True)
            split_smooth_type.label(text="Mesh Smoothing Type")
            split_smooth_type.prop(exp_settings, "mesh_smooth_type", text="")
            
            #Vertex color export
            vertex_color_type_row=common_options_box.row(align=True)
            #Split for better reading
            split_vertex_color=vertex_color_type_row.split(factor=0.45, align=True)
            split_vertex_color.label(text="Vertex Color Export")
            split_vertex_color.prop(exp_settings, "vertex_color", text="")
        
        #GLTF Only options    
        if exp_settings.export_formats_selection == "GLTF":
            #export materials
            export_materials_row=common_options_box.row(align=True)
            split_export_materials=export_materials_row.split(factor=0.45, align=True)
            split_export_materials.label(text="Export Materials")
            split_export_materials.prop(exp_settings, "export_gltf_materials", text="")
            
            #export format
            export_format_row=common_options_box.row(align=True)
            split_export_format=export_format_row.split(factor=0.45, align=True)
            split_export_format.label(text="Export Format")
            split_export_format.prop(exp_settings, "export_format", text="")
            
            #export vertex color
            vertex_color_gltf_row=common_options_box.row(align=True)
            split_vertex_color_gltf=vertex_color_gltf_row.split(factor=0.45, align=True)
            split_vertex_color_gltf.label(text="Vertex Color Export")
            split_vertex_color_gltf.prop(exp_settings, "export_vertex_color", text="")
            
            #gltf compression
            gltfpack_compression_row=common_options_box.row(align=True)
            gltfpack_compression_row.prop(exp_settings, "use_gltfpack_compression")
            

        
        #OBJ Only options    
        if exp_settings.export_formats_selection == "OBJ":
            #export mtl
            mtl_export_row=common_options_box.row(align=True)
            mtl_export_row.prop(exp_settings, "export_obj_materials")
            
            #Vertex color export
            vertex_color_obj_row=common_options_box.row(align=True)
            vertex_color_obj_row.prop(exp_settings, "obj_export_vc")
            
            
            
######################INFO PANEL#######################
def draw_info_panel(layout, context):
    scene = context.scene
    
    info_box=layout.box()
    info_box.label(text="This addon is still an early WIP")
    info_box.label(text="Feedback or tool suggestions is welcome")
    
    row = info_box.row(align=True)
    row.operator("wm.url_open", text="Github", icon="FILE_SCRIPT",).url="https://github.com/GonzaloM01/GM_Utility_Tools"
    row2=info_box.row(align=True)
    row2.operator("wm.url_open", text="BlenderArtists Post", icon="FILE_SCRIPT",).url="https://blenderartists.org/t/gm-utility-tools-general-tools-for-modeling-and-game-dev/1601727"
    row3=info_box.row(align=True)
    row3.operator("wm.url_open", text="Gumroad", icon="FILE_SCRIPT",).url="https://gonzalom3d.gumroad.com/l/gm_utility_tools"
    row4=info_box.row(align=True)
    row4.operator("wm.url_open", text="Twitter/X", icon="FILE_SCRIPT",).url="https://x.com/GonzaloM01"
    
    
    
              
            
        
        



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
            
        draw_info_panel(layout, context)




