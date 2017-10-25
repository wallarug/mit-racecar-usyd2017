import numpy as np
import pickle
from keras.models import load_model

# Evaluate one pickle file
def evaluate_one(pickle_file, model_path):
    model = load_model(model_path)
    
    pickle_file = pickle_file.reshape((1, pickle_file.shape[0], pickle_file.shape[1], pickle_file.shape[2]))
    
    class_index = np.argmax(model.predict(pickle_file))
    steering_value = ((class_index / 5.0) + ((class_index + 1) / 5.0)) / 2
    return steering_value