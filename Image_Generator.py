import base64
import streamlit as st
from PIL import Image
from download_button import download_button
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, storage
import requests

firebase_config = {
    "type": st.secrets['type'],
    "project_id": st.secrets['project_id'],
    "private_key_id": st.secrets['private_key_id'],
    "private_key": st.secrets['private_key'],
    "client_email": st.secrets['client_email'],
    "client_id": st.secrets['client_id'],
    "auth_uri": st.secrets['auth_uri'],
    "token_uri": st.secrets['token_uri'],
    "auth_provider_x509_cert_url": st.secrets['auth_provider_x509_cert_url'],
    "client_x509_cert_url": st.secrets['client_x509_cert_url'],
    "universe_domain": st.secrets['universe_domain']
}


headers = {"Authorization": st.secrets['huggingface_token']}
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def generate_image_from_text(text) -> [Image, str]:
    # Call your image generation model here
    # Replace this with your own code to generate the image based on the text input
    # You can use libraries like PIL or OpenCV to create the image
    
    # Example code to generate a placeholder image
    payload = {"inputs": text}  
    image = Image.open(BytesIO(query(payload)))
    #hash the text
    citations = str(hash(text))
    return [image, text+citations]

try:
    firebase_admin.get_app()
except ValueError as e:
    # If not, initialize a new default app
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'hacktx2023-c123e.appspot.com'
    })







st.title("ArtGuardAI 🧠")
st.write("A Tool for Ethical Image Generation: Traceable Origins, Transparent AI. Know the DNA of every pixel.")
# Function to generate image from text

def upload_image(image, imageName):
    # Convert to bytes
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()

    # Encode bytes to base64 string
    b64_str = base64.b64encode(image_bytes).decode() 
    imageToString = f'data:file/txt;base64,{b64_str}'

    # Upload to Firebase
    bucket = storage.bucket()
    bucket.blob(imageName).upload_from_string(imageToString)
    return



# Initialize session state variables
if 'upload_clicked' not in st.session_state:
    st.session_state['upload_clicked'] = False
    st.session_state['image'] = None
    st.session_state['imageName'] = ""








# Initialize the session state variable to store the images


# Text input
text = st.text_input("Enter the text:")

# Create a layout with two columns
col1, col2, col3 = st.columns(3)

if col1.button("Generate Image"):
    # Generate image from text
    image, citations = generate_image_from_text(text)
    citations = ''.join(citations)

    
    
    # Display the image
    if image:
        st.session_state['image'] = image
        st.session_state['imageName'] = citations

        imageName = citations
        st.code('Citations: '+imageName)
        st.image(image, caption=text, use_column_width=True)
        
        download_button_str = download_button(image, imageName, 'Download Image')
        col2.markdown(download_button_str, unsafe_allow_html=True)

      

if col3.button("Share to Gallery"):
    st.session_state['upload_clicked'] = True

if st.session_state['upload_clicked']:
    if st.session_state['image'] is None:
        st.session_state['upload_clicked'] = False
        st.error("Please generate an image first")
    else:
        st.write("Uploading image to gallery...")
        with st.spinner('Uploading image...'):
            upload_image(st.session_state['image'], st.session_state['imageName'])
            st.success("Image uploaded to gallery")
            st.session_state['upload_clicked'] = False  
            st.session_state['image'] = None
            st.session_state['imageName'] = ""   
else:
    st.write("Click the button to upload the image to the gallery")

        

    
    






