/*
 * Script to draw a complex shape in 2D
 *
 * DARÍO PEÑA A01785420
 * 2025-14-11
 */

"use strict";

import * as twgl from "twgl-base.js";
import { M3 } from "./A01785420-2d-libs.js";
import GUI from "lil-gui";

// Define the shader code, using GLSL 3.00

const vsGLSL = `#version 300 es
in vec2 a_position;
in vec4 a_color;

uniform vec2 u_resolution;
uniform mat3 u_transforms;

out vec4 v_color;

void main() {
    // Multiply the matrix by the vector, adding 1 to the vector to make
    // it the correct size. Then keep only the two first components
    vec2 position = (u_transforms * vec3(a_position, 1)).xy;

    // Convert the position from pixels to 0.0 - 1.0
    vec2 zeroToOne = position / u_resolution;

    // Convert from 0->1 to 0->2
    vec2 zeroToTwo = zeroToOne * 2.0;

    // Convert from 0->2 to -1->1 (clip space)
    vec2 clipSpace = zeroToTwo - 1.0;

    // Invert Y axis
    gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);

    // Pass the vertex color to the fragment shader
    v_color = a_color;
}
`;

const fsGLSL = `#version 300 es
precision highp float;

in vec4 v_color;
out vec4 outColor;

void main() {
    outColor = v_color;
}
`;

const objects = {
  model: {
    transforms: {
      t: {
        x: 0,
        y: 0,
        z: 0,
      },
      rr: {
        x: 0,
        y: 0,
        z: 0,
      },
      s: {
        x: 1,
        y: 1,
        z: 1,
      },
    },
    color: [1, 0.5, 0.2, 1],
  },
  modelP: {
    transforms: {
      t: {
        x: 0,
        y: 0,
        z: 0,
      },
    },
  },
  // Guardar la posición del pivote para no depender de la cara ni viciversa
  fixedPivot: {
    x: 0,
    y: 0,
    isSet: false
  }
};

// Initialize the WebGL environmnet
function main() {
  const canvas = document.querySelector("canvas");
  const gl = canvas.getContext("webgl2");
  twgl.resizeCanvasToDisplaySize(gl.canvas);
  gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

  setupUI(gl);

  const programInfo = twgl.createProgramInfo(gl, [vsGLSL, fsGLSL]);

  const sides = 20;
  // Pivote y cara  centrado
  const centerX = gl.canvas.width / 2;
  const centerY = gl.canvas.height / 2;
  const radius = 100;

  const sidesP = 4;

  const centerXP = gl.canvas.width / 2;
  const centerYP = gl.canvas.height / 2;
  const radiusP = 10;

  
  objects.model.transforms.t.x = centerX;
  objects.model.transforms.t.y = centerY;
  objects.modelP.transforms.t.x = centerXP;
  objects.modelP.transforms.t.y = centerYP;

  // Create a polygon with the center at a specific location
  // CARA
  const arraysF = generateDataFace(radius, 0, 0, objects.model.color);
  const bufferInfoF = twgl.createBufferInfoFromArrays(gl, arraysF);
  const vaoF = twgl.createVAOFromBufferInfo(gl, programInfo, bufferInfoF);

  // Pivote
  const arraysP = generateData(sidesP, 0, 0, radiusP);
  const bufferInfoP = twgl.createBufferInfoFromArrays(gl, arraysP);
  const vaoP = twgl.createVAOFromBufferInfo(gl, programInfo, bufferInfoP);


  drawScene(gl, vaoF, programInfo, bufferInfoF, vaoP, bufferInfoP);
}


function drawScene(gl, vao, programInfo, bufferInfo, vaoP, bufferInfoP) {
 
  gl.clearColor(0, 0, 0, 0);
  gl.clear(gl.COLOR_BUFFER_BIT);

  // CARA
  let translate = [objects.model.transforms.t.x, objects.model.transforms.t.y];
  let angle_radians = objects.model.transforms.rr.z;
  let scale = [objects.model.transforms.s.x, objects.model.transforms.s.y];

  // PIVOTE
  let translateP = [
    objects.modelP.transforms.t.x,
    objects.modelP.transforms.t.y,
  ];

  
  const scaMat = M3.scale(scale);
  const rotMat = M3.rotation(angle_radians);
  const traMat = M3.translation(translate);
  
  const traMatP = M3.translation(translateP);

  // Si hay rotación pero no se ha fijado el pivote fjarlo
  if (angle_radians !== 0 && !objects.fixedPivot.isSet) {
    objects.fixedPivot.x = objects.modelP.transforms.t.x;
    objects.fixedPivot.y = objects.modelP.transforms.t.y;
    objects.fixedPivot.isSet = true;
  }
  
  
  if (angle_radians === 0) {
    objects.fixedPivot.isSet = false;
  }

  // Usar el pivote fijo para rotacin no el actul
  const pivotPos = objects.fixedPivot.isSet 
    ? [objects.fixedPivot.x, objects.fixedPivot.y]
    : [objects.modelP.transforms.t.x, objects.modelP.transforms.t.y];


  const faceX = translate[0];
  const faceY = translate[1];
  
  // Para rotar alrededor del pivote
  const toPivot = M3.translation([-pivotPos[0], -pivotPos[1]]);
  const backFromPivot = M3.translation([pivotPos[0], pivotPos[1]]);
  const toFace = M3.translation([faceX, faceY]);
  const fromFace = M3.translation([-faceX, -faceY]);
  
  let transforms = M3.identity();
  // Escalar
  transforms = M3.multiply(scaMat, transforms);
  // Mover a la posición de la cara
  transforms = M3.multiply(toFace, transforms);
  // Desde la posición de la cara,
  transforms = M3.multiply(toPivot, transforms);
  // Rotar alrededor del pivote
  transforms = M3.multiply(rotMat, transforms);
  // Regresar del pivote a donde estaba la cara
  transforms = M3.multiply(backFromPivot, transforms);

  let uniforms = {
    u_resolution: [gl.canvas.width, gl.canvas.height],
    u_transforms: transforms,
  };

  // Transformaciones del pivote
  let transformsP = M3.identity();
  transformsP = M3.multiply(traMatP, transformsP);

  let uniformsP = {
    u_resolution: [gl.canvas.width, gl.canvas.height],
    u_transforms: transformsP,
  };

  gl.useProgram(programInfo.program);

 
  twgl.setUniforms(programInfo, uniforms);
  gl.bindVertexArray(vao);
  twgl.drawBufferInfo(gl, bufferInfo);


  twgl.setUniforms(programInfo, uniformsP);
  gl.bindVertexArray(vaoP);
  twgl.drawBufferInfo(gl, bufferInfoP);

  requestAnimationFrame(() => drawScene(gl, vao, programInfo, bufferInfo, vaoP, bufferInfoP));
}

function setupUI(gl) {
  const gui = new GUI();

  const traFolder = gui.addFolder("Translation");
  traFolder.add(objects.model.transforms.t, "x", 0, gl.canvas.width);
  traFolder.add(objects.model.transforms.t, "y", 0, gl.canvas.height);

  const rotFolder = gui.addFolder("Rotation");
  rotFolder.add(objects.model.transforms.rr, "z", 0, Math.PI * 2);

  const scaFolder = gui.addFolder("Scale");
  scaFolder.add(objects.model.transforms.s, "x", -5, 5);
  scaFolder.add(objects.model.transforms.s, "y", -5, 5);

  gui.addColor(objects.model, "color");

  const traFolderP = gui.addFolder("Translation Pivot");
  traFolderP.add(objects.modelP.transforms.t, "x", 0, gl.canvas.width);
  traFolderP.add(objects.modelP.transforms.t, "y", 0, gl.canvas.height);
}

function generateData(sides, centerX, centerY, radius) {
    let arrays =
    {
        a_position: { numComponents: 2, data: [] },
        a_color:    { numComponents: 4, data: [] },
        indices:  { numComponents: 3, data: [] }
    };

    arrays.a_position.data.push(centerX);
    arrays.a_position.data.push(centerY);
    arrays.a_color.data.push(1);
    arrays.a_color.data.push(1);
    arrays.a_color.data.push(1);
    arrays.a_color.data.push(1);

    let angleStep = 2 * Math.PI / sides;
    for (let s=0; s<sides; s++) {
        let angle = angleStep * s;
        let x = centerX + Math.cos(angle) * radius;
        let y = centerY + Math.sin(angle) * radius;
        arrays.a_position.data.push(x);
        arrays.a_position.data.push(y);
        arrays.a_color.data.push(Math.random());
        arrays.a_color.data.push(Math.random());
        arrays.a_color.data.push(Math.random());
        arrays.a_color.data.push(1);
        arrays.indices.data.push(0);
        arrays.indices.data.push(s + 1);
        arrays.indices.data.push(((s + 2) <= sides) ? (s + 2) : 1);
    }

    return arrays;
}

function generateDataFace(r, centerX = 0, centerY = 0, color = [1, 0.5, 0.2, 1]) {

  const sides = 20;
  const arrays = generateData(sides, centerX, centerY, r);

  const numVerts = arrays.a_position.data.length / 2;
  arrays.a_color.data = [];
  for (let i = 0; i < numVerts; i++) {
    arrays.a_color.data.push(...color);
  }

  const addTriangle = (x1, y1, x2, y2, x3, y3, color = [0, 0, 0, 1]) => {
    arrays.a_position.data.push(x1, y1, x2, y2, x3, y3);
    arrays.a_color.data.push(...color, ...color, ...color);
    const base = arrays.a_position.data.length / 2 - 3;
    arrays.indices.data.push(base, base + 1, base + 2);
  };

  const addCircle = (x, y, radius, color = [0, 0, 0, 1], segments = 8) => {
    const centerIdx = arrays.a_position.data.length / 2;
    arrays.a_position.data.push(x, y);
    arrays.a_color.data.push(...color);
    
    const angleStep = (2 * Math.PI) / segments;
    for (let i = 0; i <= segments; i++) {
      const angle = angleStep * i;
      const px = x + Math.cos(angle) * radius;
      const py = y + Math.sin(angle) * radius;
      arrays.a_position.data.push(px, py);
      arrays.a_color.data.push(...color);
      
      if (i > 0) {
        arrays.indices.data.push(centerIdx, centerIdx + i, centerIdx + i + 1);
      }
    }
  };

  // caracteristiacs de la cara
  const eyeOffsetX = r / 3.5;
  const eyeOffsetY = r / 5;
  const eyeSize = r / 6;
  const pupilSize = r / 12;
  
  const leftX = centerX - eyeOffsetX;
  const leftY = centerY - eyeOffsetY;
  const rightX = centerX + eyeOffsetX;
  const rightY = centerY - eyeOffsetY;

  addCircle(leftX, leftY, eyeSize, [1, 1, 1, 1]);
  addCircle(rightX, rightY, eyeSize, [1, 1, 1, 1]);
  
 
  addCircle(leftX, leftY, pupilSize, [0, 0, 0, 1]);
  addCircle(rightX, rightY, pupilSize, [0, 0, 0, 1]);

  
  const mouthY = centerY + r * 0.25;
  const mouthWidth = r * 0.7;
  const mouthDepth = r * 0.15;
  const mouthSegments = 10;
  
  for (let i = 0; i < mouthSegments; i++) {
    const t1 = i / mouthSegments;
    const t2 = (i + 1) / mouthSegments;
    

    const x1 = centerX - mouthWidth / 2 + t1 * mouthWidth;
    const y1 = mouthY + Math.pow(2 * t1 - 1, 2) * mouthDepth;
    
    const x2 = centerX - mouthWidth / 2 + t2 * mouthWidth;
    const y2 = mouthY + Math.pow(2 * t2 - 1, 2) * mouthDepth;
    
    const thickness = r * 0.08;
    addTriangle(x1, y1, x2, y2, x2, y2 + thickness, [0, 0, 0, 1]);
    addTriangle(x1, y1, x2, y2 + thickness, x1, y1 + thickness, [0, 0, 0, 1]);
  }


  const cheekOffsetX = r * 0.55;
  const cheekY = centerY + r * 0.1;
  const cheekSize = r * 0.15;
  addCircle(centerX - cheekOffsetX, cheekY, cheekSize, [1, 0.6, 0.7, 0.6]);
  addCircle(centerX + cheekOffsetX, cheekY, cheekSize, [1, 0.6, 0.7, 0.6]);

  return arrays;
}


main();