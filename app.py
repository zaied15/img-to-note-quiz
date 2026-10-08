import streamlit as st
from PIL import Image
from api_calling import note_generator, audio_transcription, quiz_generator

# Site Title and header
st.title("Summary and Quiz Generator")
st.subheader("Upload upto 3 images to generate summary and quizzes")
st.divider()

# Sidebar
with st.sidebar:
    st.header("Search Here")

    images = st.file_uploader("Upload image(s) of your note", ['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    pil_images = list(map(Image.open, images))

# Image upload options
    if images:
        if len(images) > 3:
            st.error("Upload max 3 images")
        else:
            st.subheader("Your uploaded images")
            col = st.columns(len(images))
            for i, img in enumerate(images):
                with col[i]:
                    st.image(img)

# Difficulties part
    difficulties = st.selectbox('Enter your difficulties label',['Easy', 'Medium', 'Hard'], index=None)
    if difficulties:
        st.markdown(f"You selected **{difficulties}** as difficulty")
        
    search_btn = st.button("Click to generate", type="primary")


if search_btn:
    if not images:
        st.error("Please upload atleast 1 image")
    if not difficulties:
        st.error("Select an option as difficulty")
    if images and difficulties:

        # Note Generate
        with st.container(border=True):
            st.subheader("Summary or note", anchor=None)
            with st.spinner("AI is generating your notes..."):
                note = note_generator(pil_images)
                st.markdown(note, anchors=False)

        # Audio Generate
        with st.container(border=True):
            st.subheader("Summary in audio transcript", anchor=None)
            note_for_audio = note.replace("#", "").replace("*", "").replace("-", "")
            with st.spinner("Audio generating..."):
                my_audio = audio_transcription(note_for_audio)
                st.audio(my_audio)


        # Quiz section
        with st.container(border=True):
            st.subheader(f"Quiz of difficulty level ({difficulties})", anchor=None)
            with st.spinner("Quize generating..."):
             quiz = quiz_generator(pil_images, difficulties)
             st.markdown(quiz)



