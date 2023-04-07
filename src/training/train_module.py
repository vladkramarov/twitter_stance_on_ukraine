import src.preprocessor.preprocessor_pipelines as pp
import src.core as core
import importlib
from transformers import TFDistilBertModel
import src.training.classifier as ct
import src.training.model_compiler as mc
import src.utils as ut
from typing import Tuple
importlib.reload(core)
importlib.reload(src.training.classifier)
importlib.reload(pp)
importlib.reload(ct)
importlib.reload(mc)

train_ids, train_attention, train_labels = pp.prepare_training_data(ut.load_data(core.TRAIN_DATASET_DIR))
valid_ids, valid_attention, valid_labels = pp.prepare_training_data(ut.load_data(core.VALID_DATASET_DIR))
test_ids, test_attention, test_labels = pp.prepare_training_data(ut.load_data(core.TEST_DATASET_DIR))

def train_and_evaluate() -> Tuple[ct.Classifier, ct.Evaluator]: 
  '''A pipeline that 
          1.Uses compile_model function to compile a model
          2.Creates a Classifier class
          3.Trains and evaluates the model
          4.Writes the results to tensorboard'''
  classifier = ct.Classifier(mc.compile_model(), 'transformer_conv_3_maxpool_conv5_maxpool_global_max',
  [train_ids, train_attention, train_labels],
  [valid_ids, valid_attention, valid_labels])
  classifier.fit(batch_size=16, epochs=10)
  evaluator = ct.Evaluator(classifier, 
                            [test_ids, test_attention, test_labels])
  evaluator.classify_test_data()
  evaluator.classify_sanity_check_dataset()
  evaluator.write_to_tensorboard()
  return classifier, evaluator

clasifier, evaluator = train_and_evaluate()
evaluator.sanity_test_accuracy

import pandas as pd
train_data = pd.read_csv(core.TRAIN_DATASET_DIR).shape
print(train_data)
valid_data = pd.read_csv(core.VALID_DATASET_DIR).shape
test_data = pd.read_csv(core.TEST_DATASET_DIR).shape
test_data