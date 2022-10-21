import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
dic = {0: "grey", 1: "yellow", 2: "green"}

try:
    model = load_model('color.h5')
except: 
    train = np.array([[164, 198, 203], [131, 132, 130], [130, 154, 133], [118, 156, 126], [196, 201, 199], [126, 125, 121], [132, 131, 127], [135, 160, 140], [123, 154, 126], [127, 178, 182], [123, 123, 123], [138, 176, 183], [118, 154, 127], [127, 156, 124], [124, 125, 121], [199, 198, 194], [140, 164, 147], [137, 165, 140], [134, 167, 138], [134, 163, 139], [133, 163, 134], [127, 124, 119], [118, 179, 191], [123, 124, 122], [89, 184, 194], [124, 123, 119], [112, 176, 192], [122, 119, 115], [134, 174, 179], [132, 130, 129], [132, 130, 130], [127, 124, 119], [121, 178, 186], [125, 126, 123], [94, 180, 189], [127, 124, 123], [109, 167, 110], [124, 123, 122], [122, 151, 123], [125, 125, 123], [114, 161, 118], [105, 170, 101], [129, 126, 122], [124, 163, 126], [131, 127, 126], [123, 179, 127], [104, 167, 111], [119, 158, 124], [126, 153, 129], [114, 159, 115], [113, 159, 116]])

    valid = np.array([1, 0, 2, 2, 0, 0, 0, 2, 2, 1, 0, 1, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2])

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(3, input_shape=[3], activation='softmax')
        ])
    model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(
            train, valid, epochs=100
            )
    model.summary()
    model.save('color.h5')

test = np.array([[126, 124, 120]])
pred = model.predict(test)
all_ = []
for i in pred:
    i = list(i.astype(int))
    result = i.index(max(i))
    result= dic[result]
    all_.append(result)
print(all_)

