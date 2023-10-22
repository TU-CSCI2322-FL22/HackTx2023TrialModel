import base64
import streamlit as st
from PIL import Image
from download_button import download_button
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, storage



try:
    firebase_admin.get_app()
except ValueError as e:
    # If not, initialize a new default app
    cred = credentials.Certificate(st.secrets['firebase_config'])
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'hacktx2023-c123e.appspot.com'
    })







st.title("Text-to-Image+Citations")
# Function to generate image from text

def upload_image(image, imageName):
    # Convert to bytes
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()

    # Encode bytes to base64 string
    b64_str = base64.b64encode(image_bytes).decode() 

    # Upload to Firebase
    bucket = storage.bucket()
    bucket.blob(imageName).upload_from_string(b64_str)
    return



# Initialize session state variables
if 'upload_clicked' not in st.session_state:
    st.session_state['upload_clicked'] = False
    st.session_state['image'] = None
    st.session_state['imageName'] = ""


def generate_image_from_text(text) -> [Image, str]:
    # Call your image generation model here
    # Replace this with your own code to generate the image based on the text input
    # You can use libraries like PIL or OpenCV to create the image
    
    # Example code to generate a placeholder image
    image = Image.new('RGB', (300, 300), color = (73, 109, 137))
    # citation = f"{class_name}_{random_name}_img{idx}_{random_chars}"

    citations = "This is a placeholder image".split()
    return [image, citations]





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
        st.image(image, caption=text, use_column_width=True)
        imageName = citations
        download_button_str = download_button(image, imageName, 'Download Image')
        col2.markdown(download_button_str, unsafe_allow_html=True)

      

if col3.button("Upload to Gallery"):
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

        

    
    






