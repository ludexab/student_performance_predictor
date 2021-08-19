import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


def load_trained_model():
    model = load_model('gpa_model.h5')
    return model


def stdscaler(cgpa):
    # Scalers, either StandardScaler or MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 5))
    # scaler = StandardScaler()

    cgpa_array = np.array(cgpa)

    shaped_cgpa = cgpa_array.reshape(1, -1)
    mmscaled_cgpa = scaler.fit_transform(shaped_cgpa)
    inversed_cgpa = scaler.inverse_transform(mmscaled_cgpa)
    lstm_shaped_cgpa = inversed_cgpa.reshape((1, 1, 9))
    return lstm_shaped_cgpa


def make_prediction(cgpa):
    model = load_trained_model()
    prepped_cgpa = stdscaler(cgpa)
    prediction = model.predict(prepped_cgpa)
    return prediction
