import tensorflow as tf

model = tf.keras.models.load_model("best_model.keras", compile=False)

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [tf.lite.Optimize.DEFAULT]

# DO NOT use SELECT_TF_OPS
# DO NOT set supported_ops

tflite_model = converter.convert()

with open("best_model.tflite", "wb") as f:
    f.write(tflite_model)

print("Done!")