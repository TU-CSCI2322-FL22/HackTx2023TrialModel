from pathlib import Path
import streamlit as st
from PIL import Image
from io import BytesIO
import streamlit_authenticator as stauth 
import yaml
from yaml.loader import SafeLoader
from download_button import download_button




with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator.login('Login', 'main')



def main():
    st.title("Text-to-Image+Citations")
    # Function to generate image from text

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
            st.image(image, caption=text, use_column_width=True)
            imageName = citations + ".jpeg"
            download_button_str = download_button(image, imageName, 'Download Image')
            col2.markdown(download_button_str, unsafe_allow_html=True)

            if col3.button("Upload to Gallery"):
                # Save the image to the 'img' folder
                image.save(Path('img', imageName))
                st.success("Image uploaded successfully!")


    
    
    
    
# Run the app

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    main()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')