import functions_framework
from flask import jsonify, Flask
import os

app = Flask(__name__)

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function to return available appointment times."""
    # Only allow POST requests
    if request.method != 'POST':
        return jsonify({'error': 'Only POST requests are accepted'}), 405
    
    try:
        request_json = request.get_json(silent=True)
        
        if not request_json or 'day' not in request_json:
            return jsonify({'error': 'Day parameter is required'}), 400
        
        day = request_json['day'].lower()
        
        availability = {
            'monday': ['9:00-11:00'],
            'tuesday': ['10:00-13:00'],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []
        }
        
        times = availability.get(day, [])
        
        return jsonify({
            'day': day,
            'available_times': times
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# This is only needed when running locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))