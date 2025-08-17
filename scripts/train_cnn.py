import os, json
from pathlib import Path
import tensorflow as tf

# HIPERPARÁMETROS Y RUTAS
IMG_SIZE = int(os.getenv("IMG_SIZE", "128"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "64"))
EPOCHS = int(os.getenv("EPOCHS", "15"))

TRAIN_DIR = os.getenv("TRAIN_DIR", "data/train")
VAL_DIR   = os.getenv("VAL_DIR", "data/val")

ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "artifacts")
MODEL_PATH = os.getenv("MODEL_PATH", f"{ARTIFACTS_DIR}/model.keras")
LABELS_PATH = os.getenv("LABELS_PATH", f"{ARTIFACTS_DIR}/labels.json")


# DATASETS DESDE CARPETAS (CARGA DE DATOS)
def make_ds(directory, img_size, batch_size, shuffle=True):
    return tf.keras.preprocessing.image_dataset_from_directory(
        directory,
        labels="inferred",          # infiere etiquetas desde subcarpetas
        label_mode="binary",        # etiquetas binarias (0/1)
        color_mode="rgb",
        batch_size=batch_size,
        image_size=(img_size, img_size),
        shuffle=shuffle,
    )

# DEFINICIÓN DEL MODELO
def build_model(img_size):
    inputs = tf.keras.Input(shape=(img_size, img_size, 3))
    x = tf.keras.layers.Rescaling(1./255)(inputs)
    x = tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)  # SIGMOID(1)
    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")]
    )
    return model

def main():
    print(f"IMG_SIZE={IMG_SIZE}  BATCH_SIZE={BATCH_SIZE}  EPOCHS={EPOCHS}")
    print(f"Train dir: {TRAIN_DIR}  Val dir: {VAL_DIR}")

    train_ds = make_ds(TRAIN_DIR, IMG_SIZE, BATCH_SIZE, shuffle=True)
    val_ds = make_ds(VAL_DIR, IMG_SIZE, BATCH_SIZE, shuffle=False)

    # Orden de clases por índice (clave para la API)
    class_names = train_ds.class_names
    print("class_names (por índice):", class_names)

    # Prefetch para rendimiento
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds   = val_ds.prefetch(AUTOTUNE)

    model = build_model(IMG_SIZE)
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True, monitor="val_auc", mode="max")
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    # EXPORTA ARTEFACTOS
    Path(ARTIFACTS_DIR).mkdir(exist_ok=True, parents=True)
    model.save(MODEL_PATH)
    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

    print("Artefactos guardados:")
    print(" -", MODEL_PATH)
    print(" -", LABELS_PATH)
    print("Recuerda cuál es índice 1 (clase positiva) al configurar la API.")

if __name__ == "__main__":
    main()
