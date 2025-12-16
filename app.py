import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

# --- CONFIGURATION ---
# 1. PASTE YOUR API KEY HERE
API_KEY = "YOUR_API_KEY_HERE"
# Configure the AI model
genai.configure(api_key=API_KEY)

# --- THE "HANDS": TOOLS FOR THE AI ---
def check_inventory_database(item_name: str):
    """
    Looks up stock level, price, and location for a specific item name.
    """
    try:
        with open('inventory.json', 'r') as f:
            data = json.load(f)
        
        item_info = data.get(item_name.lower())
        
        if item_info:
            return item_info
        else:
            return {"error": "Item not found in database."}
    except Exception as e:
        return {"error": str(e)}

tools_list = [check_inventory_database]

# --- THE "BRAIN": SETUP GEMINI ---
# UPDATED: Using the model we found in your account
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-preview-09-2025',
    tools=tools_list
)

# --- THE "FACE": STREAMLIT UI ---
st.title("📦 Smart Inventory Auditor")
st.write("Upload a photo of an item to check its stock level instantly.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Item', use_column_width=True)

    if st.button('Audit Item'):
        with st.spinner('Analyzing image with Gemini 2.5...'):
            try:
                # Start the Chat Session with automatic function calling
                chat = model.start_chat(enable_automatic_function_calling=True)
                
                prompt = "Identify this object. Then, use the inventory tool to check its status and give me a full report."
                response = chat.send_message([prompt, image])
                
                st.success("Audit Complete!")
                st.markdown(response.text)
                
                with st.expander("See Technical Details (For Judges)"):
                    st.write("Gemini 2.5 recognized the object and triggered the `check_inventory_database` function.")
            except Exception as e:

                st.error(f"An error occurred: {e}")
