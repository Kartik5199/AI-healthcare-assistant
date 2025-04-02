import random

# Sample diseases and tumor results for placeholder predictions
SAMPLE_DISEASES = ["Flu", "Common Cold", "COVID-19", "Malaria", "Typhoid", "Dengue"]
SAMPLE_TUMOR_RESULTS = ["Tumor Detected", "No Tumor Detected", "Unclear MRI, Needs Further Testing"]

# Function to generate a random disease as a placeholder
def predict_disease(symptoms):
    return random.choice(SAMPLE_DISEASES)

# Function to generate a random brain tumor result as a placeholder
def predict_brain_tumor():
    return random.choice(SAMPLE_TUMOR_RESULTS)
