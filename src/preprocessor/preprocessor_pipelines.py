import src.preprocessor.preprocessor_funcs as pf
import pandas as pd
import keras


def preprocess_pipeline(dataset: pd.DataFrame, text_feature: str = pf.TEXT_COLUMN):
    '''A pipeline of preprocessing and tokenizing functions'''
    dataset[text_feature] = dataset[text_feature].apply(pf.clean_tweets).apply(pf.replace_flag_emojis).apply(pf.remove_emojis)
    dataset = pf.drop_short_tweets(dataset, text_feature)
    input_ids, attention_mask = pf.distilbert_tokenizer(dataset, text_feature)
    return dataset, input_ids, attention_mask

def prepare_training_data(dataset: pd.DataFrame, label_feature: str = pf.LABEL_COLUMN):
    dataset, input_ids, attention_mask = preprocess_pipeline(dataset)
    one_hot_encoded_labels = keras.utils.to_categorical(dataset[label_feature])
    return input_ids, attention_mask, one_hot_encoded_labels



