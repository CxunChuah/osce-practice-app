import streamlit as st
import os
import sys

# Add the parent directory to the path so we can import from station modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import station modules - uncomment these as you implement each station
try:
    from stations.msk.shoulder import display_station as display_shoulder_station
    from stations.msk.knee import display_station as display_knee_station
except ImportError:
    # Create placeholder functions if the modules don't exist yet
    def display_shoulder_station():
        st.title("Shoulder Examination Station")
        st.info("This station is under development. Please check back later.")
    
    def display_knee_station():
        st.title("Knee Examination Station")
        st.info("This station is under development. Please check back later.")

# Set page config
st.set_page_config(
    page_title="OSCE Practice - Station Selection",
    page_icon="🏥",
    layout="wide"
)

# Check if logged in - using your authentication system
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this page.")
    st.switch_page("Main Page.py")  # Maintain your original redirect

# Check if we're in a specific station mode
if "selected_station" in st.session_state:
    selected = st.session_state.selected_station
    
    # Display the appropriate station based on selection
    if "MSK Station 1: Shoulder Examination" in selected:
        display_shoulder_station()
    elif "MSK Station 2: Knee Examination" in selected:
        display_knee_station()
    elif "Cardio Station 1: Cardiovascular Examination" in selected:
        st.title("Cardiovascular Examination Station")
        st.info("This station is under development. Please check back later.")
    elif "Cardio Station 2: Respiratory Examination" in selected:
        st.title("Respiratory Examination Station")
        st.info("This station is under development. Please check back later.")
    elif "Neuro Station 1: Cranial Nerve Examination" in selected:
        st.title("Cranial Nerve Examination Station")
        st.info("This station is under development. Please check back later.")
    elif "Neuro Station 2: Upper Limb Neurological Examination" in selected:
        st.title("Upper Limb Neurological Examination Station")
        st.info("This station is under development. Please check back later.")
    elif "Geriatric Station" in selected:
        st.title("Comprehensive Geriatric Assessment Station")
        st.info("This station is under development. Please check back later.")
    elif "Paediatric Station" in selected:
        st.title("Paediatric Developmental Assessment Station")
        st.info("This station is under development. Please check back later.")
    else:
        st.error(f"Unknown station: {selected}")
    
    # Clear selection if user wants to select a different station
    if st.sidebar.button("← Return to Station Selection"):
        del st.session_state.selected_station
        st.experimental_rerun()
    
    # Stop processing the rest of the page
    st.stop()

# Page title
st.title("OSCE Practice Stations")
st.write("Select a station to begin practicing your clinical skills.")

# Station categories and descriptions
stations = {
    "Musculoskeletal": [
        {
            "title": "MSK Station 1: Shoulder Examination",
            "description": "Practice a focused examination of the shoulder joint.",
            "difficulty": "Moderate",
            "time": "8 minutes"
        },
        {
            "title": "MSK Station 2: Knee Examination",
            "description": "Conduct a comprehensive assessment of the knee joint.",
            "difficulty": "Moderate",
            "time": "8 minutes"
        }
    ],
    "Cardiorespiratory": [
        {
            "title": "Cardio Station 1: Cardiovascular Examination",
            "description": "Perform a systematic cardiovascular examination.",
            "difficulty": "Challenging",
            "time": "8 minutes"
        },
        {
            "title": "Cardio Station 2: Respiratory Examination",
            "description": "Complete a thorough respiratory system examination.",
            "difficulty": "Moderate",
            "time": "8 minutes"
        }
    ],
    "Neurology": [
        {
            "title": "Neuro Station 1: Cranial Nerve Examination",
            "description": "Assess the 12 cranial nerves systematically.",
            "difficulty": "Challenging",
            "time": "10 minutes"
        },
        {
            "title": "Neuro Station 2: Upper Limb Neurological Examination",
            "description": "Perform a focused neurological examination of the upper limb.",
            "difficulty": "Moderate",
            "time": "8 minutes"
        }
    ],
    "Specialty": [
        {
            "title": "Geriatric Station: Comprehensive Geriatric Assessment",
            "description": "Perform key elements of a geriatric assessment.",
            "difficulty": "Moderate",
            "time": "10 minutes"
        },
        {
            "title": "Paediatric Station: Developmental Assessment",
            "description": "Conduct age-appropriate developmental screening.",
            "difficulty": "Challenging",
            "time": "8 minutes"
        }
    ]
}

# Display stations by category
for category, category_stations in stations.items():
    st.header(category)
    
    # Create two columns per category row
    cols = st.columns(2)
    
    # Display each station in the appropriate column
    for idx, station in enumerate(category_stations):
        col_idx = idx % 2  # Alternate between columns 0 and 1
        
        with cols[col_idx]:
            st.subheader(station["title"])
            st.write(station["description"])
            st.write(f"**Difficulty:** {station['difficulty']}")
            st.write(f"**Time:** {station['time']}")
            
            # Button to start this station
            button_label = "Start Station"
            if "MSK Station 1" in station["title"] or "MSK Station 2" in station["title"]:
                # Only enable buttons for implemented stations
                disabled = False
            else:
                button_label = "Coming Soon"
                disabled = True
                
            if st.button(button_label, key=f"btn_{station['title']}", disabled=disabled):
                # Store the selected station in session state
                st.session_state.selected_station = station["title"]
                st.experimental_rerun()
