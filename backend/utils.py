import numpy as np
import cv2
from PIL import Image
import io

# Function to preprocess MRI image for Brain Tumor Detection model
def preprocess_mri(file):
    image = Image.open(io.BytesIO(file.read())).convert("L")  # Convert to grayscale
    image = image.resize((128, 128))  # Resize to match CNN input
    image_array = np.array(image) / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = np.expand_dims(image_array, axis=-1)  # Add channel dimension
    return image_array

# Function to process symptoms input into ML model-compatible format
def process_symptoms(symptoms, symptom_list):
    symptoms_vector = np.zeros(len(symptom_list))  # Initialize zero vector
    for symptom in symptoms:
        if symptom in symptom_list:
            index = symptom_list.index(symptom)
            symptoms_vector[index] = 1  # Mark symptom presence
    return symptoms_vector
