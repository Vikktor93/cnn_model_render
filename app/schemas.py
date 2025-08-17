from typing import Optional, Dict
from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict

class PredictRequest(BaseModel):
    image_url: Optional[HttpUrl] = None
    image_b64: Optional[str] = None
    model_config = ConfigDict(extra="forbid")

    @field_validator("image_b64")
    @classmethod
    def strip_b64(cls, v):
        if v is not None:
            return v.strip()
        return v

    @classmethod
    def model_validate_request(cls, data):
        obj = cls(**data)
        if (obj.image_url is None) == (obj.image_b64 is None):
            raise ValueError("Debes enviar exactamente uno: 'image_url' o 'image_b64'")
        return obj

class PredictResponse(BaseModel):
    label: str
    score: float
    probabilities: Dict[str, float]

class ErrorResponse(BaseModel):
    detail: str
