import tensorflow as tf
from keras import Model
from tensorflow.keras.optimizers.legacy import Adam
from keras.layers import Conv1D, MaxPooling1D, LSTM, Bidirectional, GlobalMaxPooling1D, BatchNormalization, Dense, Input, Concatenate
import src.core as core
import src.training.class_train
import importlib
importlib.reload(core)
importlib.reload(src.training.class_train)
from transformers import TFDistilBertModel

checkpoint = 'distilbert-base-uncased'
distilbert = TFDistilBertModel.from_pretrained(checkpoint)

def compile_model():
    '''Defines and compiles a model'''
    input_ids = Input(shape = (core.MAX_LENGTH, ), name = 'input_ids', dtype='int32')
    attention_masks = Input(shape = (core.MAX_LENGTH, ),name = 'attention_mask', dtype='int32')
    embedding_layer = distilbert(input_ids, attention_masks)[0]

    conv_3 = Conv1D(128, kernel_size = 3, activation='relu', padding='same')(embedding_layer)
    max_pool_3 = MaxPooling1D(3)(conv_3)
    X = Conv1D(128, kernel_size = 5, activation='relu', padding='same')(max_pool_3)
    X = MaxPooling1D(3)(X)
    X = GlobalMaxPooling1D()(X)
    X = Dense(128, activation='relu')(X)
    output = Dense(3, activation='softmax')(X)
    model = Model([input_ids, attention_masks], output)

    for layer in model.layers[:3]:
        layer.trainable=False
    adam = Adam()
    model.compile(optimizer=adam, loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False), metrics=['accuracy'])
    return model
