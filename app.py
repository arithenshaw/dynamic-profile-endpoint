from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import requests
import logging
import os

app = Flask(__name__)

CORS(app)

limiter = Limiter(
    app = app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - %(name)s -%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/me', methods = ['GET'])
@limiter.limit("10 per minute")
def return_json():

    logger.info("GET /me request received")

    timestamp = datetime.utcnow().isoformat() + 'Z'

    try:
        logger.info(f'Attempting to fetch cat fact from {'https://catfact.ninja/fact'}')
        response = requests.get('https://catfact.ninja/fact', timeout =5)
        response.raise_for_status
        cat_data = response.json()
        cat_fact = cat_data.get('fact')
    except requests.exceptions.RequestException as e:
        cat_fact = f"Error fetching cat fact: {str(e)}"
    except requests.exceptions.HTTPError as e:
        cat_fact = f"Error: Cat Facts API returned {response.status_code}"
    except requests.exceptions.ConnectionError:
        cat_fact = "Error: Unable to connect to Cat Facts API"
    except requests.exceptions.Timeout:
        cat_fact = "Error: Cat Facts API request timed out"
    except Exception as e:
        cat_fact = "Error: Unexpected error occured"

    if not cat_fact:
        cat_fact = 'Fallback: Cat can make over 100 different sounds'

    user = {
            "status": "success",
            "user": {
                "email": "judyhenshaw01@gmail.com",
                "name": "Judy Henshaw",
                "stack": "Python/Flask"
            },
            "timestamp": timestamp,
            "fact": cat_fact
    }

    logger.info("Successfully reurning /me response")
    return jsonify(user), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f'Rate limit exceeded: {e.description}.')
    return jsonify({
        "status": "Error",
        "message": "Rate limit exceeded. Please try again later."
    }), 429

if __name__ == '__main__':
    logger.info('Starting Flask application')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)