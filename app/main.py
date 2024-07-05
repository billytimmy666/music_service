from flask import Blueprint
import subprocess
from flasgger import swag_from

main = Blueprint('main', __name__)

@main.route('/split_flac', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Script output',
            'schema': {
                'type': 'string'
            }
        }
    }
})
def run_split_script():
    try:
        result = subprocess.run(['python', "-u", 'app/split_flac.py'], capture_output=True, text=True)
        return f"Script output:\n{result.stdout}\n\n{result.stderr}"
    except Exception as e:
        return str(e), 500


@main.route('/flac2mp3', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Script output',
            'schema': {
                'type': 'string'
            }
        }
    }
})
def run_mp3_script():
    try:
        result = subprocess.run(['python', "-u", 'app/flac2mp3.py'], capture_output=True, text=True)
        return f"Script output:\n{result.stdout}\n\n{result.stderr}"
    except Exception as e:
        return str(e), 500
