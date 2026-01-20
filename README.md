# Age Gating API

A lightweight, developer-friendly API that helps applications determine whether a user meets minimum age requirements for restricted content, features, or parental controls.

Designed for apps and services targeting families, children, and compliance-sensitive platforms.


## Features

- Simple age eligibility checks
- Works for COPPA, app feature gating, and content restrictions
- Developer-friendly JSON requests and responses
- Built with FastAPI (high performance, auto-generated docs)
- Rate-limited for fair usage
- Ready for RapidAPI monetization


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
age | int | Yes | User’s age
minimum_age | int | Yes | Required minimum age

### Example Request

```json
{
  "age": 10,
  "minimum_age": 13
}
```


## Response

### Success Response (200)

```json
{
  "allowed": false,
  "age": 10,
  "minimum_age": 13,
  "reason": "User does not meet the minimum age requirement."
}
```

### Allowed Example

```json
{
  "allowed": true,
  "age": 16,
  "minimum_age": 13,
  "reason": "User meets the minimum age requirement."
}
```


## Error Responses

### Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "field required",
      "type": "value_error.missing"
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
curl -X POST https://age-gating-api.onrender.com/age-gate/check \
  -H "Content-Type: application/json" \
  -d '{"age":12,"minimum_age":13}'
```

### JavaScript (Fetch)

```javascript
fetch("https://age-gating-api.onrender.com/age-gate/check", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    age: 12,
    minimum_age: 13
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Python

```python
import requests

url = "https://age-gating-api.onrender.com/age-gate/check"
payload = {
    "age": 12,
    "minimum_age": 13
}

response = requests.post(url, json=payload)
print(response.json())
```


## Rate Limiting

Plan | Limit 
----- | ----
Free | 30 requests per minute
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