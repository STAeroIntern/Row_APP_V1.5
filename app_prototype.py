import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from sql_tool.queries import get_all_reports
from ui.upload import show_new_report


st.set_page_config(
    page_title="RoW Inspection Report",
    layout="wide",
)


# ============================================================
# Hide Streamlit Deploy button
# ============================================================

st.markdown("""
<style>
[data-testid="stAppDeployButton"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 3D Drone Viewer
# ============================================================

st.title("3D Drone Viewer")

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">

    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        #viewer {
            width: 100%;
            height: 600px;
            background: #f2f2f2;
        }

        canvas {
            display: block;
        }
    </style>
</head>

<body>

<div id="viewer"></div>

<script type="importmap">
{
    "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js"
    }
}
</script>

<script type="module">

import * as THREE from 'three';

import { OrbitControls }
    from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

import { OBJLoader }
    from 'https://unpkg.com/three@0.160.0/examples/jsm/loaders/OBJLoader.js';


const container = document.getElementById("viewer");


// ============================================================
// Scene
// ============================================================

const scene = new THREE.Scene();

scene.background = new THREE.Color(0xf2f2f2);


// ============================================================
// Camera
// ============================================================

const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    100000
);

camera.position.set(5, 5, 5);


// ============================================================
// Renderer
// ============================================================

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setPixelRatio(window.devicePixelRatio);

renderer.setSize(
    container.clientWidth,
    container.clientHeight
);

renderer.shadowMap.enabled = true;

container.appendChild(renderer.domElement);


// ============================================================
// Lighting
// ============================================================

const ambientLight = new THREE.AmbientLight(
    0xffffff,
    2.0
);

scene.add(ambientLight);


const directionalLight = new THREE.DirectionalLight(
    0xffffff,
    3.0
);

directionalLight.position.set(
    10,
    20,
    10
);

directionalLight.castShadow = true;

scene.add(directionalLight);


const fillLight = new THREE.DirectionalLight(
    0xffffff,
    1.5
);

fillLight.position.set(
    -10,
    5,
    -10
);

scene.add(fillLight);


// ============================================================
// Controls
// ============================================================

const controls = new OrbitControls(
    camera,
    renderer.domElement
);

controls.enableDamping = true;

controls.dampingFactor = 0.05;

controls.enablePan = true;

controls.minDistance = 0.1;

controls.maxDistance = 100000;


// ============================================================
// Load OBJ
// ============================================================

const loader = new OBJLoader();

loader.load(
    "models/drone_costum.obj",

    function(object) {

        console.log("Drone OBJ loaded");

        // Apply a default material because OBJ may not
        // have its MTL/material information available.

        object.traverse(function(child) {

            if (child.isMesh) {

                child.material = new THREE.MeshStandardMaterial({
                    color: 0x888888,
                    roughness: 0.55,
                    metalness: 0.25
                });

                child.castShadow = true;
                child.receiveShadow = true;
            }

        });


        scene.add(object);


        // ====================================================
        // Automatically center and scale the drone
        // ====================================================

        const box = new THREE.Box3().setFromObject(object);

        const center = box.getCenter(new THREE.Vector3());

        const size = box.getSize(new THREE.Vector3());


        object.position.sub(center);


        const maxDimension = Math.max(
            size.x,
            size.y,
            size.z
        );


        // Normalize model size
        const targetSize = 5;

        const scale = targetSize / maxDimension;

        object.scale.setScalar(scale);


        // ====================================================
        // Position camera automatically
        // ====================================================

        const distance = targetSize * 2.2;

        camera.position.set(
            distance,
            distance * 0.7,
            distance
        );

        camera.lookAt(0, 0, 0);

        controls.target.set(0, 0, 0);

        controls.update();
    },


    function(xhr) {

        if (xhr.total > 0) {

            console.log(
                "Loading: " +
                Math.round((xhr.loaded / xhr.total) * 100) +
                "%"
            );

        }

    },


    function(error) {

        console.error(
            "Error loading drone OBJ:",
            error
        );

        container.innerHTML = `
            <div style="
                display:flex;
                align-items:center;
                justify-content:center;
                height:100%;
                font-family:Arial;
                color:#cc0000;
            ">
                Failed to load drone model.
            </div>
        `;
    }
);


// ============================================================
// Resize
// ============================================================

window.addEventListener(
    "resize",
    function() {

        camera.aspect =
            container.clientWidth /
            container.clientHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            container.clientWidth,
            container.clientHeight
        );

    }
);


// ============================================================
// Animation
// ============================================================

function animate() {

    requestAnimationFrame(animate);

    controls.update();

    renderer.render(
        scene,
        camera
    );
}

animate();

</script>

</body>
</html>
"""

components.html(
    html,
    height=620,
)


# ============================================================
# Row Inspection Report
# ============================================================

st.title("Row Inspection Report")


# ============================================================
# Database
# ============================================================

db_report = get_all_reports()

df = pd.DataFrame(db_report)


# ============================================================
# Session State
# ============================================================

if "popover_open" not in st.session_state:
    st.session_state.popover_open = False

if "confirm_cancel" not in st.session_state:
    st.session_state.confirm_cancel = False


# ============================================================
# UAV IDs
# ============================================================

if not df.empty and "uav_id" in df.columns:

    uav_ids = sorted(
        df["uav_id"]
        .dropna()
        .unique()
        .tolist()
    )

else:

    uav_ids = []


# ============================================================
# New Report
# ============================================================

show_new_report()