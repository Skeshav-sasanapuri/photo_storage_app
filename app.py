from flask import Flask, render_template, request, jsonify, flash
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Back end URL
BACKEND_URL = "http://127.0.0.1:5000"  # Adjust this URL if back end runs on a different port or host


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search_photos():
    print("came here, front")
    date_taken = request.args.get('date')
    tag = request.args.get('tag')

    params = {}
    if date_taken:
        params['date_taken'] = date_taken.strip()  # Strip whitespace
    if tag:
        params['tag'] = ','.join([t.strip() for t in tag.split(',')])  # Join tags with commas

    # Request to back end API to fetch photos
    response = requests.get(f"{BACKEND_URL}/photos", params=params)

    if response.status_code == 200:
        photos = response.json()
        print(photos)
        if not photos:
            flash("No photos found matching your criteria.", "info")  # Notify user
    else:
        flash("Error fetching photos. Please try again.", "error")  # Notify user
        photos = []

    # Render the photos in the template context
    return render_template('index.html', photos=photos)


@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('files[]')  # Adjusted to get multiple files

    if files:
        # Create a dictionary for multiple files
        files_dict = [('files[]', (file.filename, file)) for file in files]
        response = requests.post(f"{BACKEND_URL}/upload", files=files_dict)
        return jsonify(response.json()), 200
    return jsonify({"error": "No file uploaded."}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Running on a different port to avoid conflicts
