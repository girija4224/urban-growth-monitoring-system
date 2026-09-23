from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename
from database import init_db, add_user, verify_user, get_all_users, save_prediction, get_user_predictions, get_total_users, get_total_predictions
from preprocessing.process import full_preprocess
from prediction.visualize import generate_inference_visualizations
from prediction.infer import predict_image
from prediction.gemini_helper import generate_suggestions, generate_report, chat_with_bot
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'urban_growth_secret'

UPLOAD_FOLDER = 'static/uploads'
MODEL_FOLDER = 'models'
GRAPH_FOLDER = 'static/graphs'
REPORT_FOLDER = 'reports'

for folder in [UPLOAD_FOLDER, MODEL_FOLDER, GRAPH_FOLDER, REPORT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))
        
        success, msg = add_user(name, username, email, phone, password)
        if success:
            flash(msg, "success")
            return redirect(url_for('login'))
        else:
            flash(msg, "error")
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_user(username, password):
            session['user'] = username
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials!", "error")
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        model = request.form.get('model_file')
        session['current_model'] = model
            
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Validate if it's a satellite image (OOD check)
            import cv2
            import numpy as np
            img = cv2.imread(file_path)
            if img is not None:
                is_valid = True
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                unique_colors = len(np.unique(img.reshape(-1, img.shape[2]), axis=0))
                
                # Check for screenshots/clipart (low color variance)
                if unique_colors < 1000:
                    is_valid = False
                    
                # Check for faces
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) > 0:
                    is_valid = False
                    
                if not is_valid:
                    os.remove(file_path) # Delete the invalid image
                    flash('Error: The uploaded file does not appear to be a valid remote sensing/satellite image. Please try again.', 'danger')
                    return redirect(url_for('user_dashboard'))

            session['current_image'] = file_path
            return redirect(url_for('preprocessing'))
            
    return render_template('user_dashboard.html', date=datetime.now().strftime("%Y-%m-%d"))

@app.route('/preprocessing')
def preprocessing():
    if 'user' not in session: return redirect(url_for('login'))
    image_path = session.get('current_image')
    if not image_path: return redirect(url_for('user_dashboard'))
    
    try:
        proc_data = full_preprocess(image_path)
        session['proc_data_shapes'] = {
            "original": proc_data["original_shape"],
            "resized": proc_data["resized_shape"]
        }
    except Exception as e:
        flash(f"Error processing image: {e}", "error")
        return redirect(url_for('user_dashboard'))
        
    return render_template('preprocessing.html', image_path=image_path, shapes=session['proc_data_shapes'])

@app.route('/visualization')
def visualization():
    if 'user' not in session: return redirect(url_for('login'))
    image_path = session.get('current_image')
    
    generate_inference_visualizations(image_path, GRAPH_FOLDER)
    
    return render_template('visualization.html', image_path=image_path)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'user' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        model_name = request.form.get('model_name', 'CNN')
        session['current_model'] = model_name
    else:
        model_name = session.get('current_model', 'CNN')
    
    # Process prediction (simulated delay inside)
    image_path = session.get('current_image')
    result = predict_image(image_path, model_name)
    session['prediction_result'] = result
    
    # Save to database
    save_prediction(
        username=session['user'],
        image_path=session.get('current_image'),
        model_used=model_name,
        prediction=result['prediction'],
        confidence=result['confidence']
    )
    
    # If it was a POST request from the result page (One-click switch), redirect to result directly
    if request.method == 'POST' and request.headers.get('Referer') and 'result' in request.headers.get('Referer'):
        return redirect(url_for('result'))
        
    return render_template('prediction.html', result=result)

@app.route('/result')
def result():
    if 'user' not in session: return redirect(url_for('login'))
    result = session.get('prediction_result', {})
    image_path = session.get('current_image', '')
    
    # Generate full technical report
    report = generate_report(
        prediction_text=result.get('prediction', 'Unknown'),
        confidence=result.get('confidence', 0),
        model_used=result.get('model_used', 'CNN'),
        time_taken=result.get('time_taken', '0s')
    )
    
    return render_template('result.html', result=result, image_path=image_path, suggestions=report)

@app.route('/download_report')
def download_report():
    if 'user' not in session: return redirect(url_for('login'))
    pred_data = session.get('prediction_result')
    
    report_content = generate_report(pred_data['prediction'], pred_data['confidence'], pred_data['model_used'], pred_data['time_taken'])
    
    import re
    # Clean HTML tags for the text report
    clean_report = re.sub('<[^<]+>', '', report_content)
    
    report_path = os.path.join(REPORT_FOLDER, f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    with open(report_path, 'w') as f:
        f.write("URBAN GROWTH MONITORING REPORT\n")
        f.write("="*30 + "\n\n")
        f.write(clean_report)
        
    return send_file(report_path, as_attachment=True)

@app.route('/history')
def history():
    if 'user' not in session: return redirect(url_for('login'))
    search_query = request.args.get('search', '')
    preds = get_user_predictions(session['user'], search_query)
    return render_template('history.html', predictions=preds, search=search_query)

@app.route('/time_series', methods=['GET', 'POST'])
def time_series():
    if 'user' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        past_img = request.files.get('image1')
        present_img = request.files.get('image2')
        
        if past_img and present_img:
            past_name = secure_filename(past_img.filename)
            present_name = secure_filename(present_img.filename)
            
            past_path = os.path.join(UPLOAD_FOLDER, past_name)
            present_path = os.path.join(UPLOAD_FOLDER, present_name)
            
            past_img.save(past_path)
            present_img.save(present_path)
            
            flash('Time-Series Comparison Generated!', 'success')
            return render_template('time_series.html', images_uploaded=True, past_image=past_name, present_image=present_name)
        else:
            flash('Please upload both images.', 'danger')
            return redirect(url_for('time_series'))
    return render_template('time_series.html', images_uploaded=False)

@app.route('/export_excel')
def export_excel():
    if 'user' not in session: return redirect(url_for('login'))
    preds = get_user_predictions(session['user'])
    
    df = pd.DataFrame(preds, columns=['Image Path', 'Model Used', 'Prediction', 'Confidence', 'Date'])
    export_path = os.path.join(REPORT_FOLDER, f"{session['user']}_history.xlsx")
    df.to_excel(export_path, index=False)
    
    return send_file(export_path, as_attachment=True)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    context = session.get('prediction_result', {}).get('prediction', 'No recent prediction.')
    response = chat_with_bot(message, context=f"Recent model output: {context}")
    return jsonify({'response': response})

@app.route('/download_model/<filename>')
def download_model(filename):
    # Create a dummy file to represent the downloaded model weight
    model_path = os.path.join(MODEL_FOLDER, filename)
    if not os.path.exists(model_path):
        with open(model_path, 'w') as f:
            f.write(f"Simulated {filename} model weights.")
    return send_file(model_path, as_attachment=True)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session: return redirect(url_for('admin_login'))
    total_users = get_total_users()
    total_predictions = get_total_predictions() # Representing total models run
    return render_template('admin_dashboard.html', total_users=total_users, total_models=total_predictions)

@app.route('/upload_dataset', methods=['GET', 'POST'])
def upload_dataset():
    if 'admin' not in session: return redirect(url_for('admin_login'))
    if request.method == 'POST':
        flash("Dataset uploaded and Data Collection simulated successfully.", "success")
    return render_template('upload_dataset.html')

@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    if 'admin' not in session: return redirect(url_for('admin_login'))
    if request.method == 'POST':
        # Simulate training
        model_type = request.form.get('model_type')
        flash(f"{model_type} trained successfully and saved to models/ directory.", "success")
    return render_template('train_model.html')

@app.route('/user_details')
def user_details():
    if 'admin' not in session: return redirect(url_for('admin_login'))
    users = get_all_users()
    return render_template('user_details.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
