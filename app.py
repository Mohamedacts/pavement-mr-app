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
length = st.number_input("Segment Length (m)", min
