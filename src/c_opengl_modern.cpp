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




// Modern OpenGL helpers (minimal, for demonstration)
const char* vertexShaderSource = R"(
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec4 aColor;
out vec4 vColor;
void main() {
    gl_Position = vec4(aPos, 1.0);
    vColor = aColor;
}
)";

const char* fragmentShaderSource = R"(
#version 330 core
in vec4 vColor;
out vec4 FragColor;
void main() {
    FragColor = vColor;
}
)";

GLuint create_shader(GLenum type, const char* src) {
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &src, nullptr);
    glCompileShader(shader);
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        char infoLog[512];
        glGetShaderInfoLog(shader, 512, nullptr, infoLog);
        std::cerr << "Shader compile error: " << infoLog << std::endl;
    }
    return shader;
}

GLuint create_program() {
    GLuint vs = create_shader(GL_VERTEX_SHADER, vertexShaderSource);
    GLuint fs = create_shader(GL_FRAGMENT_SHADER, fragmentShaderSource);
    GLuint prog = glCreateProgram();
    glAttachShader(prog, vs);
    glAttachShader(prog, fs);
    glLinkProgram(prog);
    glDeleteShader(vs);
    glDeleteShader(fs);
    return prog;
}

struct vertex {
    float pos[3];
    float color[4];
};

// Draw bones for standalone visualization
void c_draw_opengl_bone(pybind11::list bone_list, pybind11::dict draw_dict) {
    static GLuint shader_program = 0;
    static GLuint vao = 0, vbo = 0;
    if (!shader_program) {
        shader_program = create_program();
        glGenVertexArrays(1, &vao);
        glGenBuffers(1, &vbo);
    }
    glUseProgram(shader_program);
    glBindVertexArray(vao);

    c_setup_opengl_viewport(draw_dict);
    std::vector<vertex> vertices;
    float line_width = 2.0f;

    for (auto bone : bone_list) {
        bool selected = bone.attr("get_selected")().cast<bool>();
        std::array<float, 4> line_color = selected ? std::array<float,4>{0.0f, 0.5f, 0.5f, 1.0f} : std::array<float,4>{0.5f, 0.5f, 0.5f, 1.0f};
        std::array<float, 4> face_color = selected ? std::array<float,4>{0.0f, 0.33f, 0.33f, 1.0f} : std::array<float,4>{0.33f, 0.33f, 0.33f, 1.0f};
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pxr::GfMatrix4d bone_matrix = data_dict["anim_matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();
        pybind11::list bone_children = bone.attr("get_child_nodes")();

        if (selected) {
            // Draw axes as colored lines
            pxr::GfVec3d x_axis = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));
            pxr::GfVec3d y_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 0.0));
            pxr::GfVec3d z_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 0.0, 1.0));
            // X axis (red)
            vertices.push_back({{(float)root_vert[0], (float)root_vert[1], (float)root_vert[2]}, {1.0f, 0.0f, 0.0f, 1.0f}});
            vertices.push_back({{(float)x_axis[0], (float)x_axis[1], (float)x_axis[2]}, {1.0f, 0.0f, 0.0f, 1.0f}});
            // Y axis (green)
            vertices.push_back({{(float)root_vert[0], (float)root_vert[1], (float)root_vert[2]}, {0.0f, 1.0f, 0.0f, 1.0f}});
            vertices.push_back({{(float)y_axis[0], (float)y_axis[1], (float)y_axis[2]}, {0.0f, 1.0f, 0.0f, 1.0f}});
            // Z axis (blue)
            vertices.push_back({{(float)root_vert[0], (float)root_vert[1], (float)root_vert[2]}, {0.0f, 0.0f, 1.0f, 1.0f}});
            vertices.push_back({{(float)z_axis[0], (float)z_axis[1], (float)z_axis[2]}, {0.0f, 0.0f, 1.0f, 1.0f}});
        }

        if (bone_children.size() == 0) {
            // End bone geometry (lines only for demo)
            pxr::GfVec3d end_bone_start_vert = bone_matrix.Transform(pxr::GfVec3d(-1.0, 0.0, 0.0));
            pxr::GfVec3d end_bone_vert_1 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, 1.0));
            pxr::GfVec3d end_bone_vert_2 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, 1.0));
            pxr::GfVec3d end_bone_vert_3 = bone_matrix.Transform(pxr::GfVec3d(0.0, -1.0, -1.0));
            pxr::GfVec3d end_bone_vert_4 = bone_matrix.Transform(pxr::GfVec3d(0.0, 1.0, -1.0));
            pxr::GfVec3d end_bone_end_vert = bone_matrix.Transform(pxr::GfVec3d(1.0, 0.0, 0.0));
            // Lines
            auto add_line = [&](const pxr::GfVec3d& a, const pxr::GfVec3d& b) {
                vertices.push_back({{(float)a[0], (float)a[1], (float)a[2]}, {line_color[0], line_color[1], line_color[2], line_color[3]}});
                vertices.push_back({{(float)b[0], (float)b[1], (float)b[2]}, {line_color[0], line_color[1], line_color[2], line_color[3]}});
            };
            add_line(end_bone_start_vert, end_bone_vert_1);
            add_line(end_bone_start_vert, end_bone_vert_2);
            add_line(end_bone_start_vert, end_bone_vert_3);
            add_line(end_bone_start_vert, end_bone_vert_4);
            add_line(end_bone_end_vert, end_bone_vert_1);
            add_line(end_bone_end_vert, end_bone_vert_2);
            add_line(end_bone_end_vert, end_bone_vert_3);
            add_line(end_bone_end_vert, end_bone_vert_4);
            add_line(end_bone_vert_1, end_bone_vert_2);
            add_line(end_bone_vert_2, end_bone_vert_3);
            add_line(end_bone_vert_3, end_bone_vert_4);
            add_line(end_bone_vert_4, end_bone_vert_1);
            // (Triangles for faces can be added similarly if needed)
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
            // Triangles (faces)
            auto add_tri = [&](const pxr::GfVec3d& a, const pxr::GfVec3d& b, const pxr::GfVec3d& c) {
                vertices.push_back({{(float)a[0], (float)a[1], (float)a[2]}, {face_color[0], face_color[1], face_color[2], face_color[3]}});
                vertices.push_back({{(float)b[0], (float)b[1], (float)b[2]}, {face_color[0], face_color[1], face_color[2], face_color[3]}});
                vertices.push_back({{(float)c[0], (float)c[1], (float)c[2]}, {face_color[0], face_color[1], face_color[2], face_color[3]}});
            };
            add_tri(root_vert, bone_middle_vert_1, bone_middle_vert_2);
            add_tri(root_vert, bone_middle_vert_2, bone_middle_vert_3);
            add_tri(root_vert, bone_middle_vert_3, bone_middle_vert_4);
            add_tri(root_vert, bone_middle_vert_4, bone_middle_vert_1);
            add_tri(calc_end_vert, bone_middle_vert_1, bone_middle_vert_2);
            add_tri(calc_end_vert, bone_middle_vert_2, bone_middle_vert_3);
            add_tri(calc_end_vert, bone_middle_vert_3, bone_middle_vert_4);
            add_tri(calc_end_vert, bone_middle_vert_4, bone_middle_vert_1);
            // Lines (edges)
            auto add_line = [&](const pxr::GfVec3d& a, const pxr::GfVec3d& b) {
                vertices.push_back({{(float)a[0], (float)a[1], (float)a[2]}, {line_color[0], line_color[1], line_color[2], line_color[3]}});
                vertices.push_back({{(float)b[0], (float)b[1], (float)b[2]}, {line_color[0], line_color[1], line_color[2], line_color[3]}});
            };
            add_line(root_vert, bone_middle_vert_1);
            add_line(root_vert, bone_middle_vert_2);
            add_line(root_vert, bone_middle_vert_3);
            add_line(root_vert, bone_middle_vert_4);
            add_line(calc_end_vert, bone_middle_vert_1);
            add_line(calc_end_vert, bone_middle_vert_2);
            add_line(calc_end_vert, bone_middle_vert_3);
            add_line(calc_end_vert, bone_middle_vert_4);
            add_line(bone_middle_vert_1, bone_middle_vert_2);
            add_line(bone_middle_vert_2, bone_middle_vert_3);
            add_line(bone_middle_vert_3, bone_middle_vert_4);
            add_line(bone_middle_vert_4, bone_middle_vert_1);
        }
    }

    // Upload and draw
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(vertex), vertices.data(), GL_DYNAMIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(vertex), (void*)0);
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, sizeof(vertex), (void*)(3 * sizeof(float)));
    glLineWidth(line_width);
    if (!vertices.empty()) {
        size_t tri_count = (vertices.size() / 3) * 3;
        if (tri_count > 0) {
            glDrawArrays(GL_TRIANGLES, 0, tri_count);
        }
        size_t line_start = tri_count;
        size_t line_count = vertices.size() - tri_count;
        if (line_count > 0) {
            glDrawArrays(GL_LINES, line_start, line_count);
        }
    }
    glBindVertexArray(0);
    glUseProgram(0);
    c_check_opengl_error();
}