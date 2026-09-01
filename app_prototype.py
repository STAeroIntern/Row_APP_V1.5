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

import streamlit as st
import streamlit.components.v1 as components
import base64


st.title("3D Drone Viewer")

OBJ_PATH = "/app/models/drone_costum.obj"

# Read OBJ
with open(OBJ_PATH, "rb") as f:
    obj_base64 = base64.b64encode(f.read()).decode("utf-8")


html = f"""
<!DOCTYPE html>
<html>

<head>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/OBJLoader.js"></script>

<style>

html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}}

#viewer {{
    width: 100%;
    height: 600px;
    background: #eeeeee;
}}

#error {{
    position: absolute;
    top: 20px;
    left: 20px;
    color: red;
    font-family: Arial;
    font-size: 16px;
}}

</style>

</head>

<body>

<div id="viewer"></div>
<div id="error"></div>


<script>

console.log("Starting drone viewer...");


// ============================================================
// Scene
// ============================================================

const container = document.getElementById("viewer");

const scene = new THREE.Scene();

scene.background = null;


// ============================================================
// Camera
// ============================================================

const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.01,
    100000
);

camera.position.set(5, 5, 5);


// ============================================================
// Renderer
// ============================================================

const renderer = new THREE.WebGLRenderer({{
    antialias: true
}});

renderer.setPixelRatio(window.devicePixelRatio);

renderer.setSize(
    container.clientWidth,
    container.clientHeight
);

container.appendChild(renderer.domElement);


// ============================================================
// Lights
// ============================================================

const ambient = new THREE.AmbientLight(
    0xffffff,
    2
);

scene.add(ambient);


const light1 = new THREE.DirectionalLight(
    0xffffff,
    3
);

light1.position.set(
    10,
    20,
    10
);

scene.add(light1);


const light2 = new THREE.DirectionalLight(
    0xffffff,
    2
);

light2.position.set(
    -10,
    5,
    -10
);

scene.add(light2);


// ============================================================
// Controls
// ============================================================

const controls = new THREE.OrbitControls(
    camera,
    renderer.domElement
);

controls.enableDamping = true;

controls.dampingFactor = 0.05;


// ============================================================
// OBJ DATA
// ============================================================

const objBase64 = "{obj_base64}";


function base64ToString(base64) {{

    const binary = atob(base64);

    let bytes = new Uint8Array(
        binary.length
    );

    for (let i = 0; i < binary.length; i++) {{
        bytes[i] = binary.charCodeAt(i);
    }}

    return new TextDecoder().decode(bytes);
}}


// ============================================================
// Load OBJ
// ============================================================

try {{

    console.log("Converting OBJ data...");

    const objText = base64ToString(objBase64);

    console.log(
        "OBJ size:",
        objText.length
    );


    const loader = new THREE.OBJLoader();

    console.log("Parsing OBJ...");

    const drone = loader.parse(objText);

    console.log(
        "Drone loaded:",
        drone
    );


    // ========================================================
    // Material
    // ========================================================

    drone.traverse(function(child) {{

        if (child instanceof THREE.Mesh) {{

            child.material =
                new THREE.MeshStandardMaterial({{
                    color: 0x777777,
                    roughness: 0.5,
                    metalness: 0.2
                }});

        }}

    }});


    scene.add(drone);


    // ========================================================
    // Find model dimensions
    // ========================================================

    const box =
        new THREE.Box3().setFromObject(drone);

    const center =
        box.getCenter(new THREE.Vector3());

    const size =
        box.getSize(new THREE.Vector3());


    console.log(
        "Model size:",
        size.x,
        size.y,
        size.z
    );


    // ========================================================
    // Center
    // ========================================================

    drone.position.x -= center.x;
    drone.position.y -= center.y;
    drone.position.z -= center.z;


    // ========================================================
    // Scale
    // ========================================================

    const maxSize = Math.max(
        size.x,
        size.y,
        size.z
    );

    const targetsize = 20;

    const scale = targetsize / maxSize;

    drone.scale.setScalar(scale)


    // ========================================================
    // Camera
    // ========================================================

    camera.position.set(
        7,
        5,
        7
    );

    camera.lookAt(
        0,
        0,
        0
    );

    controls.target.set(
        0,
        0,
        0
    );

    controls.update();


    console.log("Drone viewer initialized");


}} catch (error) {{

    console.error(
        "DRONE ERROR:",
        error
    );

    document.getElementById("error").innerText =
        "Error loading 3D model: " + error.message;

}}


// ============================================================
// Resize
// ============================================================

window.addEventListener(
    "resize",
    function() {{

        camera.aspect =
            container.clientWidth /
            container.clientHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            container.clientWidth,
            container.clientHeight
        );

    }}
);


// ============================================================
// Animation
// ============================================================

function animate() {{

    requestAnimationFrame(animate);

    controls.update();

    renderer.render(
        scene,
        camera
    );

}}

animate();

</script>

</body>

</html>
"""


components.html(
    html,
    height=620
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