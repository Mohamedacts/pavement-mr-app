import streamlit as st
from utils.astm_guidance import ASTM_GUIDANCE
from utils.data_validation import validate_required_fields

# ASTM-based dropdowns
FLEXIBLE_DISTRESS_TYPES = [
    "Alligator Cracking", "Bleeding", "Block Cracking", "Corrugation", "Depression",
    "Edge Cracking", "Joint Reflection Cracking", "Lane/Shoulder Drop-Off", "Longitudinal & Transverse Cracking",
    "Patching & Utility Cut Patching", "Polished Aggregate", "Potholes", "Railroad Crossing",
    "Raveling (Weathering)", "Rutting", "Shoving", "Slippage Cracking", "Swelling"
]
RIGID_DISTRESS_TYPES = [
    "Blowup", "Corner Break", "Divided Slab", "Durability Cracking", "Faulting", "Joint Seal Damage",
    "Lane/Shoulder Drop-Off", "Linear Cracking", "Patching", "Polished Aggregate", "Popouts",
    "Pumpings", "Scaling, Map Cracking, Crazing", "Settlement", "Shattered Slab", "Shrinkage Cracking", "Spalling"
]
TREATMENTS = [
    "Routine Maintenance", "Crack Sealing", "Surface Sealing", "Thin Overlay", "Thick Overlay", "Partial Depth Repair",
    "Full Depth Repair", "Reconstruction", "Patching", "Slab Replacement", "Diamond Grinding", "Other"
]

def recommend_treatment(pci, distress_type, severity, traffic_volume, climate_zone, facility_type, pavement_type):
    # Example logic: expand as needed for your standards or agency
    if pci >= 85:
        return "Routine Maintenance"
    elif pci >= 70:
        if "Cracking" in distress_type and severity == "Low":
            return "Crack Sealing"
        elif traffic_volume > 10000:
            return "Thin Overlay"
        else:
            return "Surface Sealing"
    elif pci >= 50:
        if traffic_volume > 20000 or climate_zone.lower() in ["hot", "wet"]:
            return "Thick Overlay"
        else:
            return "Partial Depth Repair"
    else:
        if facility_type in ["Airport Runway", "Taxiway"]:
            return "Full Depth Repair"
        elif pavement_type == "Rigid":
            return "Slab Replacement"
        else:
            return "Reconstruction"

st.set_page_config(page_title="ASTM Pavement M&R Planner", layout="wide")
st.title("ASTM-Compliant Pavement Maintenance & Rehabilitation Planner")
st.markdown("""
This tool guides you step-by-step using ASTM D6433 (roads/parking lots) and ASTM D5340 (airfields).  
All fields and recommendations reference the relevant ASTM standard.
""")

# Step 1: Pavement & Facility Type
st.header("1. Project Setup")
with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["pavement_type"]["info"] + f" **[{ASTM_GUIDANCE['pavement_type']['standard']}]**")
pavement_type = st.selectbox("Pavement Type", ["Flexible", "Rigid"])

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["facility_type"]["info"] + f" **[{ASTM_GUIDANCE['facility_type']['standard']}]**")
facility_type = st.selectbox("Facility Type", ["Highway", "Local Road", "Airport Runway", "Taxiway", "Apron"])

# Step 2: Pavement Inventory
st.header("2. Pavement Inventory")
with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["segment_id"]["info"])
segment_id = st.text_input("Segment ID (required)")

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["length"]["info"])
length = st.number_input("Segment Length (m)", min_value=0.0)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["width"]["info"])
width = st.number_input("Segment Width (m)", min_value=0.0)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["layer_type"]["info"])
layer_type = st.text_input("Layer Type")

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["thickness"]["info"])
thickness = st.number_input("Layer Thickness (mm)", min_value=0.0)

# Step 3: Condition Survey
st.header("3. Condition Survey")
with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["pci"]["info"])
pci = st.number_input("Pavement Condition Index (PCI, 0-100)", min_value=0, max_value=100)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["distress_type"]["info"])
if pavement_type == "Flexible":
    distress_type = st.selectbox("Distress Type", FLEXIBLE_DISTRESS_TYPES)
else:
    distress_type = st.selectbox("Distress Type", RIGID_DISTRESS_TYPES)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["severity"]["info"])
severity = st.selectbox("Severity Level", ["Low", "Medium", "High"])

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["extent"]["info"])
extent = st.number_input("Extent of Distress (%)", min_value=0, max_value=100)

# Step 4: Traffic and Environment
st.header("4. Traffic and Environment")
with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["traffic_volume"]["info"])
traffic_volume = st.number_input("Traffic Volume (AADT)", min_value=0)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["load_type"]["info"])
load_type = st.text_input("Load Type (e.g., ESALs)")

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["climate_zone"]["info"])
climate_zone = st.text_input("Climate Zone")

# Step 5: M&R Options
st.header("5. Maintenance & Rehabilitation Options")
with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["treatment"]["info"])
treatment = st.selectbox("Select Treatment", TREATMENTS)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["treatment_effectiveness"]["info"])
treatment_effectiveness = st.text_input("Expected Effectiveness (years of life extension)")

# Step 6: Cost and Resources
st.header("6. Cost and Resource Inputs")
with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["unit_cost"]["info"])
unit_cost = st.number_input("Unit Cost ($/m²)", min_value=0.0)

with st.expander("Guidance"):
    st.info(ASTM_GUIDANCE["budget"]["info"])
budget = st.number_input("Available Budget ($)", min_value=0.0)

# Step 7: Review & Validation
st.header("7. Review Inputs")
inputs = {
    "segment_id": segment_id,
    "length": length,
    "width": width,
    "layer_type": layer_type,
    "thickness": thickness,
    "pci": pci,
}
required_fields = ["segment_id", "length", "width", "layer_type", "thickness", "pci"]
missing = validate_required_fields(inputs, required_fields)
if missing:
    st.warning(f"Missing required fields per ASTM standard: {', '.join(missing)}")
else:
    if st.button("Generate M&R Plan"):
        recommended = recommend_treatment(pci, distress_type, severity, traffic_volume, climate_zone, facility_type, pavement_type)
        st.success("M&R Plan generated per ASTM D6433/D5340. See below for details.")
        st.markdown(f"""
        - **Pavement Type**: {pavement_type} ({ASTM_GUIDANCE['pavement_type']['standard']})
        - **Facility Type**: {facility_type} ({ASTM_GUIDANCE['facility_type']['standard']})
        - **Segment ID**: {segment_id}
        - **PCI**: {pci} ({ASTM_GUIDANCE['pci']['standard']})
        - **Distress**: {distress_type} ({severity}), {extent}%
        - **Traffic Volume**: {traffic_volume} AADT
        - **Climate Zone**: {climate_zone}
        - **Recommended Treatment**: {recommended}
        - **Selected Treatment**: {treatment}
        - **Expected Effectiveness**: {treatment_effectiveness} years
        - **Budget Used**: ${unit_cost * length * width:.2f}
        """)
        st.info("For detailed guidance, refer to the official ASTM D6433 or D5340 documentation at each step.")

st.markdown("**Note:** All guidance and field requirements are derived from the relevant ASTM standards. Please consult the standards for full details.")
