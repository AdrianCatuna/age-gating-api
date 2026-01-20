from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import date
from dateutil.relativedelta import relativedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional
from pydantic import root_validator

# ------------------------
# APP INITIALIZATION
# ------------------------
app = FastAPI(
    title="Age-Based Feature Gating API",
    description="Determines whether a feature should be enabled for a child based on age and region.",
    version="1.0.0"
)

# ------------------------
# RATE LIMITER CONFIG
# ------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

# ------------------------
# RULE DEFINITIONS
# ------------------------
RULES = {
    "US": {
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "CA": {  # Canada
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "GB": {  # United Kingdom
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "AU": {  # Australia
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "DE": {  # Germany
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "FR": {  # France
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "JP": {  # Japan
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "IN": {  # India
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "BR": {  # Brazil
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "MX": {  # Mexico
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "CN": {  # China
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "KR": {  # South Korea
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    },
    "ZA": {  # South Africa
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 8,
        "image_upload": 8,
        "ai_chat": 13,
        "push_notifications": 5,
        "personalized_ads": 13
    }
}

# ------------------------
# DEFAULT RULES FOR ANY OTHER REGION
# ------------------------
DEFAULT_RULES = {
    "free_chat": 13,
    "user_generated_content": 13,
    "location_sharing": 13,
    "voice_recording": 8,
    "image_upload": 8,
    "ai_chat": 13,
    "push_notifications": 5,
    "personalized_ads": 13
}

AGE_BANDS = [
    (0, 4, "0-4"),
    (5, 7, "5-7"),
    (8, 12, "8-12"),
    (13, 120, "13+")
]

# ------------------------
# Pydantic Models
# ------------------------

class AgeGateRequest(BaseModel):
    child_dob: Optional[date] = Field(None, description="Child's date of birth in YYYY-MM-DD format", example="2018-06-12")
    age: Optional[int] = Field(None, description="Child's age in years", example=7)
    region: str = Field(..., description="Country code, e.g., US", example="US")
    feature: str = Field(..., description="Feature you want to check access for", example="free_chat")

    @root_validator
    def check_dob_or_age(cls, values):
        dob, age = values.get("child_dob"), values.get("age")
        if not dob and age is None:
            raise ValueError("Either 'child_dob' or 'age' must be provided.")
        return values


class AgeGateResponse(BaseModel):
    allowed: bool
    reason_code: str
    reason: str
    age: int
    age_band: str
    next_eligible_date: str | None
    disclaimer: str

# ------------------------
# UTILS
# ------------------------
def calculate_age(dob: date) -> int:
    return relativedelta(date.today(), dob).years

def get_age_band(age: int) -> str:
    for min_age, max_age, band in AGE_BANDS:
        if min_age <= age <= max_age:
            return band
    return "unknown"

# ------------------------
# ENDPOINTS
# ------------------------
@app.get("/health")
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

@app.post("/age-gate/check", response_model=AgeGateResponse)
@limiter.limit("10/minute")  # Limit 10 requests per minute per IP
def age_gate_check(payload: AgeGateRequest, request: Request):
    """
    Determines if a feature is allowed for a child based on age and region.
    """
    # Determine age
    if payload.child_dob:
        age = calculate_age(payload.child_dob)
        dob = payload.child_dob
    else:
        age = payload.age
        # Approximate DOB from age
        today = date.today()
        dob = date(today.year - age, today.month, today.day)

    age_band = get_age_band(age)
    region = payload.region
    feature = payload.feature

    # Validate region (fall back to default rules if region not listed)
    region_rules = RULES.get(region, DEFAULT_RULES)

    # Validate feature
    min_age = region_rules.get(feature)
    if min_age is None:
        raise HTTPException(status_code=400, detail="Unsupported feature")

    # Determine if allowed
    allowed = age >= min_age

    # Prepare response
    response = AgeGateResponse(
        allowed=allowed,
        reason_code="AGE_RESTRICTED" if not allowed else "ALLOWED",
        reason=(
            f"{feature} is restricted for children under {min_age} in {region}"
            if not allowed else
            f"{feature} is allowed for this age group"
        ),
        age=age,
        age_band=age_band,
        next_eligible_date=(dob.replace(year=dob.year + min_age).isoformat()
                            if not allowed else None),
        disclaimer="This response provides general guidance only and does not constitute legal advice."
    )

    return response

