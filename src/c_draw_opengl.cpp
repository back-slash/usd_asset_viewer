///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Draw OpenGL
// TODO:
// 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Define
#define NOMINMAX
#define PYBIND11_DETAILED_ERROR_MESSAGES

// C++
#include <iostream>
#include <vector>
#include <string>

// PyBind11
#include "usd_pybind_cast.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// OpenUSD
#include <pxr/base/gf/matrix4d.h>
#include <pxr/base/gf/rotation.h>
#include <pxr/base/gf/vec3d.h>
#include <pxr/base/tf/token.h>
#include <pxr/usd/usd/prim.h>

// OpenGL
#include <glad/glad.h>

// Project
#include "c_draw_utils.cpp"
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Draws bones for overlay visualization
void c_draw_opengl_bone_xray(pybind11::list bone_list, pybind11::dict draw_dict) {
    glPushMatrix();
    c_setup_opengl_viewport(
        draw_dict
    );
    glDisable(GL_DEPTH_TEST);
    
    float line_width = 0.5f;
    std::vector<float> line_color = { 0.66f, 1.0f, 0.66f, 0.5f };
    for (auto bone : bone_list) {
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pxr::GfMatrix4d bone_matrix = data_dict["matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();

        glLineWidth(line_width);
        glBegin(GL_LINES);
        glColor3f(1.0f, 0.0f, 0.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d x_axis = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));
        glVertex3d(x_axis[0], x_axis[1], x_axis[2]);
        glColor3f(0.0f, 1.0f, 0.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d y_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 0.0));
        glVertex3d(y_axis[0], y_axis[1], y_axis[2]);
        glColor3f(0.0f, 0.0f, 1.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d z_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 0.0, 1.0));
        glVertex3d(z_axis[0], z_axis[1], z_axis[2]);
        glEnd();
        pybind11::list bone_children = bone.attr("get_child_nodes")();

        if (bone_children.size() == 0) {

            pxr::GfVec3d end_bone_start_vert = bone_matrix.Transform(pxr::GfVec3d(-1.0, 0.0, 0.0));
            pxr::GfVec3d end_bone_vert_1 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 1.0));
            pxr::GfVec3d end_bone_vert_2 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, 1.0));
            pxr::GfVec3d end_bone_vert_3 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, -1.0));
            pxr::GfVec3d end_bone_vert_4 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, -1.0));
            pxr::GfVec3d end_bone_end_vert = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));

            glLineWidth(line_width);
            glBegin(GL_LINES);
            glColor4f(line_color[0], line_color[1], line_color[2], line_color[3]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);

            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);

            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glEnd();
        }
        for (auto child : bone_children) {
            pybind11::dict child_data_dict = child.attr("get_data_object")();
            pxr::GfMatrix4d child_matrix = child_data_dict["matrix"].cast<pxr::GfMatrix4d>();
            pxr::GfVec3d child_root_vert = child_matrix.ExtractTranslation();
            double bone_length = (child_root_vert - root_vert).GetLength();
            if (bone_length < 0.1) {
                continue;
            }
            double bone_spur = bone_length * 0.2;
            double radial_segments = 4;
            double bone_radius = bone_length / 25.0;
            pxr::GfVec3d direction = child_root_vert - root_vert;
            direction.Normalize();
            pxr::GfVec3d up(0.0, 0.0, 1.0);

            pxr::GfMatrix4d bone_world_matrix = calc_look_at_x(root_vert, child_root_vert, up);
            pxr::GfVec3d bone_middle_vert_1 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_2 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_3 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, -bone_radius));
            pxr::GfVec3d bone_middle_vert_4 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, -bone_radius));
            pxr::GfVec3d calc_end_vert = child_root_vert;

            glLineWidth(line_width);
            glBegin(GL_LINES);
            glColor4f(line_color[0], line_color[1], line_color[2], line_color[3]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);

            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);

            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);            
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);   
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);   
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]); 
            glEnd();
        }
    
    }
    glEnable(GL_DEPTH_TEST);
    glPopMatrix();
    c_check_opengl_error();
}

// Draw bones for standalone visualization
void c_draw_opengl_bone(pybind11::list bone_list, pybind11::dict draw_dict) {
    glPushMatrix();

    c_setup_opengl_viewport(
        draw_dict
    );

    float line_width = 2.0f;
    std::vector<float> line_color = { 0.5f, 0.5f, 0.5f, 1.0f };
    std::vector<float> face_color = { 0.33f, 0.33f, 0.33f, 1.0f };

    for (auto bone : bone_list) {
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pxr::GfMatrix4d bone_matrix = data_dict["matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();
        pybind11::list bone_children = bone.attr("get_child_nodes")();



        if (bone_children.size() == 0) {

            pxr::GfVec3d end_bone_start_vert = bone_matrix.Transform(pxr::GfVec3d(-1.0, 0.0, 0.0));
            pxr::GfVec3d end_bone_vert_1 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 1.0));
            pxr::GfVec3d end_bone_vert_2 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, 1.0));
            pxr::GfVec3d end_bone_vert_3 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, -1.0));
            pxr::GfVec3d end_bone_vert_4 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, -1.0));
            pxr::GfVec3d end_bone_end_vert = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));

            glLineWidth(line_width);
            glBegin(GL_LINES);
            glColor4f(line_color[0], line_color[1], line_color[2], line_color[3]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);

            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);

            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glEnd();

            glBegin(GL_TRIANGLES);
            glColor4f(face_color[0], face_color[1], face_color[2], face_color[3]);
            
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);            
            
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            
            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);

            glVertex3d(end_bone_start_vert[0], end_bone_start_vert[1], end_bone_start_vert[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);

            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);

            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);
            glVertex3d(end_bone_vert_2[0], end_bone_vert_2[1], end_bone_vert_2[2]);

            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_3[0], end_bone_vert_3[1], end_bone_vert_3[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);

            glVertex3d(end_bone_end_vert[0], end_bone_end_vert[1], end_bone_end_vert[2]);
            glVertex3d(end_bone_vert_4[0], end_bone_vert_4[1], end_bone_vert_4[2]);
            glVertex3d(end_bone_vert_1[0], end_bone_vert_1[1], end_bone_vert_1[2]);


            glEnd();
        }
        for (auto child : bone_children) {
            pybind11::dict child_data_dict = child.attr("get_data_object")();
            pxr::GfMatrix4d child_matrix = child_data_dict["matrix"].cast<pxr::GfMatrix4d>();
            pxr::GfVec3d child_root_vert = child_matrix.ExtractTranslation();
            double bone_length = (child_root_vert - root_vert).GetLength();
            if (bone_length < 0.1) {
                continue;
            }
            double bone_spur = bone_length * 0.2;
            double radial_segments = 4;
            double bone_radius = bone_length / 25.0;
            pxr::GfVec3d direction = child_root_vert - root_vert;
            direction.Normalize();
            pxr::GfVec3d up(0.0, 0.0, 1.0);

            pxr::GfMatrix4d bone_world_matrix = calc_look_at_x(root_vert, child_root_vert, up);
            pxr::GfVec3d bone_middle_vert_1 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_2 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_3 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, -bone_radius));
            pxr::GfVec3d bone_middle_vert_4 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, -bone_radius));
            pxr::GfVec3d calc_end_vert = child_root_vert;
            glBegin(GL_TRIANGLES);
            glColor4f(face_color[0], face_color[1], face_color[2], face_color[3]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);   
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);            
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);            
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);            
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]); 
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);  
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glEnd();

            glLineWidth(line_width);
            glBegin(GL_LINES);
            glColor4f(line_color[0], line_color[1], line_color[2], line_color[3]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);

            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(calc_end_vert[0], calc_end_vert[1], calc_end_vert[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);

            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]);            
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);   
            glVertex3d(bone_middle_vert_2[0], bone_middle_vert_2[1], bone_middle_vert_2[2]);   
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(bone_middle_vert_3[0], bone_middle_vert_3[1], bone_middle_vert_3[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(bone_middle_vert_4[0], bone_middle_vert_4[1], bone_middle_vert_4[2]);
            glVertex3d(bone_middle_vert_1[0], bone_middle_vert_1[1], bone_middle_vert_1[2]); 
            glEnd();
        }
    
    }
    glPopMatrix();
    c_check_opengl_error();
}

// Draw a grid plane
void  c_draw_opengl_grid(pybind11::dict draw_dict) {
    glPushMatrix();

    c_setup_opengl_viewport(draw_dict);

    int grid_density = draw_dict["grid_density"].cast<int>();
    pxr::GfVec3d bbox_size = draw_dict["scene_bbox_size"].cast<pxr::GfVec3d>();
    int grid_size = int(bbox_size.GetLength() * 2.0);
    float step = static_cast<float>(grid_size) / static_cast<float>(grid_density);
    std::vector<float> grid_color = draw_dict["grid_color"].cast<std::vector<float>>();
    std::string up_axis = draw_dict["up_axis"].cast<std::string>();
    glLineWidth(0.75f);
    glColor4f(
        static_cast<GLfloat>(grid_color[0]), 
        static_cast<GLfloat>(grid_color[1]),
        static_cast<GLfloat>(grid_color[2]), 
        static_cast<GLfloat>(grid_color[3])
    );
    glBegin(GL_LINES);      
    for (int index = -grid_density; index <= grid_density; ++index) {
        glColor4f(
            static_cast<GLfloat>(grid_color[0]), 
            static_cast<GLfloat>(grid_color[1]),
            static_cast<GLfloat>(grid_color[2]), 
            static_cast<GLfloat>(grid_color[3])
        );
        if (index == 0) {
            if (up_axis == "Y") {
                glColor4f(0, 0, 1, 1);
            } else {
                glColor4f(0, 1, 0, 1);
            }
        }
        if (up_axis == "Y") {
            glVertex3f(index * step, 0.0f, -grid_size);
            glVertex3f(index * step, 0.0f, grid_size);

        } else {
            glVertex3f(index * step, -grid_size, 0.0f);
            glVertex3f(index * step, grid_size, 0.0f);
        }
        glColor4f(
            static_cast<GLfloat>(grid_color[0]), 
            static_cast<GLfloat>(grid_color[1]),
            static_cast<GLfloat>(grid_color[2]), 
            static_cast<GLfloat>(grid_color[3])
        );
        if (index == 0) {
            glColor4f(1, 0, 0, 1);
        }
        if (up_axis == "Y") {
            glVertex3f(-grid_size, 0.0f, index * step);
            glVertex3f(grid_size, 0.0f, index * step);
        } else {
            glVertex3f(-grid_size, index * step, 0.0f);
            glVertex3f(grid_size, index * step, 0.0f);            
        }

    }
    glEnd();
    glPopMatrix();
    c_check_opengl_error();
}


// Draw a small orientation gizmo.
void  c_draw_opengl_gizmo(pybind11::dict draw_dict) {
    glPushMatrix();

    float gizmo_size = 60;
    int hydra_x_min = draw_dict["hydra_x_min"].cast<int>();
    int hydra_y_min = draw_dict["hydra_y_min"].cast<int>();
    glViewport(int(hydra_x_min) + 10, int(hydra_y_min), gizmo_size, gizmo_size);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    glMatrixMode(GL_MODELVIEW);
    pxr::GfMatrix4d camera_matrix = draw_dict["camera_matrix"].cast<pxr::GfMatrix4d>();
    pxr::GfMatrix4d camera_rotation_matrix = pxr::GfMatrix4d().SetRotate(camera_matrix.ExtractRotation()).GetInverse();
    double camera_rotation_matrix_gl[16];
    convert_matrix_usd_gl(camera_rotation_matrix, camera_rotation_matrix_gl);
    glLoadMatrixd(camera_rotation_matrix_gl);

    float axis_length = 0.5;
    glLineWidth(2.0);
    glBegin(GL_LINES);
    glColor3f(1.0, 0.0, 0.0);
    glVertex3f(0.0, 0.0, 0.0);
    glVertex3f(axis_length, 0.0, 0.0);
    glColor3f(0.0, 1.0, 0.0);
    glVertex3f(0.0, 0.0, 0.0);
    glVertex3f(0.0, axis_length, 0.0);
    glColor3f(0.0, 0.0, 1.0);
    glVertex3f(0.0, 0.0, 0.0);
    glVertex3f(0.0, 0.0, axis_length);
    glEnd();

    float quad_size_min = axis_length * 0.1;
    float quad_size_max = axis_length;
    glBegin(GL_QUADS);

    glColor4f(1, 1, 1, 0.2);
    glVertex3f(quad_size_min, 0.0, quad_size_min);
    glVertex3f(quad_size_max, 0.0, quad_size_min);
    glVertex3f(quad_size_max, 0.0, quad_size_max);
    glVertex3f(quad_size_min, 0.0, quad_size_max);

    glColor4f(1, 1, 1, 0.2);
    glVertex3f(quad_size_min, quad_size_min, 0.0);
    glVertex3f(quad_size_max, quad_size_min, 0.0);
    glVertex3f(quad_size_max, quad_size_max, 0.0);
    glVertex3f(quad_size_min, quad_size_max, 0.0);

    glColor4f(1, 1, 1, 0.2);
    glVertex3f(0.0, quad_size_min, quad_size_min);
    glVertex3f(0.0, quad_size_max, quad_size_min);
    glVertex3f(0.0, quad_size_max, quad_size_max);
    glVertex3f(0.0, quad_size_min, quad_size_max);
    glEnd();    

    glPopMatrix();
    c_check_opengl_error();
}

// Draw a light represenatation in OpenGL.
void c_draw_opengl_light(pybind11::dict draw_dict, pybind11::dict light_dict) {
    glPushMatrix();
    c_setup_opengl_viewport(draw_dict);
    float line_width = 1.0f;
    for (auto item : light_dict) {
        auto light_prim_str = item.first.cast<pybind11::str>();
        auto light_data_dict = light_dict[light_prim_str].cast<pybind11::dict>();
        bool visibility = light_data_dict["visibility"].cast<bool>();
        float scale_factor;
        std::vector<float> light_color;
        std::vector<float> light_outer_color = { 0.75, 0.75, 0.25 };
        if (visibility) {
            scale_factor = 20.0;
            light_color = light_data_dict["color"].cast<std::vector<float>>();
        } else {
            scale_factor = 60.0;
            light_color = { 0.0, 0.0, 0.0 };
            light_outer_color = { 0.0, 0.0, 0.0 };
        }
        float widget_size = draw_dict["scene_bbox_size"].cast<pxr::GfVec3d>().GetLength() / scale_factor;
        pxr::GfMatrix4d light_matrix = light_data_dict["matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d light_direction = pxr::GfVec3d(0.0, 0.0, -1.0);

        glLineWidth(line_width);
        glBegin(GL_LINES);
        glColor3f(light_outer_color[0], light_outer_color[1], light_outer_color[2]);
        pxr::GfVec3d box_vertex_1 = light_matrix.Transform(pxr::GfVec3d(widget_size, widget_size, 0.0));
        pxr::GfVec3d box_vertex_2 = light_matrix.Transform(pxr::GfVec3d(-widget_size, widget_size, 0.0));
        pxr::GfVec3d box_vertex_3 = light_matrix.Transform(pxr::GfVec3d(-widget_size, -widget_size, 0.0));
        pxr::GfVec3d box_vertex_4 = light_matrix.Transform(pxr::GfVec3d(widget_size, -widget_size, 0.0));
        glVertex3d(box_vertex_1[0], box_vertex_1[1], box_vertex_1[2]);
        glVertex3d(box_vertex_2[0], box_vertex_2[1], box_vertex_2[2]);
        glVertex3d(box_vertex_2[0], box_vertex_2[1], box_vertex_2[2]);
        glVertex3d(box_vertex_3[0], box_vertex_3[1], box_vertex_3[2]);
        glVertex3d(box_vertex_3[0], box_vertex_3[1], box_vertex_3[2]);
        glVertex3d(box_vertex_4[0], box_vertex_4[1], box_vertex_4[2]);
        glVertex3d(box_vertex_4[0], box_vertex_4[1], box_vertex_4[2]);
        glVertex3d(box_vertex_1[0], box_vertex_1[1], box_vertex_1[2]);
        glEnd();


        glBegin(GL_LINES);
        pxr::GfVec3d direction_vertex_1 = light_matrix.ExtractTranslation();
        pxr::GfVec3d direction_vertex_2 = light_matrix.Transform(light_direction * widget_size);
        glColor3f(light_color[0], light_color[1], light_color[2]);
        glVertex3d(direction_vertex_1[0], direction_vertex_1[1], direction_vertex_1[2]);
        glVertex3d(direction_vertex_2[0], direction_vertex_2[1], direction_vertex_2[2]);
        glEnd();
        
        glBegin(GL_LINE_LOOP);
        glColor3f(light_outer_color[0], light_outer_color[1], light_outer_color[2]);
        int num_segments = 128;
        float radius = widget_size * 0.75;
        for (int index = 0; index < num_segments; ++index) 
        {
            float theta = 2.0f * M_PI * float(index) / float(num_segments);
            float x = radius * cosf(theta);
            float y = radius * sinf(theta);
            pxr::GfVec3d transformed_vertex = light_matrix.Transform(pxr::GfVec3d(x, y, 0.0));
            glVertex3d(transformed_vertex[0], transformed_vertex[1], transformed_vertex[2]);
        }
        glEnd();
    }
    glPopMatrix();
    c_check_opengl_error();
}

// Draw a direction/distance light represenatation in OpenGL.
void c_draw_opengl_camera(pybind11::dict draw_dict, pybind11::dict camera_dict) {
    glPushMatrix();
    c_setup_opengl_viewport(draw_dict);
    float line_width = 1.0f;
    for (auto item : camera_dict) {
        auto camera_prim_str = item.first.cast<pybind11::str>();
        auto camera_data_dict = camera_dict[camera_prim_str].cast<pybind11::dict>(); 
        bool visibility = camera_data_dict["visibility"].cast<bool>();  
        float scale_factor;
        std::vector<float> camera_color;
        if (visibility) {
            scale_factor = 50.0;
            camera_color = { 0.75, 0.25, 0.75 };
        } else {
            scale_factor = 150.0;
            camera_color = { 0.0, 0.0, 0.0 };
        }
        float widget_size = draw_dict["scene_bbox_size"].cast<pxr::GfVec3d>().GetLength() / scale_factor;
        pxr::GfMatrix4d camera_matrix = camera_data_dict["matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d direction_vector = pxr::GfVec3d(0.0, 0.0, -1.0);
        glLineWidth(line_width);
        glBegin(GL_LINES);
        pxr::GfVec3d direction_vertex_1 = camera_matrix.ExtractTranslation();
        pxr::GfVec3d direction_vertex_2 = camera_matrix.Transform(direction_vector * widget_size);
        glColor3f(camera_color[0], camera_color[1], camera_color[2]);
        glVertex3f(direction_vertex_1[0], direction_vertex_1[1], direction_vertex_1[2]);
        glVertex3f(direction_vertex_2[0], direction_vertex_2[1], direction_vertex_2[2]);
        glEnd();
        glBegin(GL_LINE_LOOP);
        glColor3f(camera_color[0], camera_color[1], camera_color[2]);
        int num_segments = 128;
        float radius = widget_size * 0.75;
        for (int index = 0; index < num_segments; ++index) {
            float theta = 2.0f * M_PI * float(index) / float(num_segments);
            float x = radius * cosf(theta);
            float y = radius * sinf(theta);
            pxr::GfVec3d transformed_vertex = camera_matrix.Transform(pxr::GfVec3d(x, y, 0.0));
            glVertex3f(transformed_vertex[0], transformed_vertex[1], transformed_vertex[2]);
        }
        glEnd();
        glBegin(GL_LINE_LOOP);
        glColor3f(camera_color[0], camera_color[1], camera_color[2]);
        for (int index = 0; index < num_segments; ++index) {
            float theta = 2.0f * M_PI * float(index) / float(num_segments);
            float x = radius * cosf(theta);
            float y = radius * sinf(theta);
            pxr::GfVec3d transformed_vertex = camera_matrix.Transform(pxr::GfVec3d(x, y, widget_size));
            glVertex3f(transformed_vertex[0], transformed_vertex[1], transformed_vertex[2]);
        }
        glEnd();
        glBegin(GL_LINES);
        glColor3f(camera_color[0], camera_color[1], camera_color[2]);
        pxr::GfVec3d camera_edge_vert_1 = camera_matrix.Transform(pxr::GfVec3d(radius, 0.0, 0.0));
        pxr::GfVec3d camera_edge_vert_2 = camera_matrix.Transform(pxr::GfVec3d(radius, 0.0, widget_size));
        pxr::GfVec3d camera_edge_vert_3 = camera_matrix.Transform(pxr::GfVec3d(0.0, radius, 0.0));
        pxr::GfVec3d camera_edge_vert_4 = camera_matrix.Transform(pxr::GfVec3d(0.0, radius, widget_size));
        pxr::GfVec3d camera_edge_vert_5 = camera_matrix.Transform(pxr::GfVec3d(-radius, 0.0, 0.0));
        pxr::GfVec3d camera_edge_vert_6 = camera_matrix.Transform(pxr::GfVec3d(-radius, 0.0, widget_size));
        pxr::GfVec3d camera_edge_vert_7 = camera_matrix.Transform(pxr::GfVec3d(0.0, -radius, 0.0));
        pxr::GfVec3d camera_edge_vert_8 = camera_matrix.Transform(pxr::GfVec3d(0.0, -radius, widget_size));
        glVertex3f(camera_edge_vert_1[0], camera_edge_vert_1[1], camera_edge_vert_1[2]);
        glVertex3f(camera_edge_vert_2[0], camera_edge_vert_2[1], camera_edge_vert_2[2]);
        glVertex3f(camera_edge_vert_3[0], camera_edge_vert_3[1], camera_edge_vert_3[2]);
        glVertex3f(camera_edge_vert_4[0], camera_edge_vert_4[1], camera_edge_vert_4[2]);
        glVertex3f(camera_edge_vert_5[0], camera_edge_vert_5[1], camera_edge_vert_5[2]);
        glVertex3f(camera_edge_vert_6[0], camera_edge_vert_6[1], camera_edge_vert_6[2]);
        glVertex3f(camera_edge_vert_7[0], camera_edge_vert_7[1], camera_edge_vert_7[2]);
        glVertex3f(camera_edge_vert_8[0], camera_edge_vert_8[1], camera_edge_vert_8[2]);
        glEnd();
    }
    glPopMatrix();
    c_check_opengl_error();
}


// Init GLAD/OpenGL settings
void c_init_glad() {
    if (!gladLoadGL()) {
        std::cerr << "Failed to initialize GLAD" << std::endl;
        return;
    }
    else {
        c_init_opengl_settings();
        c_check_opengl_error();
    }
}


PYBIND11_MODULE(c_draw_opengl, m) {
    m.def("c_init_glad", &c_init_glad, "Initialize GLAD");  
    m.def("c_init_opengl_settings", &c_init_opengl_settings, "Initialize OpenGL Settings");
    m.def("c_setup_opengl_viewport", &c_setup_opengl_viewport, "Setup OpenGL Viewport",
          pybind11::arg("draw_dict"));
    m.def("c_draw_opengl_bone", &c_draw_opengl_bone, "Draw OpenGL Bone Visualization",
          pybind11::arg("bone_list"),
          pybind11::arg("draw_dict"));
    m.def("c_draw_opengl_bone_xray", &c_draw_opengl_bone_xray, "Draw OpenGL Bone Xray Visualization",
          pybind11::arg("bone_list"),
          pybind11::arg("draw_dict"));
    m.def("c_draw_opengl_gizmo", &c_draw_opengl_gizmo, "Draw OpenGL Gizmo",
          pybind11::arg("draw_dict"));
    m.def("c_draw_opengl_grid", &c_draw_opengl_grid, "Draw OpenGL Grid Plane",
          pybind11::arg("draw_dict"));
    m.def("c_draw_opengl_light", &c_draw_opengl_light, "Draw OpenGL Light",
          pybind11::arg("draw_dict"),
          pybind11::arg("light_dict"));
    m.def("c_draw_opengl_camera", &c_draw_opengl_camera, "Draw OpenGL Camera",
          pybind11::arg("draw_dict"),
          pybind11::arg("camera_dict"));

}

