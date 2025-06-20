///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Draw Statics
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
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct vertex_data {
    double position[3];
    double normal[3];
    float color[4];
};

struct light_data {
    std::vector<float> color;
    float intensity;
    pxr::GfMatrix4d matrix;
    light_data(std::vector<float>& input_color, float& input_intensity, pxr::GfMatrix4d& input_matrix) : 
        color({input_color[0], input_color[1], input_color[2], input_color[3]}), intensity(input_intensity), matrix(input_matrix) {}
};

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
