import base64
import io
import requests
from PIL import Image
from . import config

def load_image_from_url(url: str) -> Image.Image:
    r = requests.get(url, timeout=config.REQUEST_TIMEOUT)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    return img

def load_image_from_b64(b64: str) -> Image.Image:
    raw = base64.b64decode(b64, validate=True)
    if len(raw) > config.MAX_BASE64_SIZE_MB * 1024 * 1024:
        raise ValueError("Imagen en base64 excede el tamaño permitido")
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return img

def preprocess(img: Image.Image, img_size: int):
    img = img.resize((img_size, img_size))
    import numpy as np
    arr = (np.array(img).astype("float32") / 255.0)
    arr = arr[None, ...] 
    return arr
