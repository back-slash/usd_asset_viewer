///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Utilities
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

// USD
#include <pxr/usd/usd/primRange.h>

// OpenGL
#include <glad/glad.h>

#undef min
#undef max

// Project
#include "c_draw.cpp"
#include "c_utils.cpp"


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


PYBIND11_MODULE(c_base, m) {
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
      pybind11::class_<HydraRenderer>(m, "HydraRenderer")
            .def(pybind11::init<pybind11::str>(), pybind11::arg("stage_path"))
            .def("c_set_hydra_camera_path", &HydraRenderer::c_set_hydra_camera_path, 
                 pybind11::arg("path"))
            .def("c_hydra_render_loop", &HydraRenderer::c_hydra_render_loop,
                 pybind11::arg("render_dict"),
                 pybind11::arg("user_show_cfg"))
            .def("c_get_usd_stage", &HydraRenderer::c_get_usd_stage);
      pybind11::class_<pxr::UsdStageRefPtr>(m, "UsdStageRefPtr")
            .def("GetPsuedoRoot", [](const pxr::UsdStageRefPtr& self) {
                return self->GetPseudoRoot();
            })
            .def("Traverse", [](const pxr::UsdStageRefPtr& self) {
                return self->Traverse();
            });
}
