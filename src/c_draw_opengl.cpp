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
    pybind11::dict draw_dict
) {
    int hydra_x_min = draw_dict["hydra_x_min"].cast<int>();
    int hydra_y_min = draw_dict["hydra_y_min"].cast<int>();
    int panel_width = draw_dict["panel_width"].cast<int>();
    int panel_height = draw_dict["panel_height"].cast<int>();
    double fov = draw_dict["fov"].cast<double>();
    double near_plane = draw_dict["near_z"].cast<double>();
    double far_plane = draw_dict["far_z"].cast<double>();
    pxr::GfMatrix4d camera_matrix;
    ConvertMatrixListUSD(draw_dict["camera_matrix"].cast<pybind11::list>(), camera_matrix);

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
    ConvertMatrixUSDGL(camera_matrix.GetInverse(), camera_matrix_inverse_gl);    
    glLoadMatrixf(camera_matrix_inverse_gl);
}


void c_draw_opengl_bones(
    pybind11::list bone_list,
    pybind11::dict draw_dict
) {
    pxr::GfMatrix4d camera_matrix;
        ConvertMatrixListUSD(
        draw_dict["camera_matrix"],
        camera_matrix
    );

    glPushMatrix();

    c_setup_opengl_viewport(
        draw_dict
    );

    for (auto bone : bone_list) {
        pybind11::dict data_dict = bone.attr("get_data_object")();
        pybind11::list bone_matrix_list = data_dict["matrix"];
        pxr::GfMatrix4d bone_matrix;
        bone_matrix.SetIdentity();  
        
        ConvertMatrixListUSD(
            bone_matrix_list,
            bone_matrix
        );

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
            pybind11::list child_matrix_list = child_data_dict["matrix"];
            pxr::GfMatrix4d child_matrix;
            ConvertMatrixListUSD(
                child_matrix_list,
                child_matrix
            );
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
          pybind11::arg("draw_dict"));
    m.def("c_init_glad", &c_init_glad, "Initialize GLAD");
}

