///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ OpenGL Modern Draw
// TODO:
// 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Define
#define NOMINMAX
#pragma once

// C++
#include <iostream>
#include <vector>

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
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/sdf/path.h>

// OpenGL
#include <glad/glad.h>

// Project
#include "c_utils.cpp"
#include "c_static.cpp"

#undef min
#undef max

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



void c_draw_opengl_modern_axis(std::vector<vertex_data>& axis_vertices, pxr::GfMatrix4d bone_matrix) {
    pxr::GfVec3d normal = calc_axis_normal(bone_matrix, pxr::GfVec3d(0.0, 0.0, -1.0));
    pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();    
    double axis_length = 2.0;
    pxr::GfVec3d x_axis = bone_matrix.Transform(pxr::GfVec3d(axis_length, 0.0, 0.0));
    pxr::GfVec3d y_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, axis_length, 0.0));
    pxr::GfVec3d z_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 0.0, axis_length));
    axis_vertices.push_back({
        {root_vert[0], root_vert[1], root_vert[2]},
        {normal[0], normal[1], normal[2]},
        {1.0f, 0.0f, 0.0f, 1.0f}
    });
    axis_vertices.push_back({
        {x_axis[0], x_axis[1], x_axis[2]},
        {normal[0], normal[1], normal[2]},
        {1.0f, 0.0f, 0.0f, 1.0f}
    });
    axis_vertices.push_back({
        {root_vert[0], root_vert[1], root_vert[2]},
        {normal[0], normal[1], normal[2]},
        {0.0f, 1.0f, 0.0f, 1.0f}
    });
    axis_vertices.push_back({
        {y_axis[0], y_axis[1], y_axis[2]},
        {normal[0], normal[1], normal[2]},
        {0.0f, 1.0f, 0.0f, 1.0f}
    });
    axis_vertices.push_back({
        {root_vert[0], root_vert[1], root_vert[2]},
        {normal[0], normal[1], normal[2]},
        {0.0f, 0.0f, 1.0f, 1.0f}
    });
    axis_vertices.push_back({
        {z_axis[0], z_axis[1], z_axis[2]},
        {normal[0], normal[1], normal[2]},
        {0.0f, 0.0f, 1.0f, 1.0f}
    });    
}


// Draw bones for standalone visualization
void c_draw_opengl_modern_bone(pybind11::list bone_list, pybind11::dict draw_dict) {
    static GLuint shader_program = 0;
    static GLuint vao = 0;
    static GLuint vbo = 0;
    if (!shader_program) {
        shader_program = create_program();
        glGenVertexArrays(1, &vao);
        glGenBuffers(1, &vbo);

        glBindBuffer(GL_ARRAY_BUFFER, vbo);

        glBindVertexArray(vao);
        
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, sizeof(vertex_data), (void*)offsetof(vertex_data, position));

        glEnableVertexAttribArray(1);
        glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, sizeof(vertex_data), (void*)offsetof(vertex_data, normal));

        glEnableVertexAttribArray(2);
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, sizeof(vertex_data), (void*)offsetof(vertex_data, color));
    }
    glUseProgram(shader_program);
    float line_width = 3.0f;

    std::vector<light_data> lights;

    pybind11::dict light_dict = draw_dict["light_dict"].cast<pybind11::dict>();
    int light_idx = 0;
    for (auto item : light_dict) {
        pybind11::dict light_info = item.second.cast<pybind11::dict>();
        if (!light_info["visibility"].cast<bool>()) {
            continue;
        }
        std::vector<float> color = light_info["color"].cast<std::vector<float>>();
        pxr::GfMatrix4d matrix = light_info["matrix"].cast<pxr::GfMatrix4d>();
        float intensity = 1.0;
        lights.push_back({color, intensity, matrix});
        ++light_idx;
    }
    GLint light_count = glGetUniformLocation(shader_program, "light_count");
    glUniform1i(light_count, light_idx); 
    std::vector<float> light_dirs;
    std::vector<float> light_colors;
    for (const auto& light : lights) {
        pxr::GfVec3d light_normal = calc_axis_normal(light.matrix, pxr::GfVec3d(0.0, 0.0, -1.0));
        light_dirs.push_back(light_normal[0]);
        light_dirs.push_back(light_normal[1]);
        light_dirs.push_back(light_normal[2]);
        light_colors.push_back(light.color[0]);
        light_colors.push_back(light.color[1]);
        light_colors.push_back(light.color[2]);
    }
    GLint light_direction_id = glGetUniformLocation(shader_program, "light_direction");
    GLint light_color_id = glGetUniformLocation(shader_program, "light_color");
    const int MAX_LIGHTS = 8;
    glUniform3fv(light_direction_id, MAX_LIGHTS, light_dirs.data());
    glUniform3fv(light_color_id, MAX_LIGHTS, light_colors.data());
    
    int hydra_x_min = draw_dict["hydra_x_min"].cast<int>();
    int hydra_y_min = draw_dict["hydra_y_min"].cast<int>();
    int panel_width = draw_dict["panel_width"].cast<int>();
    int panel_height = draw_dict["panel_height"].cast<int>();
    
    glViewport(hydra_x_min, hydra_y_min, panel_width, panel_height);

    pxr::GfMatrix4d projection = c_create_projection_matrix(draw_dict);
    pxr::GfMatrix4d camera_matrix = draw_dict["camera_matrix"].cast<pxr::GfMatrix4d>().GetInverse();
    pxr::GfMatrix4d mvp = camera_matrix * projection;
    float mvp_matrix[16];
    convert_matrix_usd_f_gl(mvp, mvp_matrix);
    GLint mvp_id = glGetUniformLocation(shader_program, "mvp");    
    glUniformMatrix4fv(mvp_id, 1, GL_FALSE, mvp_matrix);

    std::vector<vertex_data> axis_vertices;
    std::vector<vertex_data> tri_vertices;
    std::vector<vertex_data> tri_selected_vertices;

    for (auto bone : bone_list) {
        bool selected = bone.attr("get_selected")().cast<bool>();
        std::vector<float> face_color = {0.33f, 0.33f, 0.33f, 1.0f};
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pxr::GfMatrix4d bone_matrix = data_dict["anim_matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();
        pybind11::list bone_children = bone.attr("get_child_nodes")();
        
        if (selected) {
            face_color = {0.0f, 0.33f, 0.33f, 1.0f};
            c_draw_opengl_modern_axis(axis_vertices, bone_matrix);
        }

        if (bone_children.size() == 0) {
            pxr::GfVec3d end_bone_start_vert = bone_matrix.Transform(pxr::GfVec3d(-1.0, 0.0, 0.0));
            pxr::GfVec3d end_bone_vert_1 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 1.0));
            pxr::GfVec3d end_bone_vert_2 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, 1.0));
            pxr::GfVec3d end_bone_vert_3 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, -1.0));
            pxr::GfVec3d end_bone_vert_4 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, -1.0));
            pxr::GfVec3d end_bone_end_vert = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));

            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_start_vert, end_bone_vert_1, end_bone_vert_2);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_start_vert, end_bone_vert_2, end_bone_vert_3);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_start_vert, end_bone_vert_3, end_bone_vert_4);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_start_vert, end_bone_vert_4, end_bone_vert_1);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_end_vert, end_bone_vert_1, end_bone_vert_2);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_end_vert, end_bone_vert_2, end_bone_vert_3);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_end_vert, end_bone_vert_3, end_bone_vert_4);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_end_vert, end_bone_vert_4, end_bone_vert_1);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_vert_1, end_bone_vert_2, end_bone_vert_3);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_vert_1, end_bone_vert_3, end_bone_vert_4);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_vert_1, end_bone_vert_4, end_bone_end_vert);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_vert_2, end_bone_vert_3, end_bone_end_vert);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_vert_3, end_bone_vert_4, end_bone_end_vert);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, end_bone_vert_4, end_bone_vert_1, end_bone_end_vert);
        }
        for (auto child : bone_children) {
            pybind11::dict child_data_dict = child.attr("get_data_object")();
            pxr::GfMatrix4d child_matrix = child_data_dict["anim_matrix"].cast<pxr::GfMatrix4d>();
            pxr::GfVec3d child_root_vert = child_matrix.ExtractTranslation();
            double bone_length = (child_root_vert - root_vert).GetLength();
            if (bone_length < 0.1) {
                continue;
            }
            double bone_spur = bone_length * 0.2;
            double bone_radius = bone_length / 25.0;
            const pxr::GfVec3d up(0.0, 0.0, 1.0);
            pxr::GfMatrix4d bone_world_matrix = calc_look_at_x(root_vert, child_root_vert, up);
            pxr::GfVec3d bone_middle_vert_1 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_2 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_3 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, -bone_radius));
            pxr::GfVec3d bone_middle_vert_4 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, -bone_radius));
            pxr::GfVec3d calc_end_vert = child_root_vert;
            
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, root_vert, bone_middle_vert_1, bone_middle_vert_2);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, root_vert, bone_middle_vert_2, bone_middle_vert_3);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, root_vert, bone_middle_vert_3, bone_middle_vert_4);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, root_vert, bone_middle_vert_4, bone_middle_vert_1);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, calc_end_vert, bone_middle_vert_2, bone_middle_vert_1);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, calc_end_vert, bone_middle_vert_3, bone_middle_vert_2);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, calc_end_vert, bone_middle_vert_4, bone_middle_vert_3);
            add_triangle(selected ? tri_selected_vertices : tri_vertices, face_color, calc_end_vert, bone_middle_vert_1, bone_middle_vert_4);
        }
    }
    
    glBindVertexArray(vao);

    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    if (!tri_vertices.empty()) {
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        glBufferData(GL_ARRAY_BUFFER, tri_vertices.size() * sizeof(vertex_data), tri_vertices.data(), GL_DYNAMIC_DRAW);
        glDrawArrays(GL_TRIANGLES, 0, tri_vertices.size());
    }
    if (!tri_selected_vertices.empty()) {
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        glBufferData(GL_ARRAY_BUFFER, tri_selected_vertices.size() * sizeof(vertex_data), tri_selected_vertices.data(), GL_DYNAMIC_DRAW);
        glDrawArrays(GL_TRIANGLES, 0, tri_selected_vertices.size());
    }
    glDisable(GL_DEPTH_TEST);    
    if (!axis_vertices.empty()) {
        glBufferData(GL_ARRAY_BUFFER, axis_vertices.size() * sizeof(vertex_data), axis_vertices.data(), GL_DYNAMIC_DRAW);
        glLineWidth(line_width);
        glDrawArrays(GL_LINES, 0, axis_vertices.size());
    }

    glEnable(GL_DEPTH_TEST);
    glBindVertexArray(0);
    glUseProgram(0);
    
    c_check_opengl_error();
}




