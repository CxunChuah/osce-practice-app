import streamlit as st
from datetime import datetime
import time

def display_station():
    st.title("Knee Examination OSCE Station")
    
    # Station information
    st.markdown("""
    ## Instructions
    
    You are asked to perform a focused examination of the knee joint on a 28-year-old patient 
    who presents with right knee pain following a football match 2 weeks ago. The patient reports 
    feeling a "pop" and experiencing immediate swelling.
    
    **Time allowed:** 8 minutes
    
    **Tasks:**
    1. Take a focused history
    2. Perform a systematic knee examination
    3. Explain your findings and differential diagnosis to the examiner
    """)
    
    # Start station button
    if 'station_started' not in st.session_state:
        st.session_state.station_started = False
        st.session_state.start_time = None
        st.session_state.current_step = 0
        st.session_state.completed_steps = []
        st.session_state.notes = ""
    
    # Timer display
    if st.session_state.station_started:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 8*60 - elapsed)
        
        mins, secs = divmod(int(remaining), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        # Display timer prominently
        st.markdown(f"""
        <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; text-align:center;">
            <h2>Time Remaining: {time_str}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # End station if time runs out
        if remaining <= 0:
            st.session_state.station_started = False
            st.warning("Time's up! Please complete your examination.")
            st.session_state.show_feedback = True
            st.rerun()  # Updated from experimental_rerun()
    
    # Station content
    if not st.session_state.station_started:
        if st.button("Start Station"):
            st.session_state.station_started = True
            st.session_state.start_time = time.time()
            st.rerun()  # Updated from experimental_rerun()
    else:
        # Define examination steps
        steps = [
            {
                "name": "Introduction & Consent",
                "content": """
                ### Introduction & Consent
                
                **Expected actions:**
                - Introduce yourself to the patient
                - Explain the examination procedure
                - Obtain consent
                - Ensure patient comfort and appropriate exposure
                
                **Sample dialogue:**
                "Hello, my name is [your name]. I'm a physiotherapy student. I'd like to examine your knee today. Is that okay with you?"
                """,
                "checklist": [
                    "Introduced self",
                    "Explained procedure",
                    "Obtained consent",
                    "Ensured appropriate exposure"
                ]
            },
            {
                "name": "Inspection",
                "content": """
                ### Inspection
                
                **Expected actions:**
                - Observe both knees from front, side, and back
                - Look for swelling, deformity, scars, muscle wasting
                - Assess gait pattern if appropriate
                - Note alignment (varus/valgus)
                
                **Findings:**
                The right knee shows moderate swelling. There is no obvious deformity or visible muscle wasting at this stage. The patient has a slight antalgic gait, favoring the right leg.
                """,
                "checklist": [
                    "Observed from multiple angles",
                    "Checked for swelling/effusion",
                    "Noted alignment and deformity",
                    "Assessed gait (if appropriate)"
                ]
            },
            {
                "name": "Palpation",
                "content": """
                ### Palpation
                
                **Expected actions:**
                - Palpate bony landmarks (patella, tibial tuberosity, femoral condyles)
                - Palpate joint lines (medial and lateral)
                - Assess for warmth, tenderness, and effusion
                - Perform patellar tap test for effusion
                
                **Findings:**
                There is warmth over the right knee. Tenderness is present along the medial joint line. Positive patellar tap test indicating effusion. No bony tenderness over the patella or tibial tuberosity.
                """,
                "checklist": [
                    "Palpated key bony landmarks",
                    "Palpated joint lines",
                    "Assessed for effusion",
                    "Noted areas of tenderness"
                ]
            },
            {
                "name": "Movement",
                "content": """
                ### Movement Assessment
                
                **Expected actions:**
                - Assess active and passive range of motion:
                  - Flexion (0-135°)
                  - Extension (0°)
                - Note any crepitus, pain, or restriction
                
                **Findings:**
                Active flexion is limited to 110° on the right with pain at end range. Passive flexion achieves 120° with discomfort. Full extension is possible but causes mild discomfort. No significant crepitus noted.
                """,
                "checklist": [
                    "Assessed active flexion",
                    "Assessed active extension",
                    "Assessed passive ROM",
                    "Noted pain and restrictions"
                ]
            },
            {
                "name": "Special Tests",
                "content": """
                ### Special Tests
                
                **Expected actions:**
                Perform appropriate special tests:
                - Anterior drawer test
                - Posterior drawer test
                - Lachman's test
                - Valgus/varus stress tests
                - McMurray's test
                - Patellofemoral assessment
                
                **Findings:**
                Positive Lachman's test with soft endpoint. Positive anterior drawer test. Medial joint line tenderness with positive McMurray's test for the medial meniscus. Negative posterior drawer and varus/valgus stress tests.
                """,
                "checklist": [
                    "Performed cruciate ligament tests",
                    "Performed collateral ligament tests",
                    "Performed meniscal tests",
                    "Interpreted test results correctly"
                ]
            },
            {
                "name": "Functional Assessment",
                "content": """
                ### Functional Assessment
                
                **Expected actions:**
                - Assess patient's ability to perform functional movements
                - Evaluate impact on activities and sport
                
                **Sample questions/tests:**
                "Can you squat down comfortably?"
                "How does the knee feel when climbing stairs?"
                "Has this affected your ability to play sports?"
                """,
                "checklist": [
                    "Assessed functional movements",
                    "Evaluated impact on daily activities",
                    "Assessed impact on sports/hobbies"
                ]
            },
            {
                "name": "Completion",
                "content": """
                ### Completion & Presentation
                
                **Expected actions:**
                - Thank the patient
                - Ensure patient comfort
                - Summarize findings
                - Present differential diagnosis
                
                **Differential Diagnosis:**
                1. Anterior cruciate ligament (ACL) tear
                2. Medial meniscus tear
                3. Combined ACL and meniscal injury
                4. MCL sprain (mild)
                
                **Next steps:**
                Recommend appropriate imaging (MRI) and initial management strategies.
                """,
                "checklist": [
                    "Thanked patient",
                    "Ensured patient comfort",
                    "Summarized findings accurately",
                    "Provided reasonable differential",
                    "Suggested appropriate next steps"
                ]
            }
        ]
        
        # Display current step
        current_step = st.session_state.current_step
        
        if current_step < len(steps):
            step = steps[current_step]
            
            st.markdown(step["content"])
            
            # Checklist for current step
            st.subheader("Checklist")
            
            checklist_cols = st.columns(2)
            checked_items = []
            
            for i, item in enumerate(step["checklist"]):
                col_idx = i % 2
                with checklist_cols[col_idx]:
                    if st.checkbox(item, key=f"check_{current_step}_{i}"):
                        checked_items.append(item)
            
            # Notes section
            st.text_area("Your notes for this step:", 
                          key=f"notes_{current_step}", 
                          height=100)
            
            # Navigation buttons
            cols = st.columns(2)
            
            with cols[0]:
                if current_step > 0:
                    if st.button("Previous Step"):
                        st.session_state.current_step -= 1
                        st.rerun()  # Updated from experimental_rerun()
            
            with cols[1]:
                if st.button("Next Step"):
                    # Save completed checklist items
                    st.session_state.completed_steps.append({
                        "step_name": step["name"],
                        "completed_items": checked_items,
                        "total_items": len(step["checklist"]),
                        "notes": st.session_state.get(f"notes_{current_step}", "")
                    })
                    
                    st.session_state.current_step += 1
                    st.rerun()  # Updated from experimental_rerun()
        else:
            # Station completed
            st.success("You have completed all steps of the examination!")
            
            # Calculate score
            total_checklist_items = sum(len(s["checklist"]) for s in steps)
            completed_items = sum(len(s["completed_items"]) for s in st.session_state.completed_steps)
            score_percentage = (completed_items / total_checklist_items) * 100
            
            # Display score
            st.markdown(f"""
            ## Station Summary
            
            **Score:** {completed_items}/{total_checklist_items} ({score_percentage:.1f}%)
            
            **Performance by section:**
            """)
            
            # Display performance by section
            for i, step_result in enumerate(st.session_state.completed_steps):
                step_score = (len(step_result["completed_items"]) / step_result["total_items"]) * 100
                st.markdown(f"""
                **{step_result["step_name"]}:** {len(step_result["completed_items"])}/{step_result["total_items"]} ({step_score:.1f}%)
                """)
                
                if step_result["notes"]:
                    st.markdown(f"**Your notes:** {step_result['notes']}")
            
            # Save results button
            if st.button("Save Results"):
                # Here you would implement saving to database
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to session state for now
                if "practice_history" not in st.session_state:
                    st.session_state.practice_history = []
                
                st.session_state.practice_history.append({
                    "station": "Knee Examination",
                    "timestamp": timestamp,
                    "score": f"{score_percentage:.1f}%",
                    "details": st.session_state.completed_steps
                })
                
                st.success("Results saved successfully!")
            
            # Return to stations button
            if st.button("Return to Stations"):
                # Reset the current station state but keep practice history
                for key in list(st.session_state.keys()):
                    if key not in ['logged_in', 'username', 'practice_history']:
                        del st.session_state[key]
                        
                # Clear selected station
                if "selected_station" in st.session_state:
                    del st.session_state.selected_station
                    
                st.rerun()  # Updated from experimental_rerun()

# For testing directly
if __name__ == "__main__":
    display_station()
