import json
from typing import Dict
from . import config

import tensorflow as tf

_model = None
_labels = None
_label_set = None

def load_artifacts():
    global _model, _labels, _label_set
    if _model is None:
        _model = tf.keras.models.load_model(config.MODEL_PATH)
    if _labels is None:
        with open(config.LABELS_PATH, "r", encoding="utf-8") as f:
            _labels = json.load(f)
        _label_set = set(_labels)
    return _model, _labels

def predict_array(arr) -> Dict[str, float]:
    model, labels = load_artifacts()
    y = model.predict(arr, verbose=0)

    # softmax(N) → no se usa aquí, pero lo dejamos como guía futura
    if y.shape[-1] > 1 and not config.BINARY_SIGMOID:
        probs = y[0].tolist()
        return {labels[i]: float(probs[i]) for i in range(len(labels))}

    # sigmoid(1) declarado
    if config.BINARY_SIGMOID:
        p_pos = float(y[0][0])
        pos = config.POSITIVE_CLASS
        if pos not in _label_set:
            raise ValueError(f"POSITIVE_CLASS='{pos}' no está en labels.json: {_label_set}")
        neg = [c for c in labels if c != pos][0]
        return {pos: p_pos, neg: float(1.0 - p_pos)}

    raise ValueError("Forma de salida del modelo no coincide con configuración (softmax vs sigmoid)")
