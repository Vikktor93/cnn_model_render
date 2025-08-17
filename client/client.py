import base64, requests, json, os, sys

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def pretty(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)

def predict_url(img_url: str):
    print("\n=== Predicción por URL ===")
    print("API:", API_URL)
    print("Image URL:", img_url)
    try:
        r = requests.post(f"{API_URL}/predict",
                          json={"image_url": img_url},
                          timeout=30)
        print("Status:", r.status_code)
        print("Response:", pretty(r.json()))
    except Exception as e:
        print("Error:", e)

def predict_b64(path: str):
    print("\n=== Predicción por Base64 ===")
    print("API:", API_URL)
    print("Local file:", path)
    if not os.path.exists(path):
        print(f"No existe el archivo: {path}")
        return
    try:
        b64 = base64.b64encode(open(path, "rb").read()).decode("utf-8")
        r = requests.post(f"{API_URL}/predict",
                          json={"image_b64": b64},
                          timeout=60)
        print("Status:", r.status_code)
        print("Response:", pretty(r.json()))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # 1) Muffin por URL
    muffin_url = "https://recetaamericana.com/wp-content/uploads/2022/07/mejor-magdalenas-chispas-chocolate-300x300.jpg"
    # 2) Perro chihuahua por URL
    chihuahua_url = "https://cdn.pixabay.com/photo/2014/09/19/21/47/chihuahua-453063_1280.jpg"
    # 3) Base64 (archivo local)
    local_img = "client/ejemplo-muffin.png"  # imagen de ejemplo de un muffin

    predict_url(muffin_url)
    predict_url(chihuahua_url)
    predict_b64(local_img)
