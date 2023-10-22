from tensorflow.keras.utils import Sequence
import numpy as np
import matplotlib.image as mpimg
import random
import os

# 数据生成器
class CaptchaSequence(Sequence):
    def __init__(self, characters, batch_size, path, steps, n_len=4, width=180, height=60):
        self.characters = characters
        self.batch_size = batch_size
        self.steps = steps
        self.n_len = n_len
        self.width = width
        self.height = height
        self.n_class = len(characters)
        self.generator = ImageGenerate(path)
        self.coder = Coder(characters)

    def __len__(self):
        return self.steps

    # 生成一个batch的数据
    def __getitem__(self, idx):
        X = np.zeros((self.batch_size, self.height, self.width, 3), dtype=np.float32)
        y = [np.zeros((self.batch_size, self.n_class), dtype=np.uint8) for i in range(self.n_len)]
        for i in range(self.batch_size):
            X[i], random_str = self.generator.generate_image()
            for j, ch in enumerate(random_str):
                y[j][i] = self.coder.encode(ch)
        return X, y

# 字符编码器
class Coder:
    def __init__(self, characters):
        self.characters = characters.lower()

    def encode(self, char):
        result = np.zeros(len(self.characters), dtype=np.uint8)
        result[self.characters.find(char.lower())] = 1
        return result

    def decode(self, array):
        return self.characters[np.argmax(array)]

# 图片生成器
class ImageGenerate:
    def __init__(self, path):
        def f1(s):
            return len(s) == 8

        self.path = path
        self.file_list = list(filter(f1, os.listdir(path)))
        random.shuffle(self.file_list)
        self.item = 0
        self.length = len(self.file_list)
        self.data = [self.generate_image1() for i in range(self.length)]
        self.item = 0

    def generate_image1(self):
        file_name = self.file_list[self.item]
        path = os.path.join(self.path, file_name)
        self.item = (self.item + 1) % self.length
        return mpimg.imread(path) / 255, file_name.split('.')[0].lower()

    def generate_image(self):
        self.item = (self.item + 1) % self.length
        return self.data[self.item]
