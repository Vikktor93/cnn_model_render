import os

IMG_SIZE = int(os.getenv("IMG_SIZE", "128"))
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.keras")
LABELS_PATH = os.getenv("LABELS_PATH", "artifacts/labels.json")

BINARY_SIGMOID = os.getenv("BINARY_SIGMOID", "true").lower() == "true"
POSITIVE_CLASS = os.getenv("POSITIVE_CLASS", "muffin")  # Aquí se ajusta según labels[1]

MAX_BASE64_SIZE_MB = float(os.getenv("MAX_BASE64_SIZE_MB", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")
