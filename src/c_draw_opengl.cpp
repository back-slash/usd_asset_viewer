///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// USD Asset Viewer | SRC | C++ Draw OpenGL
// TODO:
// 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

// OpenGL
#include <glad/glad.h>

// Project
#include "c_draw_utils.cpp"
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


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
    float camera_matrix_inverse_gl[16];
    convet_matrix_usd_gl(camera_matrix.GetInverse(), camera_matrix_inverse_gl);    
    glLoadMatrixf(camera_matrix_inverse_gl);
}

void c_draw_opengl_bones(pybind11::list bone_list, pybind11::dict draw_dict) {
    glPushMatrix();

    c_setup_opengl_viewport(
        draw_dict
    );

    for (auto bone : bone_list) {
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pxr::GfMatrix4d bone_matrix = data_dict["matrix"].cast<pxr::GfMatrix4d>();
        pxr::GfVec3d root_vert = bone_matrix.ExtractTranslation();

        glLineWidth(1.0f);
        glBegin(GL_LINES);
        glColor3f(1.0f, 0.0f, 0.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d x_axis = bone_matrix.Transform(pxr::GfVec3d(2.5, 0.0, 0.0));
        glVertex3d(x_axis[0], x_axis[1], x_axis[2]);
        glColor3f(0.0f, 1.0f, 0.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d y_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 2.5, 0.0));
        glVertex3d(y_axis[0], y_axis[1], y_axis[2]);
        glColor3f(0.0f, 0.0f, 1.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d z_axis = bone_matrix.Transform(pxr::GfVec3d(0.0, 0.0, 2.5));
        glVertex3d(z_axis[0], z_axis[1], z_axis[2]);
        glEnd();

        for (auto child : bone.attr("get_child_nodes")()) {
            pybind11::dict child_data_dict = child.attr("get_data_object")();
            pxr::GfMatrix4d child_matrix = child_data_dict["matrix"].cast<pxr::GfMatrix4d>();
            pxr::GfVec3d child_root_vert = child_matrix.ExtractTranslation();
            
            double bone_length = (child_root_vert - root_vert).GetLength();
            if (bone_length < 0.001) {
                continue;
            }
            pxr::GfVec3d bone_direction = (child_root_vert - root_vert).GetNormalized();
            double bone_radius = 5.0;
            glLineWidth(2.0f);
            glBegin(GL_LINES);
            glColor3f(0.75f, 0.75f, 0.75f);
            glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
            glVertex3d(child_root_vert[0], child_root_vert[1], child_root_vert[2]);
            glEnd();
        }
    
    }

    glPopMatrix();

    GLenum err = glGetError();
    if (err != GL_NO_ERROR) {
        std::cerr << "OpenGL error: " << err << std::endl;
    }
}

void  c_draw_opengl_grid(pybind11::dict draw_dict) {
    glPushAttrib(GL_ENABLE_BIT | GL_TRANSFORM_BIT | GL_VIEWPORT_BIT);
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
    glPopAttrib();
}

void c_init_glad() {
    if (!gladLoadGL()) {
        std::cerr << "Failed to initialize GLAD" << std::endl;
        return;
    }
    else {
        c_init_opengl_settings();
    }
}


PYBIND11_MODULE(c_draw_opengl, m) {
    m.def("c_init_glad", &c_init_glad, "Initialize GLAD");  
    m.def("c_init_opengl_settings", &c_init_opengl_settings, "Initialize OpenGL Settings");
    m.def("c_draw_opengl_bones", &c_draw_opengl_bones, "Draw OpenGL Bones",
          pybind11::arg("bone_list"),
          pybind11::arg("draw_dict"));
    m.def("c_draw_opengl_grid", &c_draw_opengl_grid, "Draw OpenGL Grid",
          pybind11::arg("draw_dict"));

}

