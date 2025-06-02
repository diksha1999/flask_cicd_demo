from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from OpenShift CI/CD!',
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'timestamp': datetime.datetime.now().isoformat(),
        'environment': os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/version')
def version():
    return jsonify({
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'build': os.getenv('BUILD_NUMBER', 'local')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)