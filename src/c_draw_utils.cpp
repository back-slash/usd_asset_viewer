///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Draw Utilities
// TODO:
// 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
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

// OpenGL
#include <glad/glad.h>
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

void c_draw_text(pybind11::dict draw_dict) {

    std::string text = draw_dict["text"].cast<std::string>();
    double x = draw_dict["x"].cast<double>();
    double y = draw_dict["y"].cast<double>();
    double z = draw_dict["z"].cast<double>();

    glColor3f(1.0f, 1.0f, 1.0f);

    glRasterPos3d(x, y, z);

    for (char c : text) {
        //glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, c);
    }
}

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

void  c_init_opengl_settings() {
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

void c_check_opengl_error() {
    GLenum err = glGetError();
    if (err != GL_NO_ERROR) {
        std::cerr << "OpenGL error: " << err << std::endl;
    }
}

void check_gl_error(const char* msg) {
    GLenum err = glGetError();
    if (err != GL_NO_ERROR) {
        std::cerr << "OpenGL error (" << msg << "): " << err << std::endl;
    }
}