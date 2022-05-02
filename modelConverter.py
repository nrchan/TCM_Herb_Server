import tensorflow as tf
import tensorflow_hub as hub

model = tf.keras.models.load_model("model_v7.h5", custom_objects={'KerasLayer': hub.KerasLayer})

with open("model.tflite", "wb") as f:
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()
    f.write(tflite_model)