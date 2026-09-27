from pydantic import BaseModel, Field

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    return_left_cm: float = Field(default=0.0, ge=0)
    return_right_cm: float = Field(default=0.0, ge=0)
