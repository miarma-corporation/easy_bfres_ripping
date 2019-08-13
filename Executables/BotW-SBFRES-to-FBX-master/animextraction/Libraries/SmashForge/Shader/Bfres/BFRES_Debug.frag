﻿#version 330

in vec2 f_texcoord0;
in vec2 f_texcoord1;
in vec2 f_texcoord2;
in vec2 f_texcoord3;
in vec3 normal;
in vec3 viewNormal;
in vec4 vertexColor;
in vec3 tangent;
in vec3 bitangent;

in vec3 objectPosition;

in vec3 boneWeightsColored;

// Viewport Camera/Lighting
uniform mat4 mvpMatrix;
uniform vec3 specLightDirection;
uniform vec3 difLightDirection;

uniform int enableCellShading;

const float levels = 3.0;

// Viewport Settings
uniform int uvChannel;
uniform int renderType;
uniform int useNormalMap;
uniform vec4 colorSamplerUV;
uniform int renderVertColor;
uniform vec3 difLightColor;
uniform vec3 ambLightColor;
uniform int colorOverride;

// Channel Toggles
uniform int renderR;
uniform int renderG;
uniform int renderB;
uniform int renderAlpha;

//------------------------------------------------------------------------------------
//
//      Texture Samplers
//
//------------------------------------------------------------------------------------

uniform sampler2D tex0;
uniform sampler2D BakeShadowMap;
uniform sampler2D spl;
uniform sampler2D normalMap;
uniform sampler2D BakeLightMap;
uniform sampler2D UVTestPattern;
uniform sampler2D TransparencyMap;
uniform sampler2D EmissionMap;
uniform sampler2D SpecularMap;
uniform sampler2D DiffuseLayer;

//------------------------------------------------------------------------------------
//
//      Shader Params
//
//------------------------------------------------------------------------------------

uniform float normal_map_weight;
uniform float ao_density;
uniform float emission_intensity;
uniform vec4 fresnelParams;
uniform vec4 base_color_mul_color;
uniform vec3 emission_color;


//------------------------------------------------------------------------------------
//
//      Shader Options
//
//------------------------------------------------------------------------------------

uniform float uking_texture2_texcoord;
uniform float bake_shadow_type;
uniform float enable_fresnel;
uniform float enable_emission;


//------------------------------------------------------------------------------------
//
//      Texture Map Toggles
//
//------------------------------------------------------------------------------------

uniform int HasNormalMap;
uniform int HasSpecularMap;
uniform int HasShadowMap;
uniform int HasAmbientOcclusionMap;
uniform int HasLightMap;
uniform int HasTransparencyMap;
uniform int HasEmissionMap;
uniform int HasDiffuseLayer;
uniform int isTransparent;

vec3 bumpMapNormal(vec3 normal);

struct VertexAttributes {
    vec3 objectPosition;
    vec2 texCoord;
    vec2 texCoord2;
    vec2 texCoord3;
    vec4 vertexColor;
    vec3 normal;
    vec3 viewNormal;
    vec3 tangent;
    vec3 bitangent;
};

out vec4 fragColor;

#define gamma 2.2

// Defined in Utility.frag.
float Luminance(vec3 rgb);

// Defined in BFRES_Utility.frag.
vec3 CalcBumpedNormal(vec3 normal, sampler2D normalMap, VertexAttributes vert, float texCoordIndex);
float AmbientOcclusionBlend(sampler2D BakeShadowMap, VertexAttributes vert, float ao_density);
vec3 EmissionPass(sampler2D EmissionMap, float emission_intensity, VertexAttributes vert, float texCoordIndex, vec3 emission_color);

vec2 displayTexCoord =  f_texcoord0;

void main()
{
    fragColor = vec4(vec3(0), 1);

    // Create a struct for passing all the vertex attributes to other functions.
    VertexAttributes vert;
    vert.objectPosition = objectPosition;
    vert.texCoord = f_texcoord0;
    vert.texCoord2 = f_texcoord1;
    vert.texCoord3 = f_texcoord2;
    vert.vertexColor = vertexColor;
    vert.normal = normal;
    vert.viewNormal = viewNormal;
    vert.tangent = tangent;
    vert.bitangent = bitangent;

    vec3 N = normal;
	if (HasNormalMap == 1 && useNormalMap == 1)
		N = CalcBumpedNormal(normal, normalMap, vert, uking_texture2_texcoord);

    if (renderType == 1) // normals vertexColor
    {
        vec3 displayNormal = (N * 0.5) + 0.5;
        fragColor = vec4(displayNormal,1);
    }
    else if (renderType == 2) // Lighting
    {
        float halfLambert = dot(difLightDirection, N) * 0.5 + 0.5;
        fragColor = vec4(vec3(halfLambert), 1);
    }
	else if (renderType == 4) //Display Normal
	{
		if (uking_texture2_texcoord == 1)
            fragColor.rgb = texture(normalMap, f_texcoord1).rgb;
		else
            fragColor.rgb = texture(normalMap, displayTexCoord).rgb;
	}
	else if (renderType == 3) //DiffuseColor
	    fragColor = vec4(texture(tex0, displayTexCoord).rgb, 1);
    else if (renderType == 5) // vertexColor
        fragColor = vertexColor;
	else if (renderType == 6) //Display Ambient Occlusion
	{
	    if (HasShadowMap == 1)
        {
            float ambientOcclusionBlend = AmbientOcclusionBlend(BakeShadowMap, vert, ao_density);
            fragColor = vec4(vec3(ambientOcclusionBlend), 1);
        }
		else
        {
            fragColor = vec4(1);
        }
	}
    else if (renderType == 7) // uv coords
        fragColor = vec4(displayTexCoord.x, displayTexCoord.y, 1, 1);
    else if (renderType == 8) // uv test pattern
	{
        fragColor = vec4(texture(UVTestPattern, displayTexCoord).rgb, 1);
	}
    else if (renderType == 9) //Display tangents
    {
        vec3 displayTangent = (tangent * 0.5) + 0.5;
        if (dot(tangent, vec3(1)) == 0)
            displayTangent = vec3(0);

        fragColor = vec4(displayTangent,1);
    }
    else if (renderType == 10) //Display bitangents
    {
        vec3 displayBitangent = (bitangent * 0.5) + 0.5;
        if (dot(bitangent, vec3(1)) == 0)
            displayBitangent = vec3(0);

        fragColor = vec4(displayBitangent,1);
    }
    else if (renderType == 11) //Display lights from second bake map if exists
	{
	    fragColor.rgb = texture2D(BakeLightMap, vert.texCoord2).rgb;

        if (HasEmissionMap == 1 || enable_emission == 1)
	        fragColor.rgb += EmissionPass(EmissionMap, emission_intensity, vert, uking_texture2_texcoord, emission_color);; 
	}

    // Toggles rendering of individual color channels for all render modes.
    fragColor.rgb *= vec3(renderR, renderG, renderB);
    if (renderR == 1 && renderG == 0 && renderB == 0)
        fragColor.rgb = fragColor.rrr;
    else if (renderG == 1 && renderR == 0 && renderB == 0)
        fragColor.rgb = fragColor.ggg;
    else if (renderB == 1 && renderR == 0 && renderG == 0)
        fragColor.rgb = fragColor.bbb;

    if (renderType == 12)
        fragColor.rgb = boneWeightsColored;
}
