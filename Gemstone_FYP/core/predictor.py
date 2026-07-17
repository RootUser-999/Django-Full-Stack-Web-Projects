import os
import numpy as np
import tensorflow as tf
from PIL import Image
from django.conf import settings

# ==========================================
# Load Models Once
# ==========================================

# Multi-class gemstone classifier
MODEL_PATH = os.path.join(settings.BASE_DIR, "model", "best_model.keras")
gemstone_model = tf.keras.models.load_model(MODEL_PATH)

# Binary classifier (0 = Non-Gemstone, 1 = Gemstone)
BINARY_MODEL_PATH = os.path.join(settings.BASE_DIR, "model", "bestmodel_2.keras")
binary_model = tf.keras.models.load_model(BINARY_MODEL_PATH)

# ==========================================
# Class Names
# ==========================================

CLASS_NAMES = [
    "Alexandrite",
    "Amber",
    "Cats Eye",
    "Malachite",
    "Morganite",
    "aquamarine",
    "diamond",
    "emerald",
    "fluorite green",
    "fluorite purple",
    "garnet",
    "peridot",
    "ruby",
    "sapphire blue",
    "sapphire pink",
    "topaz blue",
    "topaz yellow",
    "tourmaline black",
    "turquoise",
    "zircon",
]

# ==========================================
# Image Sizes
# ==========================================

BINARY_IMG_SIZE = (160, 160)
CLASSIFIER_IMG_SIZE = (224, 224)

# ==========================================
# Prediction Function
# ==========================================

def predict(image_path):
    """
    Predict gemstone from uploaded image.

    Returns
    -------
    predicted_class : str or None
        Gemstone name if detected.
        Returns None if the image is not a gemstone.

    confidence : float
        Prediction confidence (%).

    all_predictions : dict
        Confidence scores for every gemstone class.
    """

    # Open image once
    original_image = Image.open(image_path).convert("RGB")

    # ==========================================
    # STEP 1: Binary Classification
    # ==========================================

    binary_image = original_image.resize(BINARY_IMG_SIZE)

    binary_image = np.array(binary_image, dtype=np.float32)
    binary_image = np.expand_dims(binary_image, axis=0)

    binary_image = tf.keras.applications.efficientnet_v2.preprocess_input(
        binary_image
    )

    binary_prediction = binary_model.predict(binary_image, verbose=0)

    # Binary model output
    gem_probability = float(binary_prediction[0][0])

    print(f"Gemstone Probability: {gem_probability:.4f}")

    # 0 = Non-Gemstone
    # 1 = Gemstone
    if gem_probability < 0.5:
        print("Prediction: Not a Gemstone")
        return None, round((1 - gem_probability) * 100, 2), {}

    # ==========================================
    # STEP 2: Multi-Class Classification
    # ==========================================

    classifier_image = original_image.resize(CLASSIFIER_IMG_SIZE)

    classifier_image = np.array(classifier_image, dtype=np.float32)
    classifier_image = np.expand_dims(classifier_image, axis=0)

    classifier_image = tf.keras.applications.efficientnet_v2.preprocess_input(
        classifier_image
    )

    prediction = gemstone_model.predict(classifier_image, verbose=0)

    probabilities = prediction[0]

    predicted_index = np.argmax(probabilities)
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(probabilities[predicted_index] * 100)

    # Confidence scores for all gemstone classes
    all_predictions = {
        CLASS_NAMES[i]: round(float(probabilities[i] * 100), 2)
        for i in range(len(CLASS_NAMES))
    }

    print(f"Prediction: {predicted_class}")
    print(f"Confidence: {confidence:.2f}%")

    return predicted_class, confidence, all_predictions