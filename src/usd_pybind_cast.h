///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Type Caster
// TODO:
// 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#pragma once
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
#include <pxr/usd/sdf/path.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usd/prim.h>

// OpenGL
#include <glad/glad.h>
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

namespace pybind11 { namespace detail {

// GfMatrix4d
template <> struct type_caster<pxr::GfMatrix4d> {
public:
    PYBIND11_TYPE_CASTER(pxr::GfMatrix4d, _("GfMatrix4d"));

    // Python -> C++
    bool load(handle src, bool) {
        namespace py = pybind11;
        if (py::isinstance<py::sequence>(src)) {
            py::sequence seq = py::reinterpret_borrow<py::sequence>(src);
            if (seq.size() == 4) {
                py::sequence row0 = py::reinterpret_borrow<py::sequence>(seq[0]);
                py::sequence row1 = py::reinterpret_borrow<py::sequence>(seq[1]);
                py::sequence row2 = py::reinterpret_borrow<py::sequence>(seq[2]);
                py::sequence row3 = py::reinterpret_borrow<py::sequence>(seq[3]);
                value[0][0] = py::float_(row0[0]);
                value[0][1] = py::float_(row0[1]);
                value[0][2] = py::float_(row0[2]);
                value[0][3] = py::float_(row0[3]);
                value[1][0] = py::float_(row1[0]);
                value[1][1] = py::float_(row1[1]);
                value[1][2] = py::float_(row1[2]);
                value[1][3] = py::float_(row1[3]);
                value[2][0] = py::float_(row2[0]);
                value[2][1] = py::float_(row2[1]);
                value[2][2] = py::float_(row2[2]);
                value[2][3] = py::float_(row2[3]);
                value[3][0] = py::float_(row3[0]);
                value[3][1] = py::float_(row3[1]);
                value[3][2] = py::float_(row3[2]);
                value[3][3] = py::float_(row3[3]);
                return true;
            }
        }
        return false;
    }
};

// GfVec3d
template <> struct type_caster<pxr::GfVec3d> {
public:
    PYBIND11_TYPE_CASTER(pxr::GfVec3d, _( "GfVec3d" ));

    // Python -> C++
    bool load(handle src, bool) {
        namespace py = pybind11;
        if (py::isinstance<py::sequence>(src)) {
            py::sequence seq = py::reinterpret_borrow<py::sequence>(src);
            if (seq.size() != 3) return false;
            value = pxr::GfVec3d(py::float_(seq[0]), py::float_(seq[1]), py::float_(seq[2]));
            return true;
        }
        return false;
    }
};


// GfVec2i
template <> struct type_caster<pxr::GfVec2i> {
public:
    PYBIND11_TYPE_CASTER(pxr::GfVec2i, _( "GfVec2i" ));

    // Python -> C++
    bool load(handle src, bool) {
        namespace py = pybind11;
        if (py::isinstance<py::sequence>(src)) {
            py::sequence seq = py::reinterpret_borrow<py::sequence>(src);
            if (seq.size() != 2) return false;
            value = pxr::GfVec2i(py::int_(seq[0]), py::int_(seq[1]));
            return true;
        }
        return false;
    }
};


}}