from flask import Flask, render_template, Response, send_file
import cv2

# Initialize Flask application
app = Flask(__name__)

# Function to get frames from Jetson stream
def gen_frames():
    # Stream URL for the Jetson video feed
    stream_url = 'http://10.147.143.54:5000/video_feed'
    cap = cv2.VideoCapture(stream_url)

    while True:
        success, frame = cap.read()  # Read the frame from the video stream
        if not success:
            print("Failed to grab frame")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  # Encode the frame as a JPEG image
            if not ret:
                print("Failed to encode frame")
                break
            frame = buffer.tobytes()  # Convert to bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    # Render the main index page
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Render the dashboard page
    return render_template('dashboard.html')

@app.route('/live_feed')
def live_feed():
    # Render the live feed page
    return render_template('live_feed.html')

@app.route('/video_feed')
def video_feed():
    # Return the video stream to the front-end
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/report")
def report():
    # Render the report page
    return render_template("report.html")

@app.route("/download-report")
def download_report():
    # Ensure the file exists in static folder and is available for download
    return send_file("static/waste_report.pdf", as_attachment=True)

if __name__ == '__main__':
    # Run the Flask app on port 5001
    app.run(debug=True, host='0.0.0.0', port=5001)
