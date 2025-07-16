from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def system_info():
    # Basic environment info
    debug_mode = app.debug
    ip = request.host.split(':')[0]
    port = request.host.split(':')[1] if ':' in request.host else 'Unknown'
    flask_env = os.getenv('FLASK_ENV', 'production')

    return f"""
    <h2>Server Information Dashboard</h2>
    <ul>
        <li><b>Client IP:</b> {ip}</li>
        <li><b>Port:</b> {port}</li>
        <li><b>Environment:</b> {flask_env}</li>
        <li><b>Debug Mode:</b> {debug_mode}</li>
    </ul>
    """

@app.route('/status')
def status():
    if app.debug:
        return "<h3>✅ Running in Debug Mode</h3>"
    else:
        return "<h3>ℹ️ Running in Production Mode</h3>"

if __name__ == '__main__':
    print("🚀 Starting Server on port 8000...")
    app.run(debug=True, port=8000)
