from flask import Flask, request, render_template, jsonify
from services import get_service
from config import config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    drive_link = data.get('driveLink')
    service = data.get('service', 'gdtot')
    
    # First get FilePress result to get file info
    filepress_service = get_service('filepress')
    filepress_result = filepress_service.convert_link(drive_link)
    
    # If requested service is FilePress, return its result
    if service == 'filepress':
        return jsonify(filepress_result)
    
    # For other services, get their result and add FilePress file info
    service_handler = get_service(service)
    if not service_handler:
        return jsonify({
            "success": False,
            "error": "Invalid service selected"
        })
    
    result = service_handler.convert_link(drive_link)
    
    # If FilePress was successful, add its file info to the result
    if filepress_result.get('success') and result.get('success'):
        result['details'] = filepress_result.get('details', {
            'name': 'Unknown',
            'size': 'Unknown'
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 