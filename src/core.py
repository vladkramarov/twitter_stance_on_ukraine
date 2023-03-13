from pathlib import Path
import pandas as pd

PACKAGE_ROOT = Path('tweeter_ukraine').resolve().parent
DATASET_DIR = PACKAGE_ROOT / 'dataset'
TRAIN_DATASET_DIR = DATASET_DIR / 'train_set.csv'
VALID_DATASET_DIR = DATASET_DIR / 'valid_set.csv'
TEST_DATASET_DIR = DATASET_DIR / 'test_set.csv'
CONFIG_FILE_PATH = PACKAGE_ROOT / 'config.ini'

MODEL_ROOT = PACKAGE_ROOT / 'models'
BEST_MODEL_FOLDER = MODEL_ROOT / 'best_model'
BEST_MODEL = BEST_MODEL_FOLDER / 'best_model.h5'
MAX_LENGTH = 90
MODELS_LOG_PATHS = MODEL_ROOT / 'logs'
MODEL_CHECKPOINT_PATH = MODEL_ROOT / 'checkpoints'

SANITY_TEXTS = ['ukraine must win', 'russia must win', 'ukraine is full of nazis', 'russia is out ally, not ukraine', 'ukraine will win', 'ukraine needs tanks and jets',
                'putin is a terrorist', 'zelenskyy is a terrorist', 'ukraine is a pathetic puppet country', 'ukraine is not a real country', 'nato is to provide additional military help to ukraine',
                'ukraine should not exist', 'nazi took over ukraine', 'ukrainian terrorist government']
SANITY_LABELS = [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1]

SANITY_CHECK_DATAFRAME = pd.DataFrame({'text':SANITY_TEXTS, 'label':SANITY_LABELS})

TABLE_NAME = 'new_tweets_revised'

