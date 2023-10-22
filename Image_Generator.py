import base64
import streamlit as st
from PIL import Image
from download_button import download_button
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, storage

# firebase_config = {
#     "type": st.secrets['type'],
#     "project_id": st.secrets['project_id'],
#     "private_key_id": st.secrets['private_key_id'],
#     "private_key": st.secrets['private_key'],
#     "client_email": st.secrets['client_email'],
#     "client_id": st.secrets['client_id'],
#     "auth_uri": st.secrets['auth_uri'],
#     "token_uri": st.secrets['token_uri'],
#     "auth_provider_x509_cert_url": st.secrets['auth_provider_x509_cert_url'],
#     "client_x509_cert_url": st.secrets['client_x509_cert_url'],
#     "universe_domain": st.secrets['universe_domain']
# }
firebase_config = {
  "type": "service_account",
  "project_id": "hacktx2023-c123e",
  "private_key_id": "f8437760e5db4ed2d251a305c3a70f64396f58f3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDAXi0ic8Vw8VhJ\nNH1RSqMAen98uOX83kGvTffK4tlnFozA7PMzivXiWSCo8MV07d/22jT1TdP6ujWl\nR8TYHC0kJLU96qEz7UKgKHzMPaFFbfrh1ZTd59vfD1Se8NwCf7XSpctpHrhPHDKA\napsrPK1FzFOM73icLT1xVcAhBSf4LGT5W8N8dfO9yed25beuG43DvqQpIB+DA57j\nleOkh0WviIuZBbJ9hM9vh3slSF8znCo/AloW7FGvOJMax3aeibuWJFg9cyfLW60f\nihzkdplnERsXGSdaJOTHzFhnG5nHn4vN9//FGuAiXr3OItQar2CxEmClVKe3CCuV\nPlwol8URAgMBAAECggEAA56yEDwn+r5b6DK/6fPy2cs0U3NCRq4jA8q+jzeSGj3D\nI81BrVZf1qTRN8SiHpdsV7+W8AfJJaZz5HqTgnKTSeMT8wiThH/iOVPRt2Ewg/c0\nGaRUgxF+InYuJDiJl1VyZTaf+4grtTdlXuPCrD9dzlqwNs550UyLo7KWpThs3l9l\nI9F2O7tScFhsiLT647UMVZ331S80J7V20leVRrC5js+G3pzCjPWwVXq1zQF62m4S\n29tVwIJd0FU0RT4VIb5kX5ayyirQ8PRjvprT/culVw0YUsT8hTrMcUd1G+bj1lwB\ngnLmZ6tgbXqn3Hm8oo7ImBaGn5HubMDOEqnXeNX+gQKBgQDgSC1i8PFZ5pv6w5TX\nntQPIRSs9vJIQcS37LzVO6rttYRElVDlsiWeCxivdzT87c0nw8FvY4EMSop1KORC\n802pFfveQ/K2SfP3irmo0c1qMxcDVnD0pa1EBG6maTYEPMZ66Ye7QBjwWo9lDrIl\n0TJHRN18iarvTmkyOOCch7rvYQKBgQDbkpf5O6Oz6L+eufSjGHpKp2Ag/fb4BN3Z\n+o1eRZJXWLVOnTzjRXvhzUCaOxGzWh1qY/bW6L4vS97TR0kzzwmbCpmiOLA3biKY\nXYfU75pdtloFg3W/WTiKEZfXYrrTFydZ+G/iAfcSAm83txCMLrpAoV/eU+f+8rgG\nFOyJXF4jsQKBgHA3zPW/ZpM7znmW2GdWYfY78BNm7+z1c08vlX//fdO4SbjjGPoE\nu8uq86v/sjSHa2nlCWkJWW1j8okSb7uL7ySWClK4nr1UnUwTTjfI2cW0UGRsINJX\n/yyUJyT+aXePTSP8qtwnAxNnzG2c/8fqNwTv0P5aB3v7OKlXShMn2oGhAoGBANjz\nBTn7FYrDo+G/NtqXau2sZyzyAj2ZAWNJTrkg4LFxMuOUNP8SPo8i8HvzdU/S8FGY\np+I8YP32Zxo2yztni8QnOxmwDV0XcxM9BuL8Q3fonxXniEYib9zr+S2VnabIr9cT\nw+h5rJec1CsmtDDuUpVdXY4dNZMQW4eW0Qf/vfxhAoGBAJ+Y0TDQvxXSouftCClP\nV78DxqGA35edbNlZCHmmyVmivReEEulkwS7nbd6J13J+uBMqrovHHZsYt/AIN7JF\nCr8uN197VIcRceiUY6Xyr0sM7aFeqK8sRI0E2QpeEQH+SHCaxiJ1ERDdrBzDr6kL\nZJWTJgwlZY9X4+e6yxJURaD1\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-kxj29@hacktx2023-c123e.iam.gserviceaccount.com",
  "client_id": "117073521950045136282",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-kxj29%40hacktx2023-c123e.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}



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

        imageName = citations
        st.code('Citations: '+imageName)
        st.image(image, caption=text, use_column_width=True)
        
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

        

    
    






