import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
from login import main as login_main, init_db

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_image(image, prompt_text):
    """Analyze image using Gemini Vision API"""
    model = genai.GenerativeModel('gemini-pro-vision')
    prompt = f"""
    Analyze the facial features in this image and recommend suitable makeup and accessories.
    Consider skin tone, eye color, face shape, and any other relevant features.
    
    Additional requirements: {prompt_text}
    
    Provide specific recommendations for:
    1. Foundation and concealer
    2. Eye makeup
    3. Lip color
    4. Contouring and highlighting
    5. Suitable accessories
    """
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def main():
    st.set_page_config(page_title="Beauty Advisor", layout="wide")
    
    # Initialize session states
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Show login page if not logged in
    if not st.session_state.logged_in:
        login_main()
    else:
        st.title("Beauty Advisor")
        st.write("Welcome to your personal beauty advisor!")

        # Image input section
        st.subheader("Upload or Take a Photo")
        image_option = st.radio("Choose input method:", ["Upload Image", "Take Photo"])
        
        image = None
        if image_option == "Upload Image":
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
        else:
            camera_input = st.camera_input("Take a photo")
            if camera_input:
                image = Image.open(camera_input)

        if image:
            st.image(image, caption="Your Image", use_column_width=True)
            prompt_text = st.text_input("Describe the look you're going for (optional):")
            
            if st.button("Analyze Image"):
                with st.spinner("Analyzing your image..."):
                    analysis = analyze_image(image, prompt_text)
                    st.session_state.chat_history.append(("AI", analysis))
                st.subheader("Beauty Analysis Results")
                st.write(analysis)

        # Chat history section
        if st.session_state.chat_history:
            st.subheader("Analysis History")
            for role, text in st.session_state.chat_history:
                st.write(f"{role}: {text}")

        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    init_db()
    main() 