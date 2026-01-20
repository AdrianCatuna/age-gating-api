# Age Gating API

A lightweight, developer-friendly API that helps applications determine whether a user meets minimum age requirements for specific features based on region.

Available features: 
- free_chat
- user_generated_content
- location_sharing
- voice_recording
- image_upload
- ai_chat
- push_notifications, personalized_ads

Available regions:
- US

Designed for apps and services targeting families, children, and compliance-sensitive platforms.


## Features

- Simple age eligibility checks
- Works for COPPA, app feature gating, and content restrictions
- Developer-friendly JSON requests and responses
- Built with FastAPI (high performance)
- Rate-limited for fair usage


## Base URL

https://age-gating-api.onrender.com


## Endpoint Overview

### POST /age-gate/check

Determines whether a user meets a minimum age requirement.


## Request

### Headers

Content-Type: application/json

### Body Parameters

Field | Type | Required | Description
----- | ---- | -------- | -----------
child_dob| string | Yes | Child’s date of birth in YYYY-MM-DD format
region | string | Yes | ISO country code representing the child’s region (example: US)
feature | string | Yes | Feature to check eligibility for (options: free_chat, user_generated_content, location_sharing, voice_recording, image_upload, ai_chat, push_notifications, personalized_ads)

### Example Request

```json
{
  "child_dob": "2018-06-12",
  "region": "US",
  "feature": "free_chat"
}
```


## Successful Responses

### Success Response (200)

### Allowed = True Example

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
### Allowed = False Example

```json
{
  "allowed": false,
  "reason_code": "AGE_RESTRICTED",
  "reason": "free_chat is restricted for children under 13 in US",
  "age": 7,
  "age_band": "5-7",
  "next_eligible_date": "2031-06-12",
  "disclaimer": "This response provides general guidance only and does not constitute legal advice."
}
```


## Error Responses

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

### cURL

```bash
curl -X POST "https://age-gating-api.onrender.com/age-gate/check" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_RAPIDAPI_KEY" \
-d '{
  "child_dob": "2018-06-12",
  "region": "US",
  "feature": "free_chat"
}'
```

### JavaScript (Fetch)

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
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Python

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
    "feature": "free_chat"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

```


## Rate Limiting

Plan | Limit 
----- | ----
Free | 10 requests per minute (200 max per month)
Paid (RapidAPI) | Higher limits available


## Use Cases

- Parental control apps
- Kids’ games and educational platforms
- Video streaming services
- Social platforms with age restrictions
- Feature gating inside mobile or web apps
- COPPA-adjacent compliance checks


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