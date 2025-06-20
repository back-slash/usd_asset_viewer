///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Draw Utilities
// TODO:
// 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Define
#pragma once

// C++
#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <fstream>

// PyBind11
#include "usd_pybind_cast.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// OpenUSD
#include <pxr/base/gf/matrix4d.h>
#include <pxr/base/gf/rotation.h>
#include <pxr/base/gf/vec3d.h>
#include <pxr/usd/usd/stageCache.h>
#include <pxr/usd/usd/stage.h>

// OpenGL
#include <glad/glad.h>

//Project
#include "c_static.cpp"
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

pxr::GfVec3d calc_axis_normal(pxr::GfMatrix4d matrix, pxr::GfVec3d axis) {
    pxr::GfVec3d position = matrix.ExtractTranslation();
    pxr::GfVec3d axis_position = matrix.Transform(axis);
    pxr::GfVec3d normal = position - axis_position;
    normal = normal.GetNormalized();
    return normal;
}


pxr::GfMatrix4d c_create_projection_matrix(pybind11::dict draw_dict) {
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

void convert_matrix_usd_gl(const pxr::GfMatrix4d& usdMatrix, double glMatrix[16]) {
    glMatrix[0]  = usdMatrix[0][0];
    glMatrix[1]  = usdMatrix[0][1];
    glMatrix[2]  = usdMatrix[0][2];
    glMatrix[3]  = usdMatrix[0][3];
    glMatrix[4]  = usdMatrix[1][0];
    glMatrix[5]  = usdMatrix[1][1];
    glMatrix[6]  = usdMatrix[1][2];
    glMatrix[7]  = usdMatrix[1][3];
    glMatrix[8]  = usdMatrix[2][0];
    glMatrix[9]  = usdMatrix[2][1];
    glMatrix[10] = usdMatrix[2][2];
    glMatrix[11] = usdMatrix[2][3];
    glMatrix[12] = usdMatrix[3][0];
    glMatrix[13] = usdMatrix[3][1];
    glMatrix[14] = usdMatrix[3][2];
    glMatrix[15] = usdMatrix[3][3];
}

void convert_matrix_usd_f_gl(const pxr::GfMatrix4d& usdMatrix, float glMatrix[16]) {
    glMatrix[0]  = usdMatrix[0][0];
    glMatrix[1]  = usdMatrix[0][1];
    glMatrix[2]  = usdMatrix[0][2];
    glMatrix[3]  = usdMatrix[0][3];
    glMatrix[4]  = usdMatrix[1][0];
    glMatrix[5]  = usdMatrix[1][1];
    glMatrix[6]  = usdMatrix[1][2];
    glMatrix[7]  = usdMatrix[1][3];
    glMatrix[8]  = usdMatrix[2][0];
    glMatrix[9]  = usdMatrix[2][1];
    glMatrix[10] = usdMatrix[2][2];
    glMatrix[11] = usdMatrix[2][3];
    glMatrix[12] = usdMatrix[3][0];
    glMatrix[13] = usdMatrix[3][1];
    glMatrix[14] = usdMatrix[3][2];
    glMatrix[15] = usdMatrix[3][3];
}

void add_triangle(
        std::vector<vertex_data>& tri_vertices, 
        const std::vector<float>& face_color, 
        const pxr::GfVec3d& a, 
        const pxr::GfVec3d& b, 
        const pxr::GfVec3d& c
    ) {
    pxr::GfVec3d n = pxr::GfCross(b - a, b - c).GetNormalized();
    vertex_data vertex_1{{a[0], a[1], a[2]}, {n[0], n[1], n[2]}, {face_color[0], face_color[1], face_color[2], face_color[3]}};
    vertex_data vertex_2{{b[0], b[1], b[2]}, {n[0], n[1], n[2]}, {face_color[0], face_color[1], face_color[2], face_color[3]}};
    vertex_data vertex_3{{c[0], c[1], c[2]}, {n[0], n[1], n[2]}, {face_color[0], face_color[1], face_color[2], face_color[3]}};
    tri_vertices.push_back(vertex_1);
    tri_vertices.push_back(vertex_2);
    tri_vertices.push_back(vertex_3);
};   

pxr::GfMatrix4d calc_look_at_x(const pxr::GfVec3d source, const pxr::GfVec3d target, const pxr::GfVec3d up) {
    pxr::GfVec3d forward = (target - source).GetNormalized();
    pxr::GfVec3d right = pxr::GfCross(up, forward).GetNormalized();
    pxr::GfVec3d up_axis = pxr::GfCross(right, forward).GetNormalized();
    pxr::GfMatrix4d look_at_matrix(
        forward[0], forward[1], forward[2], 0.0,
        right[0], right[1], right[2], 0.0,
        up_axis[0], up_axis[1], up_axis[2], 0.0,
        source[0], source[1], source[2], 1.0
    );
    return look_at_matrix;
}

void c_init_opengl_settings() {
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);
    glEnable(GL_MULTISAMPLE);
}

void c_setup_opengl_viewport(pybind11::dict draw_dict) {
    int hydra_x_min = draw_dict["hydra_x_min"].cast<int>();
    int hydra_y_min = draw_dict["hydra_y_min"].cast<int>();
    int panel_width = draw_dict["panel_width"].cast<int>();
    int panel_height = draw_dict["panel_height"].cast<int>();
    double fov = draw_dict["fov"].cast<double>();
    double near_plane = draw_dict["near_z"].cast<double>();
    double far_plane = draw_dict["far_z"].cast<double>();
    pxr::GfMatrix4d camera_matrix = draw_dict["camera_matrix"].cast<pxr::GfMatrix4d>();

    glViewport(hydra_x_min, hydra_y_min, panel_width, panel_height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    double aspect_ratio = double(panel_width) / double(panel_height);
    double top = near_plane * tan(fov * M_PI / 360.0);
    double bottom = -top;
    double right = top * aspect_ratio;
    double left = -right;
    glFrustum(left, right, bottom, top, near_plane, far_plane);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    double camera_matrix_inverse_gl[16];
    convert_matrix_usd_gl(camera_matrix.GetInverse(), camera_matrix_inverse_gl);    
    glLoadMatrixd(camera_matrix_inverse_gl);
}

void c_create_pick_matrix(GLdouble x, GLdouble y, GLdouble delta_x, GLdouble delta_y, const GLint viewport[4]) {
    if (delta_x <= 0.0 || delta_y <= 0.0) return;
    glTranslated(
        (viewport[2] - 2.0 * (x - viewport[0])) / delta_x,
        (viewport[3] - 2.0 * (y - viewport[1])) / delta_y,
        0.0
    );
    glScaled(viewport[2] / delta_x, viewport[3] / delta_y, 1.0);
}

void c_create_pick_perspective(GLdouble fov, GLdouble aspect, GLdouble near_z, GLdouble far_z) {
    GLdouble height = tan(fov * M_PI / 360.0) * near_z;
    GLdouble width = height * aspect;
    glFrustum(-width, width, -height, height, near_z, far_z);
}

pybind11::object c_get_bone_by_id(pybind11::list bone_list, int bone_id) {
    if (bone_id <= 0 || bone_id > static_cast<int>(bone_list.size())) {
        return pybind11::none();
    }
    return bone_list[bone_id - 1];
}

void c_check_opengl_error() {
    GLenum err = glGetError();
    if (err != GL_NO_ERROR) {
        std::cerr << "OpenGL error: " << err << std::endl;
    }
}

// Init GLAD/OpenGL and related settings
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




