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

void convet_matrix_usd_gl(const pxr::GfMatrix4d& usdMatrix, GLfloat glMatrix[16]) {
    glMatrix[0]  = static_cast<GLfloat>(usdMatrix[0][0]);
    glMatrix[1]  = static_cast<GLfloat>(usdMatrix[0][1]);
    glMatrix[2]  = static_cast<GLfloat>(usdMatrix[0][2]);
    glMatrix[3]  = static_cast<GLfloat>(usdMatrix[0][3]);
    glMatrix[4]  = static_cast<GLfloat>(usdMatrix[1][0]);
    glMatrix[5]  = static_cast<GLfloat>(usdMatrix[1][1]);
    glMatrix[6]  = static_cast<GLfloat>(usdMatrix[1][2]);
    glMatrix[7]  = static_cast<GLfloat>(usdMatrix[1][3]);
    glMatrix[8]  = static_cast<GLfloat>(usdMatrix[2][0]);
    glMatrix[9]  = static_cast<GLfloat>(usdMatrix[2][1]);
    glMatrix[10] = static_cast<GLfloat>(usdMatrix[2][2]);
    glMatrix[11] = static_cast<GLfloat>(usdMatrix[2][3]);
    glMatrix[12] = static_cast<GLfloat>(usdMatrix[3][0]);
    glMatrix[13] = static_cast<GLfloat>(usdMatrix[3][1]);
    glMatrix[14] = static_cast<GLfloat>(usdMatrix[3][2]);
    glMatrix[15] = static_cast<GLfloat>(usdMatrix[3][3]);
}