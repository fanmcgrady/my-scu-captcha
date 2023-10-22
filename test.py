import string
from tensorflow import keras
import numpy as np
import matplotlib.image as mpimg

model = keras.models.load_model('cnn_best_dilation.h5')

# 读取测试图片
path = "test/cp6p.jpg"
X, y = mpimg.imread(path) / 255, path.split('.')[0].lower()
X = X.reshape(-1, 60, 180, 3)

characters = string.digits + string.ascii_lowercase

# 预测
y_pred = model.predict(X)
for i in y_pred:
    print(characters[np.argmax(i)], end='')
