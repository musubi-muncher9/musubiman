from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/my-project-dir')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)

# Endpoint to make the GET call
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    # Get the 'my_api_key' query parameter
    user_api_key = request.args.get('key')
    
    auth_key = os.getenv("AUTH")
    if user_api_key != auth_key:
        return jsonify({'error': 'Invalid API key'}), 401  # Unauthorized

    # Get the 'date' parameter
    date_param = request.args.get('date')
    if not date_param:
        return jsonify({'error': 'Date parameter is required'}), 400

    # Validate the date format
    try:
        parsed_date = datetime.strptime(date_param, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use yyyy-mm-dd'}), 400

    # Railway environment variable for the API URL (keep this hardcoded or use an environment variable)
    api_url = os.getenv("API_URL")

    # Make the GET request to the external API
    try:
        api_key = os.getenv("API_KEY")
        headers = {'API-Key': api_key}
        response = requests.get(api_url, headers=headers, params={'date': parsed_date})
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
