import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
from login import main as login_main, init_db
from datetime import datetime

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

def analyze_face(image):
    """Analyze facial features using MediaPipe"""
    # Convert PIL Image to cv2 format
    if isinstance(image, Image.Image):
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]
    
    # Process the image
    results = face_mesh.process(image_rgb)
    if not results.multi_face_landmarks:
        return None
    
    landmarks = results.multi_face_landmarks[0].landmark
    
    # Extract facial measurements
    features = {
        "face_width": np.sqrt((landmarks[234].x - landmarks[454].x)**2) * width,
        "face_height": np.sqrt((landmarks[10].y - landmarks[152].y)**2) * height,
        "eye_distance": np.sqrt((landmarks[33].x - landmarks[263].x)**2) * width,
        "lip_width": np.sqrt((landmarks[61].x - landmarks[291].x)**2) * width,
    }
    
    # Determine face shape
    ratio = features["face_width"] / features["face_height"]
    if ratio > 0.95:
        features["face_shape"] = "Round"
    elif ratio < 0.85:
        features["face_shape"] = "Long"
    else:
        features["face_shape"] = "Oval"
    
    # Get skin tone from cheek area
    cheek_x = int(landmarks[123].x * width)
    cheek_y = int(landmarks[123].y * height)
    skin_color = image_rgb[cheek_y, cheek_x]
    features["skin_tone"] = f"RGB({skin_color[0]}, {skin_color[1]}, {skin_color[2]})"
    
    return features

def get_beauty_recommendations(features):
    """Get beauty recommendations using Gemini Pro"""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    As a professional makeup artist, provide personalized beauty recommendations based on these facial features:
    - Face Shape: {features['face_shape']}
    - Face Width: {features['face_width']:.1f} pixels
    - Face Height: {features['face_height']:.1f} pixels
    - Eye Distance: {features['eye_distance']:.1f} pixels
    - Lip Width: {features['lip_width']:.1f} pixels
    - Skin Tone: {features['skin_tone']}

    Provide specific recommendations for:
    1. Foundation and concealer matching the skin tone
    2. Eye makeup techniques for the eye shape
    3. Lip color and application tips
    4. Contouring placement for the face shape
    5. Complementary accessories
    
    Keep recommendations concise and practical.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

def main():
    st.set_page_config(page_title="Beauty Advisor", layout="wide")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

    if not st.session_state.logged_in:
        login_main()
    else:
        st.title("AI Beauty Advisor")
        st.write("Upload a photo or take a picture to get personalized beauty recommendations!")

        # Image input options
        col1, col2 = st.columns(2)
        
        with col1:
            camera_input = st.camera_input("Take a Photo")
            if camera_input:
                image = Image.open(camera_input)
                st.session_state.current_image = image
        
        with col2:
            uploaded_file = st.file_uploader("Upload Photo", type=['jpg', 'jpeg', 'png'])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.session_state.current_image = image

        if 'current_image' in st.session_state:
            if st.button("Analyze Face"):
                with st.spinner("Analyzing your features..."):
                    features = analyze_face(st.session_state.current_image)
                    
                    if features:
                        recommendations = get_beauty_recommendations(features)
                        
                        # Save analysis
                        analysis = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "features": features,
                            "recommendations": recommendations
                        }
                        st.session_state.analysis_history.append(analysis)
                        
                        # Display results
                        st.subheader("Your Features")
                        st.write(features)
                        
                        st.subheader("Beauty Recommendations")
                        st.write(recommendations)
                    else:
                        st.error("No face detected. Please try again with a clearer photo.")

        # Show history
        if st.session_state.analysis_history:
            st.subheader("Previous Analyses")
            for analysis in reversed(st.session_state.analysis_history[-3:]):
                with st.expander(f"Analysis from {analysis['timestamp']}"):
                    st.write("Features:", analysis['features'])
                    st.write("Recommendations:", analysis['recommendations'])

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.analysis_history = []
            st.rerun()

if __name__ == "__main__":
    init_db()
    main() 