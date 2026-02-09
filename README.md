Region-aware age verification API for compliance and child safety.

Determine whether users meet minimum age requirements for features like chat, location sharing, AI interactions, and personalized ads—based on their country's regulations.

Supports 18+ regions with rules aligned to COPPA, GDPR, LGPD, and other privacy laws. Perfect for parental control apps, educational platforms, social features, and family-friendly services.

Send age/DOB + region + feature → Get instant eligibility status with clear reason codes.

Bulk checking supported. Production-ready with rate limiting.

## Available Features

- free_chat
- user_generated_content
- location_sharing
- voice_recording
- image_upload
- ai_chat
- push_notifications
- personalized_ads


## Available Regions

Region | Code | Key Age Thresholds | Notes
------ | ---- | ------------------ | -----
United States | US | 13 | COPPA compliance
Canada | CA | 13 | PIPEDA aligned
United Kingdom | GB | 13 (location: 18) | Age Appropriate Design Code
Australia | AU | 13 | Privacy Act
Germany | DE | 16 | GDPR strict interpretation
France | FR | 15 | GDPR
Italy | IT | 14 | GDPR
Spain | ES | 14 | GDPR
Netherlands | NL | 16 | GDPR strict interpretation
Poland | PL | 16 | GDPR strict interpretation
Sweden | SE | 13 | GDPR permissive interpretation
Japan | JP | 13 (location/ads: 16) | Personal Info Protection
India | IN | 18 | Digital Personal Data Protection Act
Brazil | BR | 13 (location/ads: 18) | LGPD
Mexico | MX | 13 (location/ads: 18) | Federal Data Protection Law
China | CN | 14 | Personal Info Protection Law
South Korea | KR | 14 | Personal Info Protection Act
South Africa | ZA | 18 | POPIA (very protective)

**Default**: For unlisted regions, defaults to age 13 for all features.

## Use Cases

- Parental control apps
- Kids’ games and educational platforms
- Video streaming services
- Social platforms with age restrictions
- Feature gating inside mobile or web apps
- COPPA-adjacent compliance checks

## Base URL

https://age-gating-api.p.rapidapi.com


## Endpoints Overview

- POST /age-gate/check
    - Checks min age requirement for single feature.
- POST /age-gate/check-bulk
    - Checks min age requirement for multiple features.
- POST /age-gate/regions
    - Lists all supported regions (and additional info for each)

Determines whether a user meets a minimum age requirement.


## Request

### Headers

Content-Type: application/json

### Body Parameters
(for **check** and **check-bulk** endpoints)

Field | Type | Required | Description
----- | ---- | -------- | -----------
child_dob| date | No | Child’s date of birth in YYYY-MM-DD format (dob or age must be provided)
age | int | No | Child's age (dob or age must be provided)
region | string | Yes | ISO country code representing the child’s region (example: US)
feature (for single request) | string | Yes | Feature to check eligibility for (options: free_chat, user_generated_content, location_sharing, voice_recording, image_upload, ai_chat, push_notifications, personalized_ads)
feature (for bulk request) |  list (array) | Yes | Bulk features to check eligibility for (options: free_chat, user_generated_content, location_sharing, voice_recording, image_upload, ai_chat, push_notifications, personalized_ads)

### Example Request for single feature check

```json
{
  "child_dob": "2018-06-12",
  "age": 7,
  "region": "US",
  "feature": "free_chat"
}
```
### Example Request for bulk feature check

```json
{
  "child_dob": "2018-06-12",
  "age": 7,
  "region": "US",
  "features": ["free_chat", "ai_chat", "voice_recording", "push_notifications"]
}
```

## Successful Responses (200)

### Single Feature

```json
{
  "allowed": true,
  "reason_code": "ALLOWED",
  "reason": "free_chat is allowed for this age group",
  "age": 15,
  "age_band": "13+",
  "region":"US",
  "next_eligible_date": null,
  "disclaimer": "This response provides general guidance only and does not constitute legal advice."
}
```
### Bulk Features

```json
{
"age":7,
"age_band":"5-7",
"region":"US",
"results":[
  {"feature":"free_chat","allowed":false,"reason_code":"AGE_RESTRICTED","reason":"free_chat is restricted for children under 13 in US","min_age_required":13,"next_eligible_date":"2031-06-12"},
  {"feature":"ai_chat","allowed":false,"reason_code":"AGE_RESTRICTED","reason":"ai_chat is restricted for children under 13 in US","min_age_required":13,"next_eligible_date":"2031-06-12"},
  {"feature":"voice_recording","allowed":false,"reason_code":"AGE_RESTRICTED","reason":"voice_recording is restricted for children under 8 in US","min_age_required":8,"next_eligible_date":"2026-06-12"},
  {"feature":"push_notifications","allowed":true,"reason_code":"ALLOWED","reason":"push_notifications is allowed for this age group","min_age_required":5,"next_eligible_date":null}
],
"summary":{"total_features_checked":4,"allowed":1,"restricted":3},"disclaimer":"This response provides general guidance only and does not constitute legal advice."}
```

## Error Responses (422)

### Validation Error Example (422)

```json
{
  "detail": [
    {
      "type": "date_from_datetime_parsing",
      "loc": [
        "body",
        "child_dob"
      ],
      "msg": "Input should be a valid date or datetime, invalid datetime separator, expected `T`, `t`, `_` or space",
      "input": "2010-06-182",
      "ctx": {
        "error": "invalid datetime separator, expected `T`, `t`, `_` or space"
      }
    }
  ]
}
```

### Rate Limit Exceeded (429)

```json
{
  "detail": "Rate limit exceeded. Try again later."
}
```


## Example Usage

### cURL (bulk features request)

```bash
curl -X POST "https://age-gating-api.onrender.com/age-gate/check" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_RAPIDAPI_KEY" \
-d '{
  "child_dob": "2018-06-12",
  "region": "US",
  "features": ["free_chat", "ai_chat", "voice_recording", "push_notifications"]
}'
```

### JavaScript (Fetch) (single feature request)

```javascript
fetch("https://age-gating-api.onrender.com/age-gate/check", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": "YOUR_RAPIDAPI_KEY"
  },
  body: JSON.stringify({
    child_dob: "2018-06-12",
    region: "US",
    feature: "free_chat"
  })
})
.then(response =&gt; response.json())
.then(data =&gt; console.log(data))
.catch(error =&gt; console.error('Error:', error));
```

### Python (bulk features request)

```python
import requests

url = "https://age-gating-api.onrender.com/age-gate/check"

headers = {
    "Content-Type": "application/json",
    "x-api-key": "YOUR_RAPIDAPI_KEY"
}

payload = {
    "child_dob": "2018-06-12",
    "region": "US",
    "features": ["free_chat", "ai_chat", "voice_recording", "push_notifications"]
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

```


## Rate Limiting

Plan | Limit 
----- | ----
Free | 40 requests per minute (200 max per month)
Paid (RapidAPI) | Higher limits available

## API Documentation (Swagger)

Interactive API docs are available at:

https://age-gating-api.onrender.com/docs


## Important Legal Disclaimer

**These age thresholds are based on common interpretations of digital consent and privacy laws as of 2025.** 

- Laws vary by jurisdiction and change over time
- Some regions require parental consent for ages below the threshold
- This API provides technical guidance only, NOT legal advice
- Always consult with legal counsel for compliance requirements
- You are responsible for ensuring compliance with all applicable laws

**Parental Consent**: Many regions allow usage below the stated age WITH verified parental consent. This API does not handle consent verification.


## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic
- SlowAPI (rate limiting)
- Render (hosting)


## Support

- Open a GitHub Issue
- Contact via RapidAPI messaging


## License

MIT License