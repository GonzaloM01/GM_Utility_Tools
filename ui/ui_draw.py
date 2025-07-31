import bpy

#Import different ui sections
from . import modeling_ui_draw
from . import materials_ui_draw
from . import export_ui_draw

         
            
######################INFO PANEL#######################
def draw_info_panel(layout, context):
    scene = context.scene
    props = scene.gm_props
    
    
    #Options drop down menu
    base_row = layout.row(align=True)
    
    sub_row=base_row.row(align=True)
    sub_row.alignment = "LEFT"
    
    sub_row.prop(props, "show_addon_info",
        text="",
        icon="TRIA_DOWN" if props.show_addon_info else "TRIA_RIGHT",
        emboss=False
    )
    
    sub_row.label(text="Documentation/Bug Report")
    
    #Draw options only if drop down menu is open
    if props.show_addon_info:
    
    
    
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
        row5=info_box.row(align=True)
        row5.label(text="Documentation")
        row5.operator("wm.url_open", text="Documentation", icon="FILE_SCRIPT",).url="https://daffy-ixia-a22.notion.site/GM_Utility_Tools-Documentation-Blender-Addon-2329a0bdb7be80fe9c49c2470b2d7746?pvs=74"
    
    
    
######################################################################################
#===============================MAIN PANEL CREATION==============================
######################################################################################
class GM_tools_main_panel(bpy.types.Panel):
    bl_label = "GM Utility Tools Panel"
    bl_idname = "GMTools_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GM Utility Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        props = scene.gm_props
        
        if not hasattr(scene, "gm_props"):
            layout.label(text="Loading(properties not found")
            return
        
        #Debug message
        print("GM_tools_panel: Showing panel") 

        row = layout.row(align=True)
        row.prop(props, "gm_active_tab", expand=True)

        if props.gm_active_tab == 'MODELING':
            modeling_ui_draw.draw_modeling_tools(layout, context)
        elif props.gm_active_tab == 'MATERIALS':
            materials_ui_draw.draw_material_tools(layout, context)
        elif props.gm_active_tab == 'EXPORT':
            export_ui_draw.draw_export_tools(layout, context)
            
               
        draw_info_panel(layout, context)




