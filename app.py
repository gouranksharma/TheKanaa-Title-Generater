import os
import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(
    page_title="E-Commerce AI Title Generator",
    page_icon="🛍️",
    layout="wide"
)

# App Header
st.title("🛍️ E-Commerce AI Title Generator")
st.markdown("Transform messy, unformatted raw product titles into clean, SEO-optimized, and standardized titles instantly.")

# Sidebar for API Key Configuration
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Enter Gemini API Key", type="password")
    
    model_choice = st.selectbox(
        "Select Model",
        ["gemini-2.5-flash", "gemini-2.5-pro"]
    )
    
    st.markdown("---")
    st.markdown("### Standard Formula")
    st.markdown("`[Brand] [Product Name] [Key Feature/Material] [Target Audience] [Color/Size]`")

# Main Interface Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Raw Input Titles")
    st.markdown("Enter your raw product titles below (one per line):")
    
    default_input = (
        "nike air max shoes black size 9 running mens\n"
        "samsung 4k smart tv 55 inch led ultra hd\n"
        "stainless steel water bottle 32oz insulated blue"
    )
    
    raw_titles_text = st.text_area("Raw Titles", value=default_input, height=250)

# Process Button
if st.button("✨ Generate Standardized Titles", type="primary"):
    # Check for API key (supports input box or Streamlit secrets for deployment)
    api_key = api_key_input or os.environ.get("GEMINI_API_KEY")
    
    try:
        if not api_key and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not api_key:
        st.error("⚠️ Please provide a Gemini API Key in the sidebar or add it to your Streamlit Secrets.")
    else:
        titles_list = [t.strip() for t in raw_titles_text.split("\n") if t.strip()]
        
        if not titles_list:
            st.warning("⚠️ Please enter at least one title to process.")
        else:
            with st.spinner("Processing titles with AI..."):
                try:
                    # Initialize the Gemini client
                    client = genai.Client(api_key=api_key)
                    
                    system_instruction = (
                        "You are an expert e-commerce SEO copywriter. "
                        "Your task is to transform messy raw product titles into clean, optimized, and standardized titles. "
                        "Follow this structure: [Brand] [Product Name] [Key Feature/Material] [Target Audience/Use Case] [Variant: Color/Size]. "
                        "Capitalize appropriately (Title Case), remove keyword spam, filler words, and unnecessary punctuation. "
                        "Return only the transformed titles as a clean numbered list matching the input order."
                    )
                    
                    prompt = f"Please standardize the following raw e-commerce product titles:\n\n{raw_titles_text}"
                    
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2,
                        )
                    )
                    
                    with col2:
                        st.subheader("📤 Standardized Output")
                        st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"❌ An error occurred during processing: {e}")
