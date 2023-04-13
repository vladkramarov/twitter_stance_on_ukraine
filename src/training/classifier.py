import pandas as pd
import src.preprocessor.preprocessor_funcs as pf
import tensorflow as tf
import numpy as np
from sklearn.metrics import f1_score
import src.core as core
from transformers import TFDistilBertModel
from typing import Callable, List
from sklearn.metrics import f1_score
from tensorflow.keras.models import load_model
from typing import Protocol

    
class Classifier:
    '''A class responsible for training a model, as well as storing model weights that resulted in the best score'''
    def __init__(self, model: Callable, model_name: str, train_data: List[np.ndarray], valid_data: List[np.ndarray]):
        self.model = model
        self.model_name = model_name
        self.train_ids = train_data[0]
        self.train_attention = train_data[1]
        self.train_labels = train_data[2]
        self.valid_ids = valid_data[0]
        self.valid_attention = valid_data[1]
        self.valid_labels = valid_data[2]

    @property
    def best_model_checkpoint_path(self):
        '''A path where best model weights are saved'''
        return f'{core.MODEL_CHECKPOINT_PATH}/{self.model_name}.h5'
    
    @property
    def log_path(self):
        '''A path where training data are saved'''
        return f'{core.MODELS_LOG_PATHS}/{self.model_name}'

    @property
    def early_stopping(self):
        return tf.keras.callbacks.EarlyStopping(
            monitor = 'val_loss',
            patience = 3,
            mode = 'min'
        )
    @property
    def best_model_checkpoint(self):
        return tf.keras.callbacks.ModelCheckpoint(
            self.best_model_checkpoint_path,
            monitor='val_loss',
            save_best_only=True
        )
    @property
    def tensorboard(self):
        return tf.keras.callbacks.TensorBoard(self.log_path)
    
    @property
    def list_of_default_callbacks(self):
        return [self.early_stopping, self.best_model_checkpoint, self.tensorboard]


    def fit(self, batch_size: int=64, epochs: int=5, verbose: int=1, callbacks: List[Callable] = None):
        '''Trains the model'''
        if callbacks==None:
            callbacks = self.list_of_default_callbacks
        self.batch_size = batch_size
        history = self.model.fit(
            x=[self.train_ids, self.train_attention], y=self.train_labels, 
            validation_data = ([self.valid_ids, self.valid_attention], self.valid_labels),
            epochs=epochs, verbose=verbose, callbacks=callbacks, batch_size = self.batch_size)
    
    @property
    def best_model(self):
        '''Model with weights that yielded the highest training results'''
        tf.keras.utils.get_custom_objects().update({'TFDistilBertModel': TFDistilBertModel})
        return load_model(self.best_model_checkpoint_path)
            
    def predict(self, inputs: List[np.ndarray]):
        '''Automatically uses the best model (from checkpoint) to classify new input data'''
        predicted_logits = self.best_model.predict(inputs)
        predicted_label = np.argmax(predicted_logits, axis=-1)
        return predicted_label

    def overwright_final_model(self):
        '''Overwrights previous model used for classifying'''
        self.model.save(core.TRANSFORMER_MODEL)

class Evaluator:
    '''A class that evaluates the model on test and sanity check data. Also logs all the results to tensorboard. Uses a previously trained classifier as input'''
    def __init__(self, trained_classifier: Classifier, test_data: List[np.ndarray], sanity_dataset: pd.DataFrame = core.SANITY_CHECK_DATAFRAME):
        self.trained_classifier = trained_classifier
        self.test_ids = test_data[0]
        self.test_attention = test_data[1]
        self.test_labels_logits = test_data[2]
        self.sanity_dataset = sanity_dataset
    
    @property
    def true_test_labels(self):
        return np.argmax(self.test_labels_logits, axis = -1)
    
    def classify_test_data(self):
        predicted_labels = self.trained_classifier.predict([self.test_ids, self.test_attention])
        self.predicted_labels = predicted_labels

    def classify_sanity_check_dataset(self):
        sanity_ids, sanity_attention = pf.distilbert_tokenizer(self.sanity_dataset, 'text')
        sanity_predicted_labels = self.trained_classifier.predict([sanity_ids, sanity_attention])
        self.sanity_predicted_labels = sanity_predicted_labels
    
    @property
    def test_accuracy(self):
        return np.mean(self.predicted_labels==self.true_test_labels)
    
    @property
    def test_f1_score(self):
        return f1_score(self.true_test_labels, self.predicted_labels, average='macro')
    
    @property 
    def sanity_test_accuracy(self):
        '''Accuracy on the sanity check dataset'''
        return np.mean(self.sanity_predicted_labels==self.sanity_dataset['label'])
    
    @property
    def sanity_test_f1_score(self):
        '''F1 score on the sanity check dataset'''
        return f1_score(self.sanity_dataset['label'], self.sanity_predicted_labels, average='macro')
    
    def write_to_tensorboard(self):
        '''Writes metrics used for evaluation to a tensorboard log'''
        with tf.summary.create_file_writer(self.trained_classifier.log_path).as_default():
            tf.summary.scalar('test_accuracy', self.test_accuracy, step=1)
            tf.summary.scalar('test_f1', self.test_f1_score, step = 1)
            tf.summary.scalar('sanity_accuracy', self.sanity_test_accuracy, step=1)
            tf.summary.scalar('sanity_f1', self.sanity_test_f1_score, step = 1)
    
