import os
import json

path = os.path.abspath(__file__)
BASE_PATH = os.path.dirname(path)
data_path = os.path.join(BASE_PATH, "data")
dataset_path = os.path.join(BASE_PATH, "dataset")
extensions_list = [".pdf", ".PDF"]