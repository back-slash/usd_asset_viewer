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
#include <string>
#include <array>
#include <memory>
#include <fstream>
#include <sstream>

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

#undef min
#undef max

// Project
#include "c_utils.cpp"


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

std::string load_shader_source(const std::string& filename) {
    std::ifstream file(filename);
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

GLuint create_shader(GLenum type, const char* src) {
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &src, nullptr);
    glCompileShader(shader);
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    return shader;
}

GLuint create_program() {
    std::string vertex_shader_src = load_shader_source("src/shader_generic.vs");
    std::string fragment_shader_src = load_shader_source("src/shader_generic.fs");
    GLuint vs = create_shader(GL_VERTEX_SHADER, vertex_shader_src.c_str());
    GLuint fs = create_shader(GL_FRAGMENT_SHADER, fragment_shader_src.c_str());
    GLuint program_id = glCreateProgram();
    glAttachShader(program_id, vs);
    glAttachShader(program_id, fs);
    glLinkProgram(program_id);
    glDeleteShader(vs);
    glDeleteShader(fs);
    return program_id;
}

struct vertex {
    double pos[3];
    double normal[3];
    float color[4];
};

const pxr::GfMatrix4d c_create_projection_matrix(pybind11::dict draw_dict) {
    int panel_width = draw_dict["panel_width"].cast<int>();
    int panel_height = draw_dict["panel_height"].cast<int>();
    double fov = draw_dict["fov"].cast<double>();
    double aspect = double(panel_width) / double(panel_height);
    double near_plane = draw_dict["near_z"].cast<double>();
    double far_plane = draw_dict["far_z"].cast<double>();
    double f = 1.0 / tan(fov * 0.5 * M_PI / 180.0);
    pxr::GfMatrix4d projection;
    projection.SetIdentity();
    projection[0][0] = f / aspect;
    projection[1][1] = f;
    projection[2][2] = (far_plane + near_plane) / (near_plane - far_plane);
    projection[2][3] = -1.0;
    projection[3][2] = (2.0 * far_plane * near_plane) / (near_plane - far_plane);
    projection[3][3] = 0.0;
    return projection;
}

// Draw bones for standalone visualization
void c_draw_opengl_modern_bone(pybind11::list bone_list, pybind11::dict draw_dict) {
    static GLuint shader_program = 0;
    static GLuint vao = 0, vbo = 0;
    if (!shader_program) {
        shader_program = create_program();
        glGenVertexArrays(1, &vao);
        glGenBuffers(1, &vbo);

        glBindVertexArray(vao);
        glBindBuffer(GL_ARRAY_BUFFER, vbo);

        glEnableVertexAttribArray(0); // position
        glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, sizeof(vertex), (void*)0);

        glEnableVertexAttribArray(1); // normal
        glVertexAttribPointer(1, 3, GL_DOUBLE, GL_FALSE, sizeof(vertex), (void*)(3 * sizeof(double)));

        glEnableVertexAttribArray(2); // color
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, sizeof(vertex), (void*)(6 * sizeof(double)));

        glBindVertexArray(0);
    }
    glUseProgram(shader_program);
    float line_width = 3.0f;
    struct light_struct {
        std::array<float, 3> color;
        pxr::GfMatrix4d matrix;
    };
    std::vector<light_struct> lights;

    pybind11::dict light_dict = draw_dict["light_dict"].cast<pybind11::dict>();
    int light_idx = 0;
    for (auto item : light_dict) {
        pybind11::dict light_info = item.second.cast<pybind11::dict>();
        if (!light_info["visibility"].cast<bool>()) {
            continue;
        }
        std::array<float, 3> color = light_info["color"].cast<std::array<float, 3>>();
        pxr::GfMatrix4d matrix = light_info["matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d light_dir_vec = matrix.TransformDir(pxr::GfVec3d(0, 0, -1)).GetNormalized();
        lights.push_back({color, matrix});
        ++light_idx;
    }
    GLint light_count = glGetUniformLocation(shader_program, "light_count");
    glUniform1i(light_count, light_idx); 
    std::vector<float> light_dirs;
    std::vector<float> light_colors;
    for (const auto& light : lights) {
        pxr::GfMatrix4d light_matrix = light.matrix;
        pxr::GfMatrix4d light_rotation_matrix = light_matrix.SetTranslateOnly(pxr::GfVec3d(0, 0, 0));
        pxr::GfVec3d light_position = light.matrix.ExtractTranslation();
        pxr::GfVec3d light_direction_position = light_rotation_matrix.Transform(pxr::GfVec3d(0, 0, -1));
        pxr::GfVec3d light_normal = light_position - light_direction_position;
        light_normal = light_normal.GetNormalized();
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
    while (light_dirs.size() < MAX_LIGHTS * 3) light_dirs.push_back(0.0f);
    while (light_colors.size() < MAX_LIGHTS * 3) light_colors.push_back(0.0f);
    glUniform3fv(light_direction_id, MAX_LIGHTS, light_dirs.data());
    glUniform3fv(light_color_id, MAX_LIGHTS, light_colors.data());
    int hydra_x_min = draw_dict["hydra_x_min"].cast<int>();
    int hydra_y_min = draw_dict["hydra_y_min"].cast<int>();
    int panel_width = draw_dict["panel_width"].cast<int>();
    int panel_height = draw_dict["panel_height"].cast<int>();
    glViewport(hydra_x_min, hydra_y_min, panel_width, panel_height);

    auto projection = c_create_projection_matrix(draw_dict);
    pxr::GfMatrix4d camera_matrix = draw_dict["camera_matrix"].cast<pxr::GfMatrix4d>().GetInverse();
    pxr::GfMatrix4d mvp = camera_matrix * projection;
    float mvp_matrix[16];
    for (int row = 0; row < 4; ++row) {
        for (int col = 0; col < 4; ++col) {
            mvp_matrix[row * 4 + col] = mvp[row][col];
        }
    }
    GLint mvp_id = glGetUniformLocation(shader_program, "mvp");    
    glUniformMatrix4fv(mvp_id, 1, GL_FALSE, mvp_matrix);
    glBindVertexArray(vao);

    std::vector<vertex> axis_vertices;
    std::vector<vertex> tri_vertices;
    std::vector<vertex> line_vertices;
    

    for (auto bone : bone_list) {
        bool selected = bone.attr("get_selected")().cast<bool>();
        std::array<float, 4> line_color = selected ? std::array<float,4>{0.0f, 0.5f, 0.5f, 1.0f} : std::array<float,4>{0.5f, 0.5f, 0.5f, 1.0f};
        std::array<float, 4> face_color = selected ? std::array<float,4>{0.0f, 0.33f, 0.33f, 1.0f} : std::array<float,4>{0.33f, 0.33f, 0.33f, 1.0f};
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pxr::GfMatrix4d bone_matrix = data_dict["anim_matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();
        pybind11::list bone_children = bone.attr("get_child_nodes")();
        
        
        if (selected) {
            pxr::GfVec3d camera_normal = pxr::GfVec3d(0.0, 0.0, -1.0);
            pxr::GfVec3d camera_position = camera_matrix.ExtractTranslation();
            pxr::GfMatrix4d camera_rotation_matrix = camera_matrix.SetTranslateOnly(pxr::GfVec3d(0.0, 0.0, 0.0));
            pxr::GfVec3d camera_z_position = camera_rotation_matrix.Transform(camera_normal);
            pxr::GfVec3d normal = camera_z_position - camera_position;
            normal = normal.GetNormalized();
            pxr::GfVec3d x_axis = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));
            pxr::GfVec3d y_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 0.0));
            pxr::GfVec3d z_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 0.0, 1.0));

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

        auto add_tri = [&](const pxr::GfVec3d& a, const pxr::GfVec3d& b, const pxr::GfVec3d& c) {
            pxr::GfVec3d normal = pxr::GfCross(b - a, b - c).GetNormalized();
            std::array<float, 3> n = {normal[0], normal[1], normal[2]};
            vertex v1, v2, v3;
            v1.pos[0] = a[0]; v1.pos[1] = a[1]; v1.pos[2] = a[2];
            v2.pos[0] = b[0]; v2.pos[1] = b[1]; v2.pos[2] = b[2];
            v3.pos[0] = c[0]; v3.pos[1] = c[1]; v3.pos[2] = c[2];
            v1.normal[0] = n[0]; v1.normal[1] = n[1]; v1.normal[2] = n[2];
            v2.normal[0] = n[0]; v2.normal[1] = n[1]; v2.normal[2] = n[2];
            v3.normal[0] = n[0]; v3.normal[1] = n[1]; v3.normal[2] = n[2];
            v1.color[0] = face_color[0]; v1.color[1] = face_color[1]; v1.color[2] = face_color[2]; v1.color[3] = face_color[3];
            v2.color[0] = face_color[0]; v2.color[1] = face_color[1]; v2.color[2] = face_color[2]; v2.color[3] = face_color[3];
            v3.color[0] = face_color[0]; v3.color[1] = face_color[1]; v3.color[2] = face_color[2]; v3.color[3] = face_color[3];
            tri_vertices.push_back(v1);
            tri_vertices.push_back(v2);
            tri_vertices.push_back(v3);
        };        

        if (bone_children.size() == 0) {
            pxr::GfVec3d end_bone_start_vert = bone_matrix.Transform(pxr::GfVec3d(-1.0, 0.0, 0.0));
            pxr::GfVec3d end_bone_vert_1 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 1.0));
            pxr::GfVec3d end_bone_vert_2 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, 1.0));
            pxr::GfVec3d end_bone_vert_3 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, -1.0));
            pxr::GfVec3d end_bone_vert_4 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, -1.0));
            pxr::GfVec3d end_bone_end_vert = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));

            add_tri(end_bone_start_vert, end_bone_vert_1, end_bone_vert_2);
            add_tri(end_bone_start_vert, end_bone_vert_2, end_bone_vert_3);
            add_tri(end_bone_start_vert, end_bone_vert_3, end_bone_vert_4);
            add_tri(end_bone_start_vert, end_bone_vert_4, end_bone_vert_1);

            add_tri(end_bone_end_vert, end_bone_vert_1, end_bone_vert_2);
            add_tri(end_bone_end_vert, end_bone_vert_2, end_bone_vert_3);
            add_tri(end_bone_end_vert, end_bone_vert_3, end_bone_vert_4);
            add_tri(end_bone_end_vert, end_bone_vert_4, end_bone_vert_1);

            add_tri(end_bone_vert_1, end_bone_vert_2, end_bone_vert_3);
            add_tri(end_bone_vert_1, end_bone_vert_3, end_bone_vert_4);
            add_tri(end_bone_vert_1, end_bone_vert_4, end_bone_end_vert);
            add_tri(end_bone_vert_2, end_bone_vert_3, end_bone_end_vert);
            add_tri(end_bone_vert_3, end_bone_vert_4, end_bone_end_vert);
            add_tri(end_bone_vert_4, end_bone_vert_1, end_bone_end_vert);
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
            pxr::GfVec3d up(0.0, 0.0, 1.0);
            pxr::GfMatrix4d bone_world_matrix = calc_look_at_x(root_vert, child_root_vert, up);
            pxr::GfVec3d bone_middle_vert_1 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_2 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, bone_radius));
            pxr::GfVec3d bone_middle_vert_3 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, -bone_radius, -bone_radius));
            pxr::GfVec3d bone_middle_vert_4 = bone_world_matrix.Transform(pxr::GfVec3d(bone_spur, bone_radius, -bone_radius));
            pxr::GfVec3d calc_end_vert = child_root_vert;
            
            add_tri(root_vert, bone_middle_vert_1, bone_middle_vert_2);
            add_tri(root_vert, bone_middle_vert_2, bone_middle_vert_3);
            add_tri(root_vert, bone_middle_vert_3, bone_middle_vert_4);
            add_tri(root_vert, bone_middle_vert_4, bone_middle_vert_1);
            add_tri(calc_end_vert, bone_middle_vert_2, bone_middle_vert_1);
            add_tri(calc_end_vert, bone_middle_vert_3, bone_middle_vert_2);
            add_tri(calc_end_vert, bone_middle_vert_4, bone_middle_vert_3);
            add_tri(calc_end_vert, bone_middle_vert_1, bone_middle_vert_4);
        }
    }

    // Upload and draw triangles
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    if (!tri_vertices.empty()) {
        glBufferData(GL_ARRAY_BUFFER, tri_vertices.size() * sizeof(vertex), tri_vertices.data(), GL_DYNAMIC_DRAW);
        glDrawArrays(GL_TRIANGLES, 0, tri_vertices.size());
    }
    // Upload and draw lines
    if (!line_vertices.empty()) {
        glBufferData(GL_ARRAY_BUFFER, line_vertices.size() * sizeof(vertex), line_vertices.data(), GL_DYNAMIC_DRAW);
        glLineWidth(line_width);
        glDrawArrays(GL_LINES, 0, line_vertices.size());
    }
    // Upload and draw axes
    if (!axis_vertices.empty()) {
        glBufferData(GL_ARRAY_BUFFER, axis_vertices.size() * sizeof(vertex), axis_vertices.data(), GL_DYNAMIC_DRAW);
        glLineWidth(1.0f);
        glDrawArrays(GL_LINES, 0, axis_vertices.size());
    }
    glBindVertexArray(0);
    glUseProgram(0);
    c_check_opengl_error();
}




