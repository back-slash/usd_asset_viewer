#version 450 core

#define MAX_LIGHTS 8
uniform int light_count;
uniform vec3 light_direction[MAX_LIGHTS];
uniform vec3 light_color[MAX_LIGHTS];

in vec3 vert_normal;
in vec4 vert_color;
out vec4 frag_color;

void main() {
    vec3 normal = normalize(vert_normal);
    vec3 color = vec3(0.1) * vert_color.rgb;
    for (int i = 0; i < light_count; ++i) {
        float diff = max(dot(normal, -normalize(light_direction[i])), 0.0);
        color += diff * light_color[i];
    }
    color *= vert_color.rgb;

    frag_color = vec4(color, vert_color.a);
}


