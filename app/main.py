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
def run_script():
    try:
        result = subprocess.run(['python', "-u", 'app/split_flac.py'], capture_output=True, text=True)
        return f"Script output:\n{result.stdout}\n\n{result.stderr}"
    except Exception as e:
        return str(e), 500
