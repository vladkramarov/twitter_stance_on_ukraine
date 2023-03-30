import pandas as pd
from tensorboard import program
import src.core as core

def load_data(data_path: str):
  data = pd.read_csv(data_path)
  return data

def launch_tensorboard():
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', str(core.MODELS_LOG_PATHS)])
    url = tb.launch()
