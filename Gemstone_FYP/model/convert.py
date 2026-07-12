import os
import sys
import traceback
import tensorflow as tf

# ==========================================================
# CONFIGURATION
# ==========================================================

KERAS_MODEL = "best_model.keras"
TFLITE_MODEL = "best_model.tflite"

print("=" * 70)
print("TensorFlow Lite Converter")
print("=" * 70)

print("TensorFlow Version :", tf.__version__)
print()

# ==========================================================
# CHECK FILE
# ==========================================================

if not os.path.exists(KERAS_MODEL):
    print(f"❌ Model not found: {KERAS_MODEL}")
    sys.exit(1)

# ==========================================================
# LOAD MODEL
# ==========================================================

print("Loading model...")

try:
    model = tf.keras.models.load_model(KERAS_MODEL, compile=False)
    print("✅ Model loaded successfully.\n")
except Exception:
    print("❌ Failed to load model\n")
    traceback.print_exc()
    sys.exit(1)

# ==========================================================
# MODEL SUMMARY
# ==========================================================

print("=" * 70)
model.summary()
print("=" * 70)

# ==========================================================
# TRY CONVERSION
# ==========================================================

strategies = [
    {
        "name": "Standard Conversion",
        "converter": lambda m: tf.lite.TFLiteConverter.from_keras_model(m)
    },
    {
        "name": "Conversion with Select TF Ops",
        "converter": lambda m: tf.lite.TFLiteConverter.from_keras_model(m)
    }
]

success = False

for i, strategy in enumerate(strategies):

    print(f"\n{'='*70}")
    print(f"Attempt {i+1}: {strategy['name']}")
    print("="*70)

    try:

        converter = strategy["converter"](model)

        converter.optimizations = [
            tf.lite.Optimize.DEFAULT
        ]

        if i == 1:

            converter.target_spec.supported_ops = [
                tf.lite.OpsSet.TFLITE_BUILTINS,
                tf.lite.OpsSet.SELECT_TF_OPS
            ]

            converter._experimental_lower_tensor_list_ops = False

        converter.inference_input_type = tf.float32
        converter.inference_output_type = tf.float32

        print("Converting...")

        tflite_model = converter.convert()

        with open(TFLITE_MODEL, "wb") as f:
            f.write(tflite_model)

        print("\n✅ Conversion Successful!")

        size = os.path.getsize(TFLITE_MODEL) / (1024 * 1024)

        print(f"Saved : {TFLITE_MODEL}")
        print(f"Size  : {size:.2f} MB")

        success = True
        break

    except Exception as e:

        print("\n❌ Conversion Failed")

        print("\nError Type:")
        print(type(e).__name__)

        print("\nError Message:")
        print(e)

        print("\nFull Traceback:\n")
        traceback.print_exc()

# ==========================================================
# VERIFY
# ==========================================================

if success:

    print("\nVerifying generated model...")

    try:

        interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL)

        interpreter.allocate_tensors()

        print("✅ Verification Successful")

        print("\nInput Details")

        for inp in interpreter.get_input_details():
            print(inp)

        print("\nOutput Details")

        for out in interpreter.get_output_details():
            print(out)

        print("\n🎉 Your model is ready for Flutter.")

    except Exception:

        print("\n⚠ Model was created but verification failed.")

        traceback.print_exc()

else:

    print("\n❌ All conversion methods failed.")