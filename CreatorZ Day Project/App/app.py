import streamlit as st
from PIL import Image
from google import genai
from google.genai import types


# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="AI Plant Care Assistant",
    page_icon="🌱",
    layout="centered"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🌱 AI Plant Care Assistant")

st.write(
    "Upload a picture of your plant or describe its problem "
    "and let AI provide plant care suggestions."
)

st.divider()


# -----------------------------
# API KEY
# -----------------------------


MY_API_KEY = st.secrets["GEMINI_API_KEY"]

# Create Gemini client
client = genai.Client(api_key=MY_API_KEY)


# -----------------------------
# USER INPUT
# -----------------------------

st.subheader("🌿 Tell us about your plant")

uploaded_image = st.file_uploader(
    "Upload a picture of your plant",
    type=["jpg", "jpeg", "png"]
)

plant_description = st.text_area(
    "Describe your plant problem",
    placeholder=(
        "Example: My tomato plant has yellow leaves "
        "and the soil is always wet."
    ),
    height=120
)


# -----------------------------
# DISPLAY IMAGE
# -----------------------------

if uploaded_image:
    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Uploaded Plant",
        use_container_width=True
    )


# -----------------------------
# ANALYSE BUTTON
# -----------------------------

if st.button("🔍 Analyse Plant", use_container_width=True):

    if not uploaded_image and not plant_description:
        st.warning(
            "Please upload a plant image or describe your plant problem."
        )
        st.stop()


    # -----------------------------
    # AI INSTRUCTIONS
    # -----------------------------

    prompt = """
You are an AI Plant Care Assistant.

Your job is to help users understand common plant health
problems and provide simple plant care recommendations.

Analyse the user's plant image and/or description.

Please provide your answer using this format:

🌱 Plant Health Analysis

1. Possible Problem
- Explain the most likely plant health issue.

2. Possible Causes
- Give the possible causes of the problem.

3. 💧 Watering
- Give suitable watering advice.

4. ☀️ Sunlight
- Give suitable sunlight advice.

5. 🌿 Fertiliser
- Give safe and general fertiliser advice.

6. 🪴 General Plant Care
- Give other useful care suggestions.

7. ⚠️ Important Note
- If the image or information is not enough to identify the
  problem confidently, clearly say that it is only a possibility
  and recommend checking the plant more closely.

Do not claim that a diagnosis is 100% certain.
Use simple language that is easy for beginners to understand.
"""


    # -----------------------------
    # PREPARE AI CONTENT
    # -----------------------------

    contents = [prompt]

    if plant_description:
        contents.append(
            "\nUser's plant description:\n"
            + plant_description
        )

    if uploaded_image:
        image_bytes = uploaded_image.getvalue()

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=uploaded_image.type
            )
        )


    # -----------------------------
    # SEND TO GEMINI
    # -----------------------------

    with st.spinner("🌱 AI is analysing your plant..."):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents
            )

            st.divider()
            st.subheader("🔍 Plant Analysis")

            st.markdown(response.text)

        except Exception as e:

            st.error(
                "Something went wrong while connecting to Gemini."
            )

            st.code(str(e))
