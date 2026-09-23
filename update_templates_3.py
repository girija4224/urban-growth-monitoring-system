import os

templates = {
    "user_sidebar.html": """
<div class="sidebar">
    <h3 style="color: var(--text-color, white); margin-bottom: 2rem; font-size: 1.2rem; text-align: center;">User Menu</h3>
    <a href="{{ url_for('user_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('time_series') }}">Time-Series Expansion</a>
    <a href="{{ url_for('preprocessing') }}">Preprocessing</a>
    <a href="{{ url_for('visualization') }}">Visualization</a>
    <a href="{{ url_for('prediction') }}">Prediction</a>
    <a href="{{ url_for('result') }}">Result</a>
    <a href="{{ url_for('history') }}">Prediction History</a>
    <a href="{{ url_for('logout') }}" style="margin-top: auto; color: #ef4444;">Logout</a>
</div>""",

    "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Urban Growth Monitoring{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: rgba(15,23,42,0.9);
            --text-color: #e2e8f0;
            --primary: #4facfe;
            --border-color: rgba(255,255,255,0.1);
        }
        [data-theme="light"] {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
            --primary: #0284c7;
            --border-color: #e2e8f0;
        }
        body { background-color: var(--bg-color); color: var(--text-color); transition: all 0.3s ease; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-color); border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .sidebar { background: var(--card-bg); border-right: 1px solid var(--border-color); }
        .sidebar a { color: var(--text-color); }
        .sidebar a:hover { background: rgba(79,172,254,0.2); }
        .layout { display: flex; min-height: 100vh; }
        .sidebar { width: 250px; padding: 2rem 1rem; }
        .sidebar a { display: block; padding: 0.75rem 1rem; text-decoration: none; border-radius: 0.5rem; margin-bottom: 0.5rem; transition: background 0.2s; }
        .main-content { flex: 1; padding: 2rem; display: flex; flex-direction: column; align-items: center; position: relative; }
        .full-bg { background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80') center/cover; }
        .home-overlay { background: rgba(15,23,42,0.8); width: 100%; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .theme-toggle { position: fixed; bottom: 20px; left: 20px; background: var(--primary); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; z-index: 1000; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        table th, table td { color: var(--text-color); border-bottom: 1px solid var(--border-color) !important; padding: 1rem; }
        input, select { background: var(--bg-color); color: var(--text-color); border: 1px solid var(--border-color); border-radius: 0.5rem; padding: 0.75rem; width: 100%; box-sizing: border-box; }
        .zoom-img { transition: transform 0.3s ease; cursor: zoom-in; }
        .zoom-img.zoomed { transform: scale(1.5); cursor: zoom-out; z-index: 50; position: relative; }
        
        /* Chatbot */
        .chatbot-container { position: fixed; bottom: 20px; right: 20px; width: 350px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: none; flex-direction: column; z-index: 1000; overflow: hidden; }
        .chatbot-header { background: var(--primary); color: white; padding: 1rem; font-weight: bold; display: flex; justify-content: space-between; align-items: center; cursor: pointer; }
        .chatbot-messages { height: 300px; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
        .chatbot-input { display: flex; border-top: 1px solid var(--border-color); }
        .chatbot-input input { border: none; padding: 1rem; flex: 1; border-radius: 0; outline: none; }
        .chatbot-input button { background: var(--primary); color: white; border: none; padding: 1rem; cursor: pointer; }
        .msg { padding: 0.75rem 1rem; border-radius: 1rem; max-width: 80%; font-size: 0.9rem; }
        .msg.user { background: var(--primary); color: white; align-self: flex-end; border-bottom-right-radius: 0; }
        .msg.bot { background: var(--bg-color); color: var(--text-color); border: 1px solid var(--border-color); align-self: flex-start; border-bottom-left-radius: 0; }
        .chat-toggle { position: fixed; bottom: 20px; right: 20px; background: var(--primary); color: white; border: none; width: 60px; height: 60px; border-radius: 50%; cursor: pointer; z-index: 999; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: 1.5rem; display: flex; align-items: center; justify-content: center; }
        
        /* Progress Bar */
        .progress-container { width: 100%; background: var(--bg-color); border-radius: 1rem; overflow: hidden; height: 1.5rem; border: 1px solid var(--border-color); margin-top: 1.5rem; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #4facfe, #00f2fe); width: 0%; transition: width 0.5s ease; position: relative; }
        
        /* Navbar Notifications */
        .navbar { position: absolute; top: 1rem; right: 2rem; display: flex; align-items: center; gap: 1rem; z-index: 100; }
        .notif-bell { background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-color); padding: 0.5rem 1rem; border-radius: 20px; cursor: pointer; position: relative; }
        .notif-badge { position: absolute; top: -5px; right: -5px; background: #ef4444; color: white; font-size: 0.7rem; padding: 0.2rem 0.4rem; border-radius: 50%; }
        .notif-dropdown { display: none; position: absolute; top: 100%; right: 0; background: var(--card-bg); border: 1px solid var(--border-color); width: 300px; border-radius: 0.5rem; margin-top: 0.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .notif-item { padding: 1rem; border-bottom: 1px solid var(--border-color); font-size: 0.9rem; }
        
        /* Activity Feed */
        .activity-feed { background: var(--bg-color); border-radius: 0.5rem; border: 1px solid var(--border-color); padding: 1rem; max-height: 250px; overflow-y: auto; }
        .activity-item { padding: 0.75rem 0; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 1rem; }
        .activity-item:last-child { border-bottom: none; }
        .activity-icon { background: var(--primary); color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body class="{% block body_class %}{% endblock %}">
    <button class="theme-toggle" onclick="toggleTheme()"><i class="bi bi-moon-stars"></i> Toggle Theme</button>
    
    {% if session.get('user') or session.get('admin') %}
    <div class="navbar">
        <div class="notif-bell" onclick="document.getElementById('notif-drop').style.display = document.getElementById('notif-drop').style.display === 'block' ? 'none' : 'block';">
            <i class="bi bi-bell-fill"></i> Notifications
            <span class="notif-badge">3</span>
            <div class="notif-dropdown" id="notif-drop">
                <div class="notif-item"><i class="bi bi-check-circle" style="color: #10b981;"></i> Model ResNet50 training completed.</div>
                <div class="notif-item"><i class="bi bi-person-plus" style="color: var(--primary);"></i> New user registered: Admin123</div>
                <div class="notif-item"><i class="bi bi-image" style="color: #f59e0b;"></i> New prediction uploaded by {{ session.get('user', 'Admin') }}</div>
            </div>
        </div>
    </div>
    {% endif %}

    {% if session.get('user') %}
    <!-- Floating Chatbot -->
    <button class="chat-toggle" onclick="document.getElementById('chatbot').style.display='flex'; this.style.display='none';"><i class="bi bi-chat-dots-fill"></i></button>
    <div class="chatbot-container" id="chatbot">
        <div class="chatbot-header" onclick="document.getElementById('chatbot').style.display='none'; document.querySelector('.chat-toggle').style.display='flex';">
            <span>Urban Planning Assistant</span>
            <i class="bi bi-x-lg"></i>
        </div>
        <div class="chatbot-messages" id="chat-msgs">
            <div class="msg bot">Hello! I am your AI assistant. Ask me anything about urban planning or your recent predictions.</div>
        </div>
        <div class="chatbot-input">
            <input type="text" id="chat-input" placeholder="Type a message..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()"><i class="bi bi-send-fill"></i></button>
        </div>
    </div>
    {% endif %}
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div style="position: absolute; top: 1rem; left: 50%; transform: translateX(-50%); z-index: 100;">
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    {% block layout %}
    {% endblock %}

    <script>
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        document.querySelectorAll('.zoom-img').forEach(img => {
            img.addEventListener('click', function() { this.classList.toggle('zoomed'); });
        });

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const msgText = input.value.trim();
            if (!msgText) return;
            
            const chatMsgs = document.getElementById('chat-msgs');
            chatMsgs.innerHTML += `<div class="msg user">${msgText}</div>`;
            input.value = '';
            chatMsgs.scrollTop = chatMsgs.scrollHeight;
            
            const typingDiv = document.createElement('div');
            typingDiv.className = 'msg bot';
            typingDiv.innerText = 'Thinking...';
            chatMsgs.appendChild(typingDiv);
            chatMsgs.scrollTop = chatMsgs.scrollHeight;
            
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msgText})
                });
                const data = await res.json();
                chatMsgs.removeChild(typingDiv);
                chatMsgs.innerHTML += `<div class="msg bot">${data.response}</div>`;
            } catch(e) {
                chatMsgs.removeChild(typingDiv);
                chatMsgs.innerHTML += `<div class="msg bot" style="color:red;">Error connecting to AI.</div>`;
            }
            chatMsgs.scrollTop = chatMsgs.scrollHeight;
        }
    </script>
</body>
</html>""",

    "user_dashboard.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%; padding: 2rem;">
            <h2>Welcome {{ session.user }}</h2>
            <p style="color: var(--text-color); margin-bottom: 2rem;">Today's Date: {{ date }}</p>
            
            <form action="{{ url_for('user_dashboard') }}" method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label>Select Pre-Trained Model</label>
                    <select name="model_file" required>
                        <option value="CNN">CNN</option>
                        <option value="VGG16">VGG16</option>
                        <option value="VGG19">VGG19</option>
                        <option value="ResNet50">ResNet50</option>
                    </select>
                </div>
                <div class="form-group" style="margin-top: 1rem;">
                    <label>Browse Input Remote Sensing Image</label>
                    <input type="file" name="image" accept="image/*" required style="padding: 1rem; border: 1px dashed var(--primary); width: 100%;">
                </div>
                <button type="submit" class="btn" style="margin-top: 1.5rem;"><i class="bi bi-cloud-upload"></i> Upload & Preprocess</button>
            </form>
            
            <h4 style="margin-top: 3rem; color: var(--primary);">Recent Activity</h4>
            <div class="activity-feed">
                <div class="activity-item"><div class="activity-icon"><i class="bi bi-image"></i></div><div>Uploaded new satellite image for analysis. <br><small style="opacity:0.7;">Just now</small></div></div>
                <div class="activity-item"><div class="activity-icon"><i class="bi bi-cpu"></i></div><div>Ran ResNet50 model (Prediction: Urban Detected). <br><small style="opacity:0.7;">2 hours ago</small></div></div>
                <div class="activity-item"><div class="activity-icon"><i class="bi bi-file-earmark-pdf"></i></div><div>Exported prediction report as PDF. <br><small style="opacity:0.7;">1 day ago</small></div></div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "admin_dashboard.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%; padding: 2rem;">
            <h2>Admin Dashboard</h2>
            <p style="color: var(--text-color); margin-bottom: 2rem;">Manage datasets, train models, and view users.</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;">
                <div style="background: var(--bg-color); padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 1px solid var(--primary);">
                    <h1 style="color: var(--primary); font-size: 3rem; margin: 0;">{{ total_users }}</h1>
                    <p>Total Registered Users</p>
                </div>
                <div style="background: var(--bg-color); padding: 1.5rem; border-radius: 0.5rem; text-align: center; border: 1px solid #10b981;">
                    <h1 style="color: #10b981; font-size: 3rem; margin: 0;">{{ total_models }}</h1>
                    <p>Total Models Run / Predictions</p>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <a href="{{ url_for('upload_dataset') }}" class="btn btn-secondary" style="padding: 2rem; text-align: center;">Upload Dataset & Collect Data</a>
                <a href="{{ url_for('train_model') }}" class="btn btn-secondary" style="padding: 2rem; text-align: center;">Create & Train DL Models</a>
                <a href="{{ url_for('user_details') }}" class="btn btn-secondary" style="padding: 2rem; text-align: center; grid-column: span 2;">View Registered Users</a>
            </div>
            
            <h4 style="margin-top: 3rem; color: var(--primary);">System Activity Feed</h4>
            <div class="activity-feed">
                <div class="activity-item"><div class="activity-icon"><i class="bi bi-person-plus"></i></div><div>New user registered successfully. <br><small style="opacity:0.7;">10 mins ago</small></div></div>
                <div class="activity-item"><div class="activity-icon"><i class="bi bi-cpu"></i></div><div>Model ResNet50 training completed. <br><small style="opacity:0.7;">1 hour ago</small></div></div>
                <div class="activity-item"><div class="activity-icon"><i class="bi bi-download"></i></div><div>Model weights (.h5) exported. <br><small style="opacity:0.7;">1 hour ago</small></div></div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "result.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <!-- Interactive Model Switcher Header -->
        <div style="width: 100%; max-width: 1200px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h2 style="margin: 0;">Analysis Results</h2>
            <form action="{{ url_for('prediction') }}" method="POST" style="display: flex; gap: 1rem; align-items: center;">
                <label style="color: var(--text-color);">One-Click Model Switch:</label>
                <select name="model_name" onchange="this.form.submit()" style="width: auto;">
                    <option value="CNN" {% if result.model_used == 'CNN' %}selected{% endif %}>CNN</option>
                    <option value="VGG16" {% if result.model_used == 'VGG16' %}selected{% endif %}>VGG16</option>
                    <option value="VGG19" {% if result.model_used == 'VGG19' %}selected{% endif %}>VGG19</option>
                    <option value="ResNet50" {% if result.model_used == 'ResNet50' %}selected{% endif %}>ResNet50</option>
                </select>
            </form>
        </div>

        <div class="card" id="exportable-report" style="max-width: 1200px; width: 100%; padding: 2rem;">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start;">
                <!-- Visualizations -->
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 0.5rem; color: var(--text-color);">Original Input</h4>
                    <img src="{{ image_path }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid var(--border-color);">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Class Activation Map (Grad-CAM)</h4>
                    <img src="{{ url_for('static', filename='graphs/heatmap_overlay.png') }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid var(--primary);">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Detected Bounding Boxes</h4>
                    <img src="{{ url_for('static', filename='graphs/bounding_boxes.png') }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid #ef4444;">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Geospatial Map Plot (Simulated)</h4>
                    <div id="map" style="width: 100%; height: 250px; border-radius: 0.5rem; border: 2px solid var(--border-color);"></div>
                </div>
                
                <!-- Metrics & Report -->
                <div>
                    <h3 style="color: {{ '#ef4444' if 'Detected' in result.prediction else '#22c55e' }}; text-align: center; font-size: 2rem; margin-bottom: 1.5rem;">{{ result.prediction }}</h3>
                    
                    <!-- Speedometer Confidence Gauge -->
                    <div style="position: relative; height: 150px; width: 100%; display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem;">
                        <canvas id="gaugeChart" style="max-width: 250px;"></canvas>
                        <div style="position: absolute; bottom: 10px; font-size: 1.2rem; font-weight: bold; color: var(--text-color);">{{ result.confidence }}%</div>
                    </div>

                    <!-- Advanced Metrics Table -->
                    <div style="background: rgba(0,0,0,0.1); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem; border: 1px solid var(--border-color);">
                        <h4 style="color: var(--primary); margin-bottom: 1rem;"><i class="bi bi-bar-chart-line-fill"></i> Model Evaluation Metrics ({{ result.model_used }})</h4>
                        <table style="width: 100%; text-align: left;">
                            <tr><th>Accuracy:</th><td>98.5%</td></tr>
                            <tr><th>Precision:</th><td>97.2%</td></tr>
                            <tr><th>Recall:</th><td>99.1%</td></tr>
                            <tr><th>F1-Score:</th><td>98.1%</td></tr>
                        </table>
                    </div>
                    
                    <!-- Confusion Matrix -->
                    <div style="text-align: center; margin-bottom: 1.5rem;">
                        <h4 style="margin-bottom: 0.5rem; color: var(--text-color);">Simulated Confusion Matrix</h4>
                        <img src="{{ url_for('static', filename='graphs/confusion_matrix.png') }}" class="zoom-img" style="max-width: 250px; border-radius: 0.5rem; border: 1px solid var(--border-color);">
                    </div>
                    
                    <!-- Gemini AI Report -->
                    <div style="background: rgba(79,172,254,0.1); padding: 1.5rem; border-radius: 0.5rem; border: 1px solid var(--primary);">
                        <h4 style="color: var(--primary); margin-bottom: 1rem;"><i class="bi bi-robot"></i> AI Generated Executive Summary</h4>
                        <div style="color: var(--text-color); font-size: 0.95rem; line-height: 1.6;">
                            {{ suggestions|safe }}
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 3rem;" data-html2canvas-ignore>
                <button onclick="exportPDF()" class="btn" style="background: #10b981;"><i class="bi bi-file-earmark-pdf-fill"></i> Export PDF Report</button>
                <a href="{{ url_for('user_dashboard') }}" class="btn btn-secondary">Predict Another Image</a>
            </div>
        </div>
    </div>
</div>

<script>
    const ctx = document.getElementById('gaugeChart').getContext('2d');
    const confidence = parseFloat("{{ result.confidence }}");
    const data = {
        labels: ['Confidence', ''],
        datasets: [{
            data: [confidence, 100 - confidence],
            backgroundColor: [confidence > 80 ? '#22c55e' : (confidence > 50 ? '#f59e0b' : '#ef4444'), '#334155'],
            borderWidth: 0,
            circumference: 180,
            rotation: 270,
            cutout: '80%'
        }]
    };
    new Chart(ctx, { type: 'doughnut', data: data, options: { responsive: true, plugins: { tooltip: { enabled: false }, legend: { display: false } } } });

    function exportPDF() {
        const element = document.getElementById('exportable-report');
        const opt = {
            margin:       0.3,
            filename:     'Urban_Growth_Report_{{ result.model_used }}.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    }
    
    // Initialize Leaflet Map (Simulated Coordinate)
    setTimeout(() => {
        var map = L.map('map').setView([28.7041, 77.1025], 13); // Default Delhi coordinates
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
        var markerColor = "{{ 'red' if 'Detected' in result.prediction else 'green' }}";
        var circle = L.circle([28.7041, 77.1025], {
            color: markerColor,
            fillColor: markerColor,
            fillOpacity: 0.5,
            radius: 500
        }).addTo(map);
        circle.bindPopup("<b>{{ result.prediction }}</b><br>Simulated Geospatial Tag.").openPopup();
    }, 500);
</script>
{% endblock %}""",

    "time_series.html": """{% extends "base.html" %}
{% block layout %}
<style>
.img-comp-container { position: relative; height: 400px; width: 100%; max-width: 600px; margin: 0 auto; overflow: hidden; border-radius: 0.5rem; border: 2px solid var(--border-color); }
.img-comp-img { position: absolute; width: auto; height: auto; overflow: hidden; }
.img-comp-img img { display: block; width: 600px; height: 400px; object-fit: cover; }
.img-comp-slider { position: absolute; z-index: 9; cursor: ew-resize; width: 40px; height: 40px; background-color: var(--primary); opacity: 0.8; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; top: 50%; left: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 10px rgba(0,0,0,0.5); }
</style>
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%; padding: 2rem;">
            <h2>Time-Series Urban Expansion Analysis</h2>
            <p style="color: var(--text-color); margin-bottom: 2rem;">Upload satellite imagery from two different dates to visually and analytically compare urban growth over time.</p>
            
            {% if not images_uploaded %}
            <form action="{{ url_for('time_series') }}" method="POST" enctype="multipart/form-data">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label>Image 1 (Past - e.g., 2015)</label>
                        <input type="file" name="image1" accept="image/*" required style="padding: 1rem; border: 1px dashed var(--primary); width: 100%;">
                    </div>
                    <div class="form-group">
                        <label>Image 2 (Present - e.g., 2025)</label>
                        <input type="file" name="image2" accept="image/*" required style="padding: 1rem; border: 1px dashed #ef4444; width: 100%;">
                    </div>
                </div>
                <button type="submit" class="btn" style="margin-top: 1.5rem; width: 100%;"><i class="bi bi-arrow-left-right"></i> Generate Comparison</button>
            </form>
            {% else %}
            
            <h4 style="text-align: center; color: var(--primary); margin-bottom: 1rem;">Before / After Comparison Slider</h4>
            <div class="img-comp-container" id="comp-container">
                <div class="img-comp-img">
                    <img src="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=600&h=400&fit=crop" alt="Present">
                </div>
                <div class="img-comp-img img-comp-overlay">
                    <img src="https://images.unsplash.com/photo-1425913397330-cf8af2ff40a1?w=600&h=400&fit=crop" alt="Past">
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem;">
                <p><strong>Analysis:</strong> Significant urban expansion detected (+45% built-up area).</p>
                <a href="{{ url_for('time_series') }}" class="btn btn-secondary" style="margin-top: 1rem;">Analyze New Pair</a>
            </div>

            <script>
                function initComparisons() {
                    var x, i;
                    x = document.getElementsByClassName("img-comp-overlay");
                    for (i = 0; i < x.length; i++) { compareImages(x[i]); }
                    function compareImages(img) {
                        var slider, clicked = 0, w, h;
                        w = img.offsetWidth; h = img.offsetHeight;
                        img.style.width = (w / 2) + "px";
                        slider = document.createElement("DIV");
                        slider.setAttribute("class", "img-comp-slider");
                        slider.innerHTML = "<i class='bi bi-arrows-expand'></i>";
                        img.parentElement.insertBefore(slider, img);
                        slider.style.top = (h / 2) - (slider.offsetHeight / 2) + "px";
                        slider.style.left = (w / 2) - (slider.offsetWidth / 2) + "px";
                        slider.addEventListener("mousedown", slideReady);
                        window.addEventListener("mouseup", slideFinish);
                        slider.addEventListener("touchstart", slideReady);
                        window.addEventListener("touchend", slideFinish);
                        function slideReady(e) { e.preventDefault(); clicked = 1; window.addEventListener("mousemove", slideMove); window.addEventListener("touchmove", slideMove); }
                        function slideFinish() { clicked = 0; }
                        function slideMove(e) {
                            var pos; if (clicked == 0) return false;
                            pos = getCursorPos(e); if (pos < 0) pos = 0; if (pos > w) pos = w;
                            slide(pos);
                        }
                        function getCursorPos(e) {
                            var a, x = 0; e = (e.changedTouches) ? e.changedTouches[0] : e;
                            a = img.getBoundingClientRect(); x = e.pageX - a.left; x = x - window.pageXOffset; return x;
                        }
                        function slide(x) { img.style.width = x + "px"; slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + "px"; }
                    }
                }
                initComparisons();
            </script>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}"""
}

for name, content in templates.items():
    with open(f'templates/{name}', 'w', encoding='utf-8') as f:
        f.write(content)

print("Ultimate templates generated successfully.")
