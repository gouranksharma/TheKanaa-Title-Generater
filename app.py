import streamlit as st
from google import genai
from google.genai import types

# Page Configuration & Styling
st.set_page_config(
    page_title="E-Commerce AI Title Generator",
    page_icon="🛍️",
    layout="centered"
)

st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
    }
    div.stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='text-align: center; color: #1F2937;'>🛍️ E-Commerce AI Title Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>Paste your raw product titles below and convert them into clean, SEO-optimized standards instantly.</p>", unsafe_allow_html=True)
st.markdown("---")

# PASTE YOUR VALID STANDARD GEMINI API KEY HERE (starts with AIza...)
DIRECT_API_KEY = "AIzaSy..." 
MODEL_CHOICE = "gemini-2.5-flash"

# Input Section
st.markdown("### 📥 Raw Product Titles")
st.markdown("Enter your titles below (one per line):")

default_input = (
    "nike air max shoes black size 9 running mens\n"
    "samsung 4k smart tv 55 inch led ultra hd\n"
    "stainless steel water bottle 32oz insulated blue"
)

raw_titles_text = st.text_area("Raw Titles Area", value=default_input, height=180, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

# Generate Button
if st.button("✨ Generate Standardized Titles"):
    titles_list = [t.strip() for t in raw_titles_text.split("\n") if t.strip()]
    
    if not titles_list:
        st.warning("⚠️ Please enter at least one product title to process.")
    elif DIRECT_API_KEY == "AIzaSy...":
        st.error("⚠️ Please replace the placeholder with your actual Gemini API key in the code.")
    else:
        with st.spinner("🤖 AI is formatting your titles..."):
            try:
                client = genai.Client(api_key=DIRECT_API_KEY)
                
                system_instruction = (
                    "You are an expert e-commerce SEO copywriter. "
                    "Your task is to transform messy raw product titles into clean, optimized, and standardized titles. "
                    "Follow this structure: [Brand] [Product Name] [Key Feature/Material] [Target Audience/Use Case] [Variant: Color/Size]. "
                    "Capitalize appropriately (Title Case), remove keyword spam, filler words, and unnecessary punctuation. "
                    "Return only the transformed titles as a clean numbered list matching the input order."
                )
                
                prompt = f"Please standardize the following raw e-commerce product titles:\n\n{raw_titles_text}"
                
                response = client.models.generate_content(
                    model=MODEL_CHOICE,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                    )
                )
                
                st.markdown("---")
                st.markdown("### 📤 Standardized Output")
                st.markdown(response.text)
                        
            except Exception as e:
                st.error(f"❌ An error occurred during processing: {e}")
