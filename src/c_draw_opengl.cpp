// C++
#include <iostream>
#include <vector>

// OpenUSD
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pxr/base/gf/matrix4d.h>
#include <pxr/base/gf/rotation.h>
#include <pxr/base/gf/vec3d.h>

// OpenGL
#include <glad/glad.h>


void ConvertMatrixUSDGL(const pxr::GfMatrix4d& usdMatrix, GLfloat glMatrix[16]) {
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


void ConvertMatrixListUSD(const pybind11::list& glMatrix, pxr::GfMatrix4d& usdMatrix) {
    usdMatrix[0][0] = glMatrix[0].cast<double>();
    usdMatrix[0][1] = glMatrix[1].cast<double>();
    usdMatrix[0][2] = glMatrix[2].cast<double>();
    usdMatrix[0][3] = glMatrix[3].cast<double>();

    usdMatrix[1][0] = glMatrix[4].cast<double>();
    usdMatrix[1][1] = glMatrix[5].cast<double>();
    usdMatrix[1][2] = glMatrix[6].cast<double>();
    usdMatrix[1][3] = glMatrix[7].cast<double>();

    usdMatrix[2][0] = glMatrix[8].cast<double>();
    usdMatrix[2][1] = glMatrix[9].cast<double>();
    usdMatrix[2][2] = glMatrix[10].cast<double>();
    usdMatrix[2][3] = glMatrix[11].cast<double>();

    usdMatrix[3][0] = glMatrix[12].cast<double>();
    usdMatrix[3][1] = glMatrix[13].cast<double>();
    usdMatrix[3][2] = glMatrix[14].cast<double>();
    usdMatrix[3][3] = glMatrix[15].cast<double>();
}    

void c_setup_opengl_viewport(
    int hydra_x_min,
    int hydra_y_min,
    int panel_width,
    int panel_height,
    double fov, 
    double near_plane, 
    double far_plane, 
    pxr::GfMatrix4d& up_axis_matrix,
    pxr::GfMatrix4d& camera_transform
) {
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
    pxr::GfMatrix4d camera_transform_offset = camera_transform.GetInverse();
    float camera_transform_offset_gl[16];
    ConvertMatrixUSDGL(camera_transform_offset, camera_transform_offset_gl);    
    glLoadMatrixf(camera_transform_offset_gl);
}


void c_draw_opengl_bones(
    pybind11::list bone_list,
    pybind11::list up_axis_matrix,
    pybind11::list camera_transform,
    int hydra_x_min, 
    int hydra_y_min, 
    int panel_width, 
    int panel_height,
    double fov, 
    double near_plane, 
    double far_plane
) {
    pxr::GfMatrix4d up_axis_matrix_gf;
    pxr::GfMatrix4d camera_transform_gf;
    
    glPushMatrix();

    ConvertMatrixListUSD(
        up_axis_matrix,
        up_axis_matrix_gf
    );
    ConvertMatrixListUSD(
        camera_transform,
        camera_transform_gf
    );

    c_setup_opengl_viewport(
        hydra_x_min, 
        hydra_y_min, 
        panel_width, 
        panel_height,
        fov, 
        near_plane, 
        far_plane,
        up_axis_matrix_gf,
        camera_transform_gf
    );

    for (auto bone : bone_list) {
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pybind11::list py_transform_list = data_dict["transform"];
        pxr::GfMatrix4d py_transform;
        py_transform.SetIdentity();  
        
        ConvertMatrixListUSD(
            py_transform_list,
            py_transform
        );

        pxr::GfMatrix4d bone_transform = py_transform;
        pxr::GfVec3d root_vert = bone_transform.ExtractTranslation();

        glLineWidth(1.0f);
        glBegin(GL_LINES);
        glColor3f(1.0f, 0.0f, 0.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d x_axis = bone_transform.Transform(pxr::GfVec3d(2.5, 0.0, 0.0));
        glVertex3d(x_axis[0], x_axis[1], x_axis[2]);
        glColor3f(0.0f, 1.0f, 0.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d y_axis = bone_transform.Transform(pxr::GfVec3d(0.0, 2.5, 0.0));
        glVertex3d(y_axis[0], y_axis[1], y_axis[2]);
        glColor3f(0.0f, 0.0f, 1.0f);
        glVertex3d(root_vert[0], root_vert[1], root_vert[2]);
        pxr::GfVec3d z_axis = bone_transform.Transform(pxr::GfVec3d(0.0, 0.0, 2.5));
        glVertex3d(z_axis[0], z_axis[1], z_axis[2]);
        glEnd();

        for (auto child : bone.attr("get_child_nodes")()) {
            pybind11::dict child_data_dict = child.attr("get_data_object")();
            pybind11::list child_transform_list = child_data_dict["transform"];
            pxr::GfMatrix4d child_transform;
            ConvertMatrixListUSD(
                child_transform_list,
                child_transform
            );
            pxr::GfVec3d child_root_vert = child_transform.ExtractTranslation();

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

float g_rotationAngle = 0.0f;

void c_init_glad() {
    if (!gladLoadGL()) {
        std::cerr << "Failed to initialize GLAD" << std::endl;
        return;
    }
}


PYBIND11_MODULE(c_draw_opengl, m) {
    m.def("c_draw_opengl_bones", &c_draw_opengl_bones, "Draw OpenGL bones",
          pybind11::arg("bone_list"),
          pybind11::arg("up_axis_matrix"),
          pybind11::arg("camera_transform"),
          pybind11::arg("hydra_x_min"),
          pybind11::arg("hydra_y_min"),
          pybind11::arg("panel_width"),
          pybind11::arg("panel_height"),
          pybind11::arg("fov"),
          pybind11::arg("near_plane"),
          pybind11::arg("far_plane"));
    m.def("c_init_glad", &c_init_glad, "Initialize GLAD");
}

