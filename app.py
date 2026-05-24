import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Set up the web page title
st.set_page_config(page_title="Animal Disease Detector", page_icon="🐾")
st.title("🐾 Animal Disease & Cure Assistant")
st.write("Upload a photo, enter or record the symptoms, and the AI will suggest the disease and cure.")

# 2. Setup the API Key
# IMPORTANT: Put your real API key back inside the quotes below!
GOOGLE_API_KEY = "YOUR_API_KEY_HERE" 
genai.configure(api_key=GOOGLE_API_KEY)

# Load the newest Gemini AI Brain
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Create the App Interface
language = st.selectbox("Select Language / भाषा निवडा / भाषा चुनें", ["English", "Marathi", "Hindi"])
animal_type = st.text_input("Which animal is sick? (e.g., Cow, Dog, Goat)")

# Provide options for text or voice for symptoms
st.write("### Symptoms")
symptoms_text = st.text_area("Type the symptoms (Optional if recording voice):")
symptoms_audio = st.audio_input("OR Record the symptoms with your microphone:")

# Image upload
uploaded_file = st.file_uploader("Upload an image of the sick animal (Optional)", type=["jpg", "jpeg", "png", "webp"])

# 4. Create the Submit Button and AI Logic
if st.button("Analyze Disease"):
    # Check if we have an animal type AND at least one type of symptom (text or voice)
    if animal_type and (symptoms_text or symptoms_audio):
        with st.spinner("Analyzing... Please wait..."):
            # Create the instruction for the AI
            prompt = f"""
            You are an expert veterinarian. 
            Animal: {animal_type}
            Typed Symptoms: {symptoms_text}
            
            Based on the typed symptoms, the voice recording (if provided), and the provided image (if any), please tell me:
            1. The possible disease name.
            2. A brief analysis of why you think it is this disease.
            3. The cure and recommended medicines.
            
            Please write the entire response in {language}. Keep the words simple and easy to understand.
            """
            
            # Prepare a list of everything we want to send to the AI
            contents_to_send = [prompt]
            
            try:
                # If an image was uploaded, add it to our list
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                    contents_to_send.append(image)
                
                # If a voice recording was made, add the audio data to our list
                if symptoms_audio is not None:
                    audio_data = {
                        "mime_type": "audio/wav",
                        "data": symptoms_audio.getvalue()
                    }
                    contents_to_send.append(audio_data)
                
                # Send everything to Gemini at once
                response = model.generate_content(contents_to_send)
                
                st.success("Analysis Complete!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred. Error details: {e}")
    else:
        st.warning("Please enter the animal type AND provide symptoms (either by typing or recording voice).")