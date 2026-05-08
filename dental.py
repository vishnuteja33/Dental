import os
import google.generativeai as genai
from PIL import Image
import pydicom
import numpy as np

# --- CONFIGURATION ---
API_KEY = "AIzaSyC9rJDt3yud6YxfrLRlP1iHmc6e-ZDB74U"
genai.configure(api_key=API_KEY)

def convert_dicom_to_pil(dicom_path, save_copy=True):
    """Converts DICOM to a PIL Image and optionally saves a PNG copy."""
    ds = pydicom.dcmread(dicom_path)
    
    # 1. Extract and Normalize pixels
    # Dental X-rays are high-bit; we must scale them to 0-255 for standard screens
    img_array = ds.pixel_array.astype(float)
    rescaled = (np.maximum(img_array, 0) / img_array.max()) * 255
    final_image = Image.fromarray(np.uint8(rescaled))
    
    # 2. SAVE THE FILE (This answers your question!)
    if save_copy:
        new_filename = dicom_path.replace('.dcm', '.png')
        final_image.save(new_filename)
        print(f"✅ Saved converted image as: {new_filename}")
        
    return final_image

def run_dental_analysis(file_path):
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    
    if file_path.lower().endswith('.dcm'):
        img = convert_dicom_to_pil(file_path)
    else:
        img = Image.open(file_path)

    prompt = "Analyze this dental X-ray and provide a clinical report on cavities and bone health."
    
    print("🧠 Analyzing...")
    response = model.generate_content([prompt, img])
    print("\n" + response.text)

if __name__ == "__main__":
    # Change this to your file name
    run_dental_analysis("dental.dcm")