from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from .schemas import PredictRequest, PredictResponse, ErrorResponse
from . import utils, config, inference

app = FastAPI(
    title="Muffins vs Chihuahuas API",
    version="0.0.1",
    description="Servicio de predicción para clasificación binaria (CNN)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.ALLOW_ORIGINS] if config.ALLOW_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["info"])
def root():
    return {"message": "Muffins vs Chihuahuas API — usa /docs para probar o /health para estado"}

@app.get("/health", response_model=Dict[str, str], tags=["health"])
def health():
    try:
        inference.load_artifacts()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"health_error: {e}")

@app.post("/predict", response_model=PredictResponse,
          responses={400: {"model": ErrorResponse}}, tags=["predict"])
def predict(payload: Dict):
    try:
        req = PredictRequest.model_validate_request(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        if req.image_url:
            img = utils.load_image_from_url(str(req.image_url))
        else:
            img = utils.load_image_from_b64(req.image_b64)

        arr = utils.preprocess(img, config.IMG_SIZE)
        probs = inference.predict_array(arr)
        label = max(probs, key=probs.get)
        score = probs[label]
        return PredictResponse(label=label, score=score, probabilities=probs)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"prediction_error: {e}")

