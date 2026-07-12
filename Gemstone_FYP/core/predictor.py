import os
import numpy as np
import tensorflow as tf
from PIL import Image
from django.conf import settings

# ==========================================
# Load Model Once
# ==========================================

MODEL_PATH = os.path.join(settings.BASE_DIR, "model", "best_model.keras")
model = tf.keras.models.load_model(MODEL_PATH)

# ==========================================
# Class Names
# (Must match training dataset order)
# ==========================================

CLASS_NAMES = [
    'Alexandrite',
    'Amber',
    'Cats Eye',
    'Malachite',
    'Morganite',
    'aquamarine',
    'diamond',
    'emerald',
    'fluorite green',
    'fluorite purple',
    'garnet',
    'peridot',
    'ruby',
    'sapphire blue',
    'sapphire pink',
    'topaz blue',
    'topaz yellow',
    'tourmaline black',
    'turquoise',
    'zircon'
]

# Image size used during training
IMG_SIZE = (224, 224)

# Minimum confidence required to accept a prediction
CONFIDENCE_THRESHOLD = 85.0

# ==========================================
# Prediction Function
# ==========================================

def predict(image_path):
    """
    Predict gemstone from uploaded image.

    Parameters
    ----------
    image_path : str
        Path to uploaded image.

    Returns
    -------
    predicted_class : str or None
        Predicted gemstone name.
        Returns None if confidence is below threshold.

    confidence : float
        Highest prediction confidence (%).

    all_predictions : dict
        Confidence scores for every class.
    """

    # Load image
    image = Image.open(image_path).convert("RGB")

    # Resize image to match training size
    image = image.resize(IMG_SIZE)

    # Convert to NumPy array
    image = np.array(image, dtype=np.float32)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Apply the same preprocessing used during training
    image = tf.keras.applications.efficientnet_v2.preprocess_input(image)

    # Model prediction
    prediction = model.predict(image, verbose=0)

    probabilities = prediction[0]

    # Get highest probability
    predicted_index = np.argmax(probabilities)
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(probabilities[predicted_index] * 100)

    # Create dictionary of all predictions
    all_predictions = {
        CLASS_NAMES[i]: round(float(probabilities[i] * 100), 2)
        for i in range(len(CLASS_NAMES))
    }

    # Print prediction for debugging
    print(f"Prediction: {predicted_class}")
    print(f"Confidence: {confidence:.2f}%")

    # Reject low-confidence predictions
    if confidence < CONFIDENCE_THRESHOLD:
        print("Rejected: Low confidence prediction.")
        return None, confidence, all_predictions

    return predicted_class, confidence, all_predictions