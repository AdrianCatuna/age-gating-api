from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date
from dateutil.relativedelta import relativedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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
    "US": {  # United States - COPPA
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 13
    },
    "CA": {  # Canada - PIPEDA
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 13
    },
    "GB": {  # United Kingdom - Age Appropriate Design Code
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 18,  # Stricter for location
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 13
    },
    "AU": {  # Australia - Privacy Act
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 13
    },
    "DE": {  # Germany - GDPR (stricter interpretation)
        "free_chat": 16,
        "user_generated_content": 16,
        "location_sharing": 16,
        "voice_recording": 16,
        "image_upload": 16,
        "ai_chat": 16,
        "push_notifications": 14,
        "personalized_ads": 16
    },
    "FR": {  # France - GDPR
        "free_chat": 15,
        "user_generated_content": 15,
        "location_sharing": 15,
        "voice_recording": 15,
        "image_upload": 15,
        "ai_chat": 15,
        "push_notifications": 13,
        "personalized_ads": 15
    },
    "JP": {  # Japan - Act on Protection of Personal Information
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 16,
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 16
    },
    "IN": {  # India - Digital Personal Data Protection Act
        "free_chat": 18,
        "user_generated_content": 18,
        "location_sharing": 18,
        "voice_recording": 18,
        "image_upload": 18,
        "ai_chat": 18,
        "push_notifications": 13,
        "personalized_ads": 18
    },
    "BR": {  # Brazil - LGPD
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 18,  # Stricter for location data
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 18  # Requires adult consent
    },
    "MX": {  # Mexico - Federal Law on Protection of Personal Data
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 18,
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 18
    },
    "CN": {  # China - Personal Information Protection Law
        "free_chat": 14,
        "user_generated_content": 14,
        "location_sharing": 14,
        "voice_recording": 14,
        "image_upload": 14,
        "ai_chat": 14,
        "push_notifications": 14,
        "personalized_ads": 14
    },
    "KR": {  # South Korea - Personal Information Protection Act
        "free_chat": 14,
        "user_generated_content": 14,
        "location_sharing": 14,
        "voice_recording": 14,
        "image_upload": 14,
        "ai_chat": 14,
        "push_notifications": 14,
        "personalized_ads": 14
    },
    "ZA": {  # South Africa - POPIA
        "free_chat": 18,
        "user_generated_content": 18,
        "location_sharing": 18,
        "voice_recording": 18,
        "image_upload": 18,
        "ai_chat": 18,
        "push_notifications": 13,
        "personalized_ads": 18
    },
    # EU Countries with GDPR variations
    "IT": {  # Italy - GDPR
        "free_chat": 14,
        "user_generated_content": 14,
        "location_sharing": 14,
        "voice_recording": 14,
        "image_upload": 14,
        "ai_chat": 14,
        "push_notifications": 13,
        "personalized_ads": 14
    },
    "ES": {  # Spain - GDPR
        "free_chat": 14,
        "user_generated_content": 14,
        "location_sharing": 14,
        "voice_recording": 14,
        "image_upload": 14,
        "ai_chat": 14,
        "push_notifications": 13,
        "personalized_ads": 14
    },
    "NL": {  # Netherlands - GDPR
        "free_chat": 16,
        "user_generated_content": 16,
        "location_sharing": 16,
        "voice_recording": 16,
        "image_upload": 16,
        "ai_chat": 16,
        "push_notifications": 13,
        "personalized_ads": 16
    },
    "SE": {  # Sweden - GDPR
        "free_chat": 13,
        "user_generated_content": 13,
        "location_sharing": 13,
        "voice_recording": 13,
        "image_upload": 13,
        "ai_chat": 13,
        "push_notifications": 13,
        "personalized_ads": 13
    },
    "PL": {  # Poland - GDPR
        "free_chat": 16,
        "user_generated_content": 16,
        "location_sharing": 16,
        "voice_recording": 16,
        "image_upload": 16,
        "ai_chat": 16,
        "push_notifications": 13,
        "personalized_ads": 16
    },
}

# Default rules for any other region (conservative approach)
DEFAULT_RULES = {
    "free_chat": 13,
    "user_generated_content": 13,
    "location_sharing": 13,
    "voice_recording": 13,
    "image_upload": 13,
    "ai_chat": 13,
    "push_notifications": 13,
    "personalized_ads": 13
}

# ------------------------
# REGION METADATA
# ------------------------
REGION_METADATA = {
    "US": {
        "name": "United States",
        "primary_regulation": "COPPA (Children's Online Privacy Protection Act)",
        "general_age_threshold": 13,
        "notable_exceptions": {},
        "description": "Federal law requiring parental consent for collection of personal information from children under 13."
    },
    "CA": {
        "name": "Canada",
        "primary_regulation": "PIPEDA (Personal Information Protection and Electronic Documents Act)",
        "general_age_threshold": 13,
        "notable_exceptions": {},
        "description": "Federal privacy law with provincial variations for data collection from minors."
    },
    "GB": {
        "name": "United Kingdom",
        "primary_regulation": "Age Appropriate Design Code (Children's Code)",
        "general_age_threshold": 13,
        "notable_exceptions": {"location_sharing": 18},
        "description": "ICO code requiring high privacy standards for services likely to be accessed by children under 18."
    },
    "AU": {
        "name": "Australia",
        "primary_regulation": "Privacy Act 1988",
        "general_age_threshold": 13,
        "notable_exceptions": {},
        "description": "Australian privacy law with specific protections for children's personal information."
    },
    "DE": {
        "name": "Germany",
        "primary_regulation": "GDPR + German Federal Data Protection Act",
        "general_age_threshold": 16,
        "notable_exceptions": {},
        "description": "Strict interpretation of GDPR requiring age 16 for consent to data processing."
    },
    "FR": {
        "name": "France",
        "primary_regulation": "GDPR (French implementation)",
        "general_age_threshold": 15,
        "notable_exceptions": {},
        "description": "France set the digital consent age at 15 under GDPR."
    },
    "IT": {
        "name": "Italy",
        "primary_regulation": "GDPR (Italian implementation)",
        "general_age_threshold": 14,
        "notable_exceptions": {},
        "description": "Italy set the digital consent age at 14 under GDPR."
    },
    "ES": {
        "name": "Spain",
        "primary_regulation": "GDPR (Spanish implementation)",
        "general_age_threshold": 14,
        "notable_exceptions": {},
        "description": "Spain set the digital consent age at 14 under GDPR."
    },
    "NL": {
        "name": "Netherlands",
        "primary_regulation": "GDPR (Dutch implementation)",
        "general_age_threshold": 16,
        "notable_exceptions": {},
        "description": "Netherlands requires age 16 for consent to data processing under GDPR."
    },
    "PL": {
        "name": "Poland",
        "primary_regulation": "GDPR (Polish implementation)",
        "general_age_threshold": 16,
        "notable_exceptions": {},
        "description": "Poland requires age 16 for consent to data processing under GDPR."
    },
    "SE": {
        "name": "Sweden",
        "primary_regulation": "GDPR (Swedish implementation)",
        "general_age_threshold": 13,
        "notable_exceptions": {},
        "description": "Sweden set the digital consent age at 13 under GDPR."
    },
    "JP": {
        "name": "Japan",
        "primary_regulation": "Act on Protection of Personal Information (APPI)",
        "general_age_threshold": 13,
        "notable_exceptions": {"location_sharing": 16, "personalized_ads": 16},
        "description": "Japanese privacy law with enhanced protections for location data and behavioral advertising."
    },
    "IN": {
        "name": "India",
        "primary_regulation": "Digital Personal Data Protection Act 2023",
        "general_age_threshold": 18,
        "notable_exceptions": {},
        "description": "Verifiable parental consent required for processing data of children under 18."
    },
    "BR": {
        "name": "Brazil",
        "primary_regulation": "LGPD (Lei Geral de Proteção de Dados)",
        "general_age_threshold": 13,
        "notable_exceptions": {"location_sharing": 18, "personalized_ads": 18},
        "description": "Brazilian data protection law requiring parental consent for minors, with stricter rules for location and advertising data."
    },
    "MX": {
        "name": "Mexico",
        "primary_regulation": "Federal Law on Protection of Personal Data",
        "general_age_threshold": 13,
        "notable_exceptions": {"location_sharing": 18, "personalized_ads": 18},
        "description": "Mexican privacy law with enhanced protections for sensitive data like location and advertising."
    },
    "CN": {
        "name": "China",
        "primary_regulation": "Personal Information Protection Law (PIPL)",
        "general_age_threshold": 14,
        "notable_exceptions": {},
        "description": "Parental consent required for processing personal information of minors under 14."
    },
    "KR": {
        "name": "South Korea",
        "primary_regulation": "Personal Information Protection Act (PIPA)",
        "general_age_threshold": 14,
        "notable_exceptions": {},
        "description": "Parental consent required for children under 14, with strict age verification requirements."
    },
    "ZA": {
        "name": "South Africa",
        "primary_regulation": "POPIA (Protection of Personal Information Act)",
        "general_age_threshold": 18,
        "notable_exceptions": {},
        "description": "Very protective approach considering anyone under 18 a child requiring consent."
    }
}

# Age bands
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

    @model_validator(mode="before")
    def check_dob_or_age(cls, values):
        dob = values.get("child_dob")
        age = values.get("age")
        if not dob and age is None:
            raise ValueError("Either 'child_dob' or 'age' must be provided.")
        return values

class AgeGateResponse(BaseModel):
    allowed: bool
    reason_code: str
    reason: str
    age: int
    age_band: str
    region: str
    next_eligible_date: Optional[str]
    disclaimer: str

class BulkAgeGateRequest(BaseModel):
    child_dob: Optional[date] = Field(None, description="Child's date of birth in YYYY-MM-DD format", example="2018-06-12")
    age: Optional[int] = Field(None, description="Child's age in years", example=7)
    region: str = Field(..., description="Country code, e.g., US", example="US")
    features: list[str] = Field(..., description="List of features to check access for", example=["free_chat", "ai_chat", "voice_recording"])

    @model_validator(mode="before")
    def check_dob_or_age(cls, values):
        dob = values.get("child_dob")
        age = values.get("age")
        if not dob and age is None:
            raise ValueError("Either 'child_dob' or 'age' must be provided.")
        return values

class FeatureResult(BaseModel):
    feature: str
    allowed: bool
    reason_code: str
    reason: str
    min_age_required: int
    next_eligible_date: Optional[str]

class BulkAgeGateResponse(BaseModel):
    age: int
    age_band: str
    region: str
    results: list[FeatureResult]
    summary: dict  # e.g., {"allowed": 3, "restricted": 5}
    disclaimer: str

class RegionInfo(BaseModel):
    code: str
    name: str
    primary_regulation: str
    general_age_threshold: int
    notable_exceptions: Optional[dict] = None
    description: str

class RegionsResponse(BaseModel):
    total_regions: int
    regions: list[RegionInfo]
    default_rules: dict
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
@app.head("/health")
def health_check():
    return {"status": "ok"}


@app.post("/age-gate/check", response_model=AgeGateResponse)
@limiter.limit("40/minute")
def age_gate_check(payload: AgeGateRequest, request: Request):
    # Determine age and DOB
    if payload.child_dob:
        age = calculate_age(payload.child_dob)
        dob = payload.child_dob
    else:
        age = payload.age
        today = date.today()
        dob = date(today.year - age, today.month, today.day)

    # Optional: verify consistency if both provided
    if payload.child_dob and payload.age is not None:
        calculated_age = calculate_age(payload.child_dob)
        if payload.age != calculated_age:
            raise HTTPException(
                status_code=400,
                detail=f"Provided age {payload.age} does not match date of birth (calculated age {calculated_age})"
            )

    region = payload.region
    feature = payload.feature

    # Get region rules (default if region not listed)
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
        age_band=get_age_band(age),
        region=region,
        next_eligible_date=(dob.replace(year=dob.year + min_age).isoformat()
                            if not allowed else None),
        disclaimer="This response provides general guidance only and does not constitute legal advice."
    )

    return response

@app.post("/age-gate/check-bulk", response_model=BulkAgeGateResponse)
@limiter.limit("40/minute")  
def age_gate_check_bulk(payload: BulkAgeGateRequest, request: Request):
    # Determine age and DOB (same logic as single check)
    if payload.child_dob:
        age = calculate_age(payload.child_dob)
        dob = payload.child_dob
    else:
        age = payload.age
        today = date.today()
        dob = date(today.year - age, today.month, today.day)

    # Optional: verify consistency if both provided
    if payload.child_dob and payload.age is not None:
        calculated_age = calculate_age(payload.child_dob)
        if payload.age != calculated_age:
            raise HTTPException(
                status_code=400,
                detail=f"Provided age {payload.age} does not match date of birth (calculated age {calculated_age})"
            )

    region = payload.region
    features = payload.features

    # Get region rules
    region_rules = RULES.get(region, DEFAULT_RULES)

    # Check each feature
    results = []
    allowed_count = 0
    restricted_count = 0

    for feature in features:
        min_age = region_rules.get(feature)
        
        if min_age is None:
            # Skip unsupported features or add to errors
            continue
        
        allowed = age >= min_age
        
        if allowed:
            allowed_count += 1
        else:
            restricted_count += 1

        results.append(FeatureResult(
            feature=feature,
            allowed=allowed,
            reason_code="ALLOWED" if allowed else "AGE_RESTRICTED",
            reason=(
                f"{feature} is allowed for this age group"
                if allowed else
                f"{feature} is restricted for children under {min_age} in {region}"
            ),
            min_age_required=min_age,
            next_eligible_date=(
                dob.replace(year=dob.year + min_age).isoformat()
                if not allowed else None
            )
        ))

    # Prepare response
    response = BulkAgeGateResponse(
        age=age,
        age_band=get_age_band(age),
        region=region,
        results=results,
        summary={
            "total_features_checked": len(results),
            "allowed": allowed_count,
            "restricted": restricted_count
        },
        disclaimer="This response provides general guidance only and does not constitute legal advice."
    )

    return response
    
@app.get("/regions", response_model=RegionsResponse)
def list_regions():
    """
    List all supported regions with their privacy regulations and age thresholds.
    """
    regions_list = []
    
    for code, metadata in REGION_METADATA.items():
        regions_list.append(RegionInfo(
            code=code,
            name=metadata["name"],
            primary_regulation=metadata["primary_regulation"],
            general_age_threshold=metadata["general_age_threshold"],
            notable_exceptions=metadata.get("notable_exceptions"),
            description=metadata["description"]
        ))
    
    # Sort by region code
    regions_list.sort(key=lambda x: x.code)
    
    response = RegionsResponse(
        total_regions=len(regions_list),
        regions=regions_list,
        default_rules=DEFAULT_RULES,
        disclaimer="Region rules are based on common interpretations of privacy laws as of 2025. Always consult legal counsel for compliance requirements."
    )
    
    return response 