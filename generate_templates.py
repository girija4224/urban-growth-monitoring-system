import os

templates = {
    "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Urban Growth Monitoring{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        .layout { display: flex; min-height: 100vh; }
        .sidebar { width: 250px; background: rgba(15,23,42,0.9); padding: 2rem 1rem; border-right: 1px solid rgba(255,255,255,0.1); }
        .sidebar a { display: block; padding: 0.75rem 1rem; color: #cbd5e1; text-decoration: none; border-radius: 0.5rem; margin-bottom: 0.5rem; transition: background 0.2s; }
        .sidebar a:hover, .sidebar a.active { background: rgba(79,172,254,0.2); color: #fff; }
        .main-content { flex: 1; padding: 2rem; display: flex; flex-direction: column; align-items: center; }
        .full-bg { background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80') center/cover; }
        .home-overlay { background: rgba(15,23,42,0.8); width: 100%; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    </style>
</head>
<body class="{% block body_class %}{% endblock %}">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div style="position: absolute; top: 1rem; right: 1rem; z-index: 100;">
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    {% block layout %}
    {% endblock %}
</body>
</html>""",

    "home.html": """{% extends "base.html" %}
{% block body_class %}full-bg{% endblock %}
{% block layout %}
<div class="home-overlay">
    <div style="text-align: center; max-width: 800px; padding: 2rem;">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">AI/ML Based Urban Growth Monitoring</h1>
        <p style="font-size: 1.2rem; color: #e2e8f0; margin-bottom: 3rem;">Urban Growth Detection using Remote Sensing Images and Deep Learning</p>
        
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
            <a href="{{ url_for('signup') }}" class="btn">User Sign Up</a>
            <a href="{{ url_for('login') }}" class="btn btn-secondary">User Sign In</a>
            <a href="{{ url_for('admin_login') }}" class="btn btn-secondary">Admin Login</a>
        </div>
    </div>
</div>
{% endblock %}""",

    "login.html": """{% extends "base.html" %}
{% block layout %}
<div class="main-content" style="justify-content: center;">
    <div class="card">
        <h2>User Login</h2>
        <form action="{{ url_for('login') }}" method="POST">
            <div class="form-group"><label>Username</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Password</label><input type="password" name="password" required></div>
            <button type="submit" class="btn">Login</button>
        </form>
        <p style="text-align: center; margin-top: 1rem;">Don't have an account? <a href="{{ url_for('signup') }}">Sign Up</a></p>
    </div>
</div>
{% endblock %}""",

    "admin_login.html": """{% extends "base.html" %}
{% block layout %}
<div class="main-content" style="justify-content: center;">
    <div class="card">
        <h2>Admin Login</h2>
        <form action="{{ url_for('admin_login') }}" method="POST">
            <div class="form-group"><label>Username</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Password</label><input type="password" name="password" required></div>
            <button type="submit" class="btn">Login</button>
        </form>
    </div>
</div>
{% endblock %}""",

    "signup.html": """{% extends "base.html" %}
{% block layout %}
<div class="main-content" style="justify-content: center;">
    <div class="card" style="max-width: 600px;">
        <h2>User Registration</h2>
        <form action="{{ url_for('signup') }}" method="POST">
            <div class="form-group"><label>Full Name</label><input type="text" name="name" pattern="[a-zA-Z ]+" required title="Alphabets only"></div>
            <div class="form-group"><label>Username</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Email ID (Only Gmail)</label><input type="email" name="email" pattern=".+@gmail\.com" required></div>
            <div class="form-group"><label>Phone Number (+91)</label><input type="tel" name="phone" pattern="\+91[0-9]{10}" placeholder="+91..." required></div>
            <div class="form-group"><label>Password</label><input type="password" name="password" required></div>
            <div class="form-group"><label>Confirm Password</label><input type="password" name="confirm_password" required></div>
            <button type="submit" class="btn">Submit</button>
        </form>
        <p style="text-align: center; margin-top: 1rem;">Already have an account? <a href="{{ url_for('login') }}">Sign In</a></p>
    </div>
</div>
{% endblock %}""",

    "user_sidebar.html": """
<div class="sidebar">
    <h3 style="color: white; margin-bottom: 2rem; font-size: 1.2rem; text-align: center;">User Menu</h3>
    <a href="{{ url_for('user_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('preprocessing') }}">Preprocessing</a>
    <a href="{{ url_for('visualization') }}">Visualization</a>
    <a href="{{ url_for('prediction') }}">Prediction</a>
    <a href="{{ url_for('result') }}">Result</a>
    <a href="{{ url_for('logout') }}" style="margin-top: auto; color: #ef4444;">Logout</a>
</div>""",

    "user_dashboard.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
            <h2>Welcome {{ session.user }}</h2>
            <p style="color: #cbd5e1; margin-bottom: 2rem;">Today's Date: {{ date }}</p>
            
            <form action="{{ url_for('user_dashboard') }}" method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label>Load Model</label>
                    <select name="model_file" required>
                        <option value="CNN">CNN</option>
                        <option value="CNN + Dense">CNN + Dense</option>
                        <option value="VGG16">VGG16</option>
                        <option value="VGG19">VGG19</option>
                        <option value="ResNet50">ResNet50</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Browse Input Remote Sensing Image</label>
                    <input type="file" name="image" accept="image/*" required style="padding: 1rem; border: 1px dashed #4facfe;">
                </div>
                <button type="submit" class="btn">Submit & Preprocess</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}""",

    "preprocessing.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
            <h2>Input Image Preprocessing</h2>
            <div style="display: flex; gap: 2rem; margin-top: 2rem;">
                <div style="flex: 1; text-align: center;">
                    <p style="margin-bottom: 1rem;">Original Image</p>
                    <img src="{{ image_path }}" style="max-width: 100%; border-radius: 0.5rem;">
                </div>
                <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 0.5rem;">
                    <h4 style="margin-bottom: 1rem; color: #4facfe;">Display Information</h4>
                    <ul style="list-style: none; color: #cbd5e1; line-height: 2;">
                        <li><strong>Original Size:</strong> {{ shapes.original[0] }}x{{ shapes.original[1] }}</li>
                        <li><strong>Resized Size:</strong> {{ shapes.resized[0] }}x{{ shapes.resized[1] }}</li>
                        <li><strong>Channels:</strong> RGB (3)</li>
                        <li><strong>Normalized:</strong> Yes (0 to 1)</li>
                    </ul>
                    <a href="{{ url_for('visualization') }}" class="btn" style="margin-top: 2rem;">Proceed to Visualization</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "visualization.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 1000px; width: 100%;">
            <h2>Image Visualization</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 2rem;">
                <div>
                    <h4 style="text-align: center; margin-bottom: 0.5rem;">1. Class Distribution Context</h4>
                    <img src="{{ url_for('static', filename='graphs/class_distribution.png') }}" style="width: 100%; border-radius: 0.5rem;">
                </div>
                <div>
                    <h4 style="text-align: center; margin-bottom: 0.5rem;">2. RGB Histogram</h4>
                    <img src="{{ url_for('static', filename='graphs/rgb_histogram.png') }}" style="width: 100%; border-radius: 0.5rem;">
                </div>
                <div>
                    <h4 style="text-align: center; margin-bottom: 0.5rem;">3. Pixel Intensity Histogram</h4>
                    <img src="{{ url_for('static', filename='graphs/pixel_intensity.png') }}" style="width: 100%; border-radius: 0.5rem;">
                </div>
                <div>
                    <h4 style="text-align: center; margin-bottom: 0.5rem;">4. Image Pixel Distribution</h4>
                    <img src="{{ url_for('static', filename='graphs/pixel_distribution.png') }}" style="width: 100%; border-radius: 0.5rem;">
                </div>
            </div>
            <div style="text-align: center; margin-top: 2rem;">
                <a href="{{ url_for('prediction') }}" class="btn">Proceed to Prediction</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "prediction.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content" style="justify-content: center;">
        <div class="card" style="text-align: center; max-width: 600px;">
            <h2>Model Comparison & Prediction</h2>
            <div style="margin: 2rem 0;">
                <div style="width: 50px; height: 50px; border: 5px solid #4facfe; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                <style>@keyframes spin { 100% { transform: rotate(360deg); } }</style>
                <p style="margin-top: 1rem; color: #cbd5e1;">Comparing Image...</p>
                <p style="color: #cbd5e1;">Generating Prediction & Confidence Score...</p>
            </div>
            <!-- Auto-redirect to result page after 2 seconds to simulate processing -->
            <script>setTimeout(() => { window.location.href = "{{ url_for('result') }}"; }, 2000);</script>
        </div>
    </div>
</div>
{% endblock %}""",

    "result.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
            <h2 style="text-align: center;">Prediction Result</h2>
            <div style="display: flex; gap: 2rem; margin-top: 2rem;">
                <div style="flex: 1; text-align: center;">
                    <img src="{{ image_path }}" style="max-width: 100%; border-radius: 0.5rem; border: 2px solid #4facfe;">
                    <h3 style="margin-top: 1.5rem; color: {{ '#ef4444' if 'Detected' in result.prediction else '#22c55e' }};">{{ result.prediction }}</h3>
                </div>
                <div style="flex: 1;">
                    <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem;">
                        <p><strong>Confidence Score:</strong> {{ result.confidence }}%</p>
                        <p><strong>Model Used:</strong> {{ result.model_used }}</p>
                        <p><strong>Prediction Time:</strong> {{ result.time_taken }}</p>
                    </div>
                    <div>
                        <h4 style="color: #4facfe; margin-bottom: 0.5rem;">Suggestions</h4>
                        <div style="color: #cbd5e1; font-size: 0.9rem; margin-left: 1rem;">
                            {{ suggestions|safe }}
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem;">
                <a href="{{ url_for('download_report') }}" class="btn" style="width: auto;">Download Report</a>
                <a href="{{ url_for('user_dashboard') }}" class="btn btn-secondary" style="width: auto;">Predict Another</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "admin_sidebar.html": """
<div class="sidebar">
    <h3 style="color: white; margin-bottom: 2rem; font-size: 1.2rem; text-align: center;">Admin Menu</h3>
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('upload_dataset') }}">Upload Dataset</a>
    <a href="{{ url_for('train_model') }}">Train Models</a>
    <a href="{{ url_for('user_details') }}">View User Details</a>
    <a href="{{ url_for('logout') }}" style="margin-top: auto; color: #ef4444;">Logout</a>
</div>""",

    "admin_dashboard.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
            <h2>Admin Dashboard</h2>
            <p style="color: #cbd5e1; margin-bottom: 2rem;">Manage datasets, train models, and view users.</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <a href="{{ url_for('upload_dataset') }}" class="btn btn-secondary" style="padding: 2rem; text-align: center;">Upload Dataset & Collect Data</a>
                <a href="{{ url_for('train_model') }}" class="btn btn-secondary" style="padding: 2rem; text-align: center;">Create & Train DL Models</a>
                <a href="{{ url_for('user_details') }}" class="btn btn-secondary" style="padding: 2rem; text-align: center; grid-column: span 2;">View Registered Users</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "upload_dataset.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
            <h2>Data Collection & Preprocessing</h2>
            <form action="{{ url_for('upload_dataset') }}" method="POST">
                <div class="form-group">
                    <label>Browse Train Folder Directory Path</label>
                    <input type="text" placeholder="dataset/train/" required>
                </div>
                <div class="form-group">
                    <label>Browse Test Folder Directory Path</label>
                    <input type="text" placeholder="dataset/test/" required>
                </div>
                <button type="submit" class="btn">Simulate Data Collection</button>
            </form>
            
            <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 0.5rem; margin-top: 2rem;">
                <h4 style="color: #4facfe; margin-bottom: 1rem;">Dataset Statistics Simulation</h4>
                <ul style="list-style: none; color: #cbd5e1; line-height: 2;">
                    <li><strong>Training Images Count:</strong> 8000</li>
                    <li><strong>Testing Images Count:</strong> 2000</li>
                    <li><strong>Number of Classes:</strong> 2 (Urban, Non-Urban)</li>
                    <li><strong>Dataset Size:</strong> ~1.2 GB</li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "train_model.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
            <h2>Create & Train Deep Learning Models</h2>
            <form action="{{ url_for('train_model') }}" method="POST">
                <div class="form-group">
                    <label>Select Model to Train</label>
                    <select name="model_type" required>
                        <option value="CNN">Model 1: CNN</option>
                        <option value="CNN + Dense">Model 2: CNN + Dense</option>
                        <option value="VGG16">Model 3: VGG16</option>
                        <option value="VGG19">Model 4: VGG19</option>
                        <option value="ResNet50">Model 5: ResNet50</option>
                    </select>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group"><label>Epochs</label><input type="number" value="10" required></div>
                    <div class="form-group"><label>Batch Size</label><input type="number" value="32" required></div>
                    <div class="form-group"><label>Learning Rate</label><input type="number" step="0.001" value="0.001" required></div>
                    <div class="form-group">
                        <label>Optimizer</label>
                        <select><option>Adam</option><option>SGD</option></select>
                    </div>
                </div>
                <button type="submit" class="btn" style="margin-top: 1rem;">Start Training Simulation</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}""",

    "user_details.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 1000px; width: 100%;">
            <h2>Registered Users</h2>
            <div style="overflow-x: auto; margin-top: 1.5rem;">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th style="padding: 1rem; border-bottom: 1px solid #cbd5e1; color: #4facfe;">Name</th>
                            <th style="padding: 1rem; border-bottom: 1px solid #cbd5e1; color: #4facfe;">Username</th>
                            <th style="padding: 1rem; border-bottom: 1px solid #cbd5e1; color: #4facfe;">Email</th>
                            <th style="padding: 1rem; border-bottom: 1px solid #cbd5e1; color: #4facfe;">Phone</th>
                            <th style="padding: 1rem; border-bottom: 1px solid #cbd5e1; color: #4facfe;">Registration Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                        <tr>
                            <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">{{ user[0] }}</td>
                            <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">{{ user[1] }}</td>
                            <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">{{ user[2] }}</td>
                            <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">{{ user[3] }}</td>
                            <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1);">{{ user[4] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div style="margin-top: 2rem; text-align: right;">
                <a href="{{ url_for('admin_dashboard') }}" class="btn btn-secondary" style="width: auto;">Return to Admin Dashboard</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
}

os.makedirs('templates', exist_ok=True)
for name, content in templates.items():
    with open(f'templates/{name}', 'w', encoding='utf-8') as f:
        f.write(content)

print("Templates generated successfully.")
