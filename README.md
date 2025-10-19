# Dynamic Profile Endpoint 
A RESTful Flask API that returns users information and random cat facts fetched from the Cat Facts API.

## Features
- GET endpoint at '/me' that returns user info with a random cat fact
- Error handling for API failures with fallbacck messages
- Rate limit to prevent abuse
- CORS support for cross-origin requests
- Comprehensive logging for debugging

## Tech Stack
**Backend:** Flask (Python)
**API:** Cat Facts API (https://catfact.ninja/fact)
**Hosting:** Railway (https://intelligent-commitment-production.up.railway.app/me)

## Prerequisites
- Python 3.9+
- pip (Python package manager)

## Installation

### 1. Clone the repository
'''bash
git clone https:github.com/arithenshaw/dynamic-profile-endpoint.git
cd dynamic-profile-endpoint
'''

### 2. Create and activate a virtual environment
**On macOS/Linux:**
'''bash
python3 -m venv venv
source venv/bin/activate
'''

**On Windows:**
'''bash
py -m venv venv
venv\Scripts\activate
'''

### 3. Install dependencies
'''bash
pip install -r requirements.txt
'''

### 4. Run the applicaton locally
'''bash
py app.py
'''

The API will be available at 'http://localhost:5000'

## API Documentation
### GET /me
Returns user information with a random cat fact.

**Request:**
'''bash
curl http://localhost:5000/me
'''

**Response:**
'''json
{
    "status": "success",
    "user": {
        "email": "judyhenshaw01@gmail.com",
        "name": "Judy Henshaw",
        "stack": "Python/Flask"
  },
    "timestamp": timestamp,
    "fact": cat_fact
}
'''

**Status Code:**
- '200 OK' - Successful request
- '429 Too many Request' - Rate limit exceeded (10 requests per minute)

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | Latest | Web framework |
| flask-cors | Latest | CORS support |
| flask-limiter | Latest | Rate limiting
| requests | latest | HTTP requests to at Facts API |

## Testing

### Manual Testing 
Test the endpoint with curl:
'''bash
_# Test basic request_
curl http://localhost:5000/me

_# Test with verbose output to see headers_
curl -i http://localhost:5000/me

_# Test rate limiting (run this 11+ times quickly)_
for i in {1..15}; do curl http://localhost:5000/me; done

### Expected Response
- Status Code: `200`
- Content-Type: `application/json`
- All required fields present: `status`, `user`, `timestamp`, `fact`
- `user` object contains: `email`, `name`, `stack`
- `timestamp` is in ISO 8601 format

## Error Handling

The API handles the following errors gracefully:

- **Timeout:** If the Cat Facts API takes too long, returns error message
- **Connection Error:** If unable to connect to Cat Facts API, returns error message
- **HTTP Error:** If Cat Facts API returns an error status, returns error message
- **Rate Limit:** Returns `429` status code if rate limit exceeded

## Logging

Logs are output to the console and include:
- Request timestamps
- API call status
- Error messages and warnings
- Rate limit events

