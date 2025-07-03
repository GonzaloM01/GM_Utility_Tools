import bpy
import bmesh
from mathutils import Vector

class quick_pivot_to_selection(bpy.types.Operator):
    bl_idname = "object.quick_pivot_to_selection"
    bl_label = "Quick pivot to Selection"
    bl_description = "Move the pivot to the selection. Works in both EDIT and OBJECT mode. Object mode moves each mesh's pivot to it's centroid"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #Save Old cursor position
        old_cursor_position = bpy.context.scene.cursor.location.copy()
        
        #Edit mode function
        def edit_mode_get_selection():
            obj = bpy.context.edit_object
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            selected_points = [
                obj.matrix_world @ v.co
                for v in bm.verts if v.select
            ]
            if not selected_points:
                return None
            center = sum(selected_points, Vector()) / len(selected_points)
            return center

        #Exec edit mode function if user is on edit mode
        if bpy.context.mode == "EDIT_MESH":
            selected_geo = edit_mode_get_selection()
            if not selected_geo:
                self.report({"WARNING"}, "There's no selection")
                return {"CANCELLED"}
            else:
                bpy.context.scene.cursor.location = selected_geo
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                bpy.context.scene.cursor.location = old_cursor_position
                bpy.ops.object.editmode_toggle()
                self.report({"INFO"}, "Pivot changed to selection")
                return {"FINISHED"}
            
         
        #Object mode functionality
        elif bpy.context.mode == "OBJECT":
            selection = bpy.context.selected_objects
            if not selection:
                self.report({"WARNING"}, "There's no selection")
                return {"CANCELLED"}
            else:
                bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
                self.report({"INFO"}, "Pivot changed to mesh centroid")
                return {"FINISHED"}
        
        #Warning if the user is neither on edit or object mode
        else:
            self.report({"WARNING"}, "This Operator only works within EDIT or OBJECT mode")
            return {"CANCELLED"}

        
