#version 450 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec4 color;

uniform mat4 mvp;

out vec3 vert_normal;
out vec4 vert_color;

void main() {
    gl_Position = mvp * vec4(position, 1.0);
    vert_normal = normal;
    vert_color = color;
}