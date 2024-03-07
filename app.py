import os
from flask import Flask, render_template, request, redirect
from inference import get_prediction

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return
        img_bytes = file.read()
        prediction = get_prediction(image_bytes=img_bytes)
        return render_template('result.html', class_name=prediction)
    return render_template('index.html')

if __name__ == '__main__':
    # Disable debug mode
    app.debug = False
    # Get the port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app using Gunicorn as the WSGI server
    # Use 4 worker processes for handling requests
    # Use 0.0.0.0 as the host to listen on all public IPs
    os.system(f"gunicorn -w 4 -b 0.0.0.0:{port} app:app")
