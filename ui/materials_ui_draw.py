import bpy

def draw_material_tools(layout, context):
    scene = context.scene
    props = scene.gm_props
    
    vertex_colours_box = layout.box()
    vertex_colours_box.label(text="Vertex Color Tools")
    vertex_colours_box.separator(factor=1, type="LINE")
    vertex_colours_box.operator("object.quick_random_vertex_color", icon="COLORSET_10_VEC")