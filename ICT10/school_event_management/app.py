import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

events = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_description = request.form['event_description']

        if 'event_image' not in request.files:
            return "No file part"
        
        file = request.files['event_image']
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            event_image = filename
            
            events.append({
                'name': event_name,
                'date': event_date,
                'description': event_description,
                'image': event_image
            })
            
            return redirect(url_for('home'))
    
    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = events[event_id]
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], event['image'])
    if not os.path.exists(image_path):
        event['image'] = 'default.jpg'  # Fallback image
    return render_template('event_details.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
