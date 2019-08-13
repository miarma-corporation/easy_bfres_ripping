﻿#version 330
 
const int MY_ARRAY_SIZE = 200;

in vec3 vPosition;
in vec3 vNormal;
in vec3 vColor;

out vec3 normal;
out vec3 color;

uniform mat4 modelview;

void main()
{


    normal = vNormal;
    color = vColor;

    gl_Position = modelview * vec4(vPosition.xyz, 1.0);

    vec3 distance = (vPosition.xyz + vec3(5, 5, 5))/2;

}