import tensorflow as tf
import tensorflow_hub as hub
from lime import lime_image
import sys
import matplotlib.pyplot as plt
import numpy as np

model = tf.keras.models.load_model("model_v17.h5", custom_objects={'KerasLayer': hub.KerasLayer})

image_size = 256
img_path = "test_images/" + sys.argv[1] + ".jpg"

indexToXIndex = (1,10,11,12,13,14,15,16,17,18,19,2,20,21,22,23,24,25,26,27,28,29,3,30,31,32,33,34,35,36,37,38,39,4,40,41,5,6,7,8,9)

def get_img(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(image_size, image_size))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x /= 255.
    return x

explainer = lime_image.LimeImageExplainer()

explanation = explainer.explain_instance(
    get_img(img_path),
    model.predict,
    top_labels=3,
    num_samples=100
)

ind =  explanation.top_labels[0]
print("X{}".format(indexToXIndex[ind]))

dict_heatmap = dict(explanation.local_exp[ind])
heatmap = np.vectorize(dict_heatmap.get)(explanation.segments)

ind2 =  explanation.top_labels[1]
print("X{}".format(indexToXIndex[ind2]))

dict_heatmap2 = dict(explanation.local_exp[ind2])
heatmap2 = np.vectorize(dict_heatmap2.get)(explanation.segments)

plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
plt.imshow(get_img(img_path))

plt.subplot(2,2,2)
plt.imshow(heatmap, cmap = 'RdBu', vmin  = -heatmap.max(), vmax = heatmap.max())
plt.colorbar()

plt.subplot(2,2,3)
plt.imshow(get_img(img_path))

plt.subplot(2,2,4)
plt.imshow(heatmap2, cmap = 'RdBu', vmin  = -heatmap.max(), vmax = heatmap.max())
plt.colorbar()

plt.show()