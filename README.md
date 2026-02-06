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

### POST /age-gate/check
### POST /age-gate/check-bulk

Determines whether a user meets a minimum age requirement.


## Request

### Headers

Content-Type: application/json

### Body Parameters

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


## Disclaimer

This API provides age-based eligibility logic only.
It does not perform identity verification or guarantee legal compliance.

You are responsible for ensuring your application meets all applicable laws and regulations.


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