# lesson_plan_generator.py

import streamlit as st
import openai

def run():
    st.title("📚 Hong Kong Kindergarten Lesson Plan Generator")
    st.caption("🎯 Generate detailed lesson plans following EDB Kindergarten Education Curriculum Guide (2017, updated 2022)")
    
    # Initialize OpenAI client
    client = openai.OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        base_url=st.secrets.get("OPENAI_BASE_URL"),
    )
    
    # Define the 7 EDB learning areas
    learning_areas = [
        "Physical Fitness and Health",
        "Language (Chinese, English, or Putonghua)",
        "Early Mathematics", 
        "Science and Technology",
        "Self and Society",
        "Arts",
        "Nature and Living"
    ]
    
    # Define activity approaches
    activity_approaches = [
        "Whole class activities",
        "Small group activities", 
        "Free play",
        "Outdoor exploration",
        "Arts and crafts",
        "Music and movement",
        "Story telling",
        "Role playing",
        "Hands-on experiments",
        "Sensory play"
    ]
    
    # Input form
    st.header("📝 Lesson Plan Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Group selection
        age_group = st.selectbox(
            "Age Group",
            ["K1", "K2", "K3"],
            help="Select the kindergarten level"
        )
        
        # Theme input
        theme = st.text_input(
            "Theme",
            placeholder="e.g., Animals, Transportation, Community Helpers",
            help="Enter the main theme for the lesson plan"
        )
        
        # Number of sessions
        num_sessions = st.number_input(
            "Number of Sessions", 
            min_value=1, 
            max_value=10, 
            value=1,
            help="1 session = single lesson, multiple sessions = module"
        )
        
    with col2:
        # Language selection
        language = st.selectbox(
            "Language of Lesson Plan Output",
            ["English", "Traditional Chinese"],
            help="Select the language for the generated lesson plan"
        )
        
        # Learning areas selection
        selected_learning_areas = st.multiselect(
            "Select Learning Areas",
            learning_areas,
            default=["Science and Technology"],
            help="Choose one or more learning areas to focus on"
        )
        
        # Activity approaches selection
        selected_approaches = st.multiselect(
            "Select Activity Approaches",
            activity_approaches,
            default=["Hands-on experiments", "Small group activities"],
            help="Choose teaching approaches to include"
        )
    
    # Additional notes
    additional_notes = st.text_area(
        "Additional Notes (Optional)",
        placeholder="Any specific requirements, materials, or considerations...",
        help="Provide any additional information or special requirements"
    )
    
    # Generate button
    if st.button("🎯 Generate Lesson Plan", type="primary"):
        if not theme:
            st.error("Please enter a theme for the lesson plan.")
            return
        
        if not selected_learning_areas:
            st.error("Please select at least one learning area.")
            return
            
        if not selected_approaches:
            st.error("Please select at least one activity approach.")
            return
        
        # Create the detailed prompt
        prompt = create_lesson_plan_prompt(
            age_group, theme, num_sessions, language, 
            selected_learning_areas, selected_approaches, additional_notes
        )
        
        # Generate lesson plan
        with st.spinner("Generating lesson plan... This may take a moment."):
            try:
                response = client.chat.completions.create(
                    model="Meta-Llama-4-Maverick-17B-128E-Instruct-FP8",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                lesson_plan = response.choices[0].message.content
                
                # Display the generated lesson plan
                st.header("📋 Generated Lesson Plan")
                st.markdown(lesson_plan)
                
                # Download option
                st.download_button(
                    label="📥 Download Lesson Plan",
                    data=lesson_plan,
                    file_name=f"lesson_plan_{theme.replace(' ', '_')}_{age_group}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Error generating lesson plan: {e}")

def create_lesson_plan_prompt(age_group, theme, num_sessions, language, learning_areas, approaches, additional_notes):
    """Create the detailed prompt for lesson plan generation"""
    
    prompt = f"""You are an expert Hong Kong kindergarten curriculum designer with full knowledge of the 
Hong Kong EDB Kindergarten Education Curriculum Guide (2017, updated 2022) and related 
Early Childhood Education requirements.

Task: Generate a detailed lesson plan or multi-session module according to the user inputs.

**Context:**
- School Type: Local Hong Kong Kindergarten
- Age Group: {age_group}
- Theme: "{theme}" 
  (If multiple sessions, treat as a module with interconnected lessons; 
   if 1 session, treat as a single lesson.)
- Number of Sessions: {num_sessions}
- Language of Lesson Plan Output: {language}
- Selected Learning Areas: {', '.join(learning_areas)}
- Selected Activity Approaches: {', '.join(approaches)}
- Additional Notes from User: {additional_notes if additional_notes else 'None provided'}

**EDB Requirements:**
Hong Kong kindergartens must plan activities to support balanced development across the 7 learning areas:
1. Physical Fitness and Health
2. Language (Chinese, English, or Putonghua)
3. Early Mathematics
4. Science and Technology
5. Self and Society
6. Arts
7. Nature and Living

**Requirements for the lesson plan:**
1. Follow EDB principles: child-centred, play-based, balanced development across domains.
2. Integrate selected learning areas and approaches meaningfully into activities.
3. Provide developmentally appropriate and engaging activities with clear teacher guidance.
4. Structure each session as:
   - **Session Title** (linked to theme/module)
   - **Objectives** (2–4 measurable outcomes)
   - **Warm-up / Circle Time** (3–5 min)
   - **Core Activities** (15–25 min, linked to learning areas)
   - **Closing / Reflection** (5–10 min)
   - **Materials Needed**
   - **Teacher Tips & Observation Focus**
5. For multi-session plans:
   - Sequence lessons logically, building on prior sessions.
   - Ensure varied activity approaches (whole class, small group, free play).
6. Avoid irrelevant or random text. Output only in the requested language.
7. Use bullet points and clear headings.

Now generate the plan(s)."""

    return prompt