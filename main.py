from fastapi import FastAPI, HTTPException
from datetime import date
from dateutil.relativedelta import relativedelta

app = FastAPI(
    title="Age-Based Feature Gating API",
    description="Determines whether a feature should be enabled for a child based on age and region.",
    version="1.0.0"
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
    }
}

AGE_BANDS = [
    (0, 4, "0-4"),
    (5, 7, "5-7"),
    (8, 12, "8-12"),
    (13, 120, "13+")
]

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
    return {"status": "ok"}

@app.post("/age-gate/check")
def age_gate_check(payload: dict):
    try:
        dob = date.fromisoformat(payload["child_dob"])
        region = payload["region"]
        feature = payload["feature"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing required fields")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    age = calculate_age(dob)
    age_band = get_age_band(age)

    region_rules = RULES.get(region)
    if not region_rules:
        raise HTTPException(status_code=400, detail="Unsupported region")

    min_age = region_rules.get(feature)
    if min_age is None:
        raise HTTPException(status_code=400, detail="Unsupported feature")

    allowed = age >= min_age

    response = {
        "allowed": allowed,
        "reason_code": "AGE_RESTRICTED" if not allowed else "ALLOWED",
        "reason": (
            f"{feature} is restricted for children under {min_age} in {region}"
            if not allowed else
            f"{feature} is allowed for this age group"
        ),
        "age": age,
        "age_band": age_band,
        "next_eligible_date": (
            dob.replace(year=dob.year + min_age).isoformat()
            if not allowed else None
        ),
        "disclaimer": "This response provides general guidance only and does not constitute legal advice."
    }

    return response
