from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Flatten, Dense
from tensorflow.keras.callbacks import EarlyStopping, CSVLogger, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model
from CaptchaSequence import *
import string



# 设置字符范围
characters = string.digits + string.ascii_lowercase

# 设置宽度、高度、字符长度、字符种类width, height, n_len, n_class
width = 180
height = 60
n_len = 4
n_class = len(characters)

# 构建CNN模型
input_tensor = Input((height, width, 3))
x = input_tensor
for i, n_cnn in enumerate([(2, 2), (2, 2), (2, 3), (1, 5)]):
    for j in range(n_cnn[0]):
        x = Conv2D(32 * 2 ** min(i, 3), kernel_size=3 - 2 * j, padding='same', kernel_initializer='he_uniform',
                   dilation_rate=(n_cnn[0], n_cnn[0]))(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
    x = MaxPool2D(n_cnn[1])(x)
x = Flatten()(x)
x = [Dense(n_class, activation='softmax', name='c%d' % (i + 1))(x) for i in range(n_len)]
model = Model(inputs=input_tensor, outputs=x)

# 打印模型
print(model.summary())
plot_model(model, to_file='cnn_dilation.png', show_shapes=True)

# 设置训练参数
train_data = CaptchaSequence(characters, batch_size=128, steps=1000, path='train')
valid_data = CaptchaSequence(characters, batch_size=128, steps=100, path='test')
callbacks = [EarlyStopping(patience=3),
             CSVLogger('cnn_dilation.csv'),
             ModelCheckpoint('cnn_best_dilation.h5',
                             save_best_only=True)]

# 编译模型
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(1e-3, amsgrad=True),
              metrics=['accuracy'])

# 训练模型
model.fit_generator(train_data, epochs=3,
                    validation_data=valid_data,
                    callbacks=callbacks)
