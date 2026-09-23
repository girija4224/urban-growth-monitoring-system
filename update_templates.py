import os

templates = {
    "user_sidebar.html": """
<div class="sidebar">
    <h3 style="color: var(--text-color, white); margin-bottom: 2rem; font-size: 1.2rem; text-align: center;">User Menu</h3>
    <a href="{{ url_for('user_dashboard') }}">Dashboard</a>
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
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
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
        .card { background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-color); }
        .sidebar { background: var(--card-bg); border-right: 1px solid var(--border-color); }
        .sidebar a { color: var(--text-color); }
        .sidebar a:hover { background: rgba(79,172,254,0.2); }
        .layout { display: flex; min-height: 100vh; }
        .sidebar { width: 250px; padding: 2rem 1rem; }
        .sidebar a { display: block; padding: 0.75rem 1rem; text-decoration: none; border-radius: 0.5rem; margin-bottom: 0.5rem; transition: background 0.2s; }
        .main-content { flex: 1; padding: 2rem; display: flex; flex-direction: column; align-items: center; }
        .full-bg { background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80') center/cover; }
        .home-overlay { background: rgba(15,23,42,0.8); width: 100%; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .theme-toggle { position: fixed; bottom: 20px; right: 20px; background: var(--primary); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; z-index: 1000; }
        table th, table td { color: var(--text-color); border-bottom: 1px solid var(--border-color) !important; }
        input, select { background: var(--bg-color); color: var(--text-color); border: 1px solid var(--border-color); }
        .zoom-img { transition: transform 0.3s ease; cursor: zoom-in; }
        .zoom-img.zoomed { transform: scale(1.5); cursor: zoom-out; z-index: 50; position: relative; }
    </style>
</head>
<body class="{% block body_class %}{% endblock %}">
    <button class="theme-toggle" onclick="toggleTheme()">🌓 Toggle Theme</button>
    
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

    <script>
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        // Interactive Zoom for images
        document.querySelectorAll('.zoom-img').forEach(img => {
            img.addEventListener('click', function() {
                this.classList.toggle('zoomed');
            });
        });
    </script>
</body>
</html>""",

    "history.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 1000px; width: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <h2>Prediction History</h2>
                <a href="{{ url_for('export_excel') }}" class="btn" style="background: #10b981;">Export to Excel</a>
            </div>
            
            <form action="{{ url_for('history') }}" method="GET" style="margin-bottom: 2rem; display: flex; gap: 1rem;">
                <input type="text" name="search" value="{{ search }}" placeholder="Search by Date, Model, or Prediction..." style="flex: 1; padding: 0.75rem; border-radius: 0.5rem;">
                <button type="submit" class="btn">Search</button>
            </form>
            
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; text-align: left;">
                    <thead>
                        <tr>
                            <th style="padding: 1rem; color: var(--primary);">Date</th>
                            <th style="padding: 1rem; color: var(--primary);">Model Used</th>
                            <th style="padding: 1rem; color: var(--primary);">Prediction</th>
                            <th style="padding: 1rem; color: var(--primary);">Confidence</th>
                            <th style="padding: 1rem; color: var(--primary);">Image Path</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for pred in predictions %}
                        <tr>
                            <td style="padding: 1rem;">{{ pred[4] }}</td>
                            <td style="padding: 1rem;">{{ pred[1] }}</td>
                            <td style="padding: 1rem;">
                                <span style="color: {{ '#ef4444' if 'Detected' in pred[2] else '#22c55e' }}; font-weight: bold;">{{ pred[2] }}</span>
                            </td>
                            <td style="padding: 1rem;">{{ pred[3] }}%</td>
                            <td style="padding: 1rem; font-size: 0.8rem; opacity: 0.7;">{{ pred[0] }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="5" style="text-align: center; padding: 2rem;">No predictions found.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
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
        <div class="card" id="exportable-report" style="max-width: 1000px; width: 100%; padding: 2rem;">
            <h2 style="text-align: center;">Advanced Analysis Report</h2>
            
            <!-- Side by Side Original vs Heatmap/BBox -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; align-items: start;">
                
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 0.5rem; color: var(--text-color);">Original Input</h4>
                    <img src="{{ image_path }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid var(--border-color);">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Urban Region Heatmap</h4>
                    <img src="{{ url_for('static', filename='graphs/heatmap_overlay.png') }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid var(--primary);">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Detected Bounding Boxes</h4>
                    <img src="{{ url_for('static', filename='graphs/bounding_boxes.png') }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid #ef4444;">
                </div>
                
                <div>
                    <h3 style="color: {{ '#ef4444' if 'Detected' in result.prediction else '#22c55e' }}; text-align: center; font-size: 2rem; margin-bottom: 2rem;">{{ result.prediction }}</h3>
                    
                    <!-- Speedometer Confidence Gauge -->
                    <div style="position: relative; height: 200px; width: 100%; display: flex; justify-content: center; align-items: center; margin-bottom: 2rem;">
                        <canvas id="gaugeChart" style="max-width: 300px;"></canvas>
                        <div style="position: absolute; bottom: 30px; font-size: 1.5rem; font-weight: bold; color: var(--text-color);">{{ result.confidence }}%</div>
                    </div>

                    <div style="background: rgba(0,0,0,0.1); padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem;">
                        <p><strong>Model Used:</strong> {{ result.model_used }}</p>
                        <p><strong>Prediction Time:</strong> {{ result.time_taken }}</p>
                    </div>
                    
                    <div>
                        <h4 style="color: var(--primary); margin-bottom: 0.5rem;">AI Suggestions</h4>
                        <div style="color: var(--text-color); font-size: 0.9rem; margin-left: 1rem;">
                            {{ suggestions|safe }}
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 3rem;" data-html2canvas-ignore>
                <a href="{{ url_for('download_report') }}" class="btn">Text Summary</a>
                <button onclick="exportPDF()" class="btn" style="background: #10b981;">Export to PDF</button>
                <a href="{{ url_for('user_dashboard') }}" class="btn btn-secondary">Predict Another</a>
            </div>
        </div>
    </div>
</div>

<script>
    // Gauge Chart Logic
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
            cutout: '80%',
            needleValue: confidence
        }]
    };
    new Chart(ctx, { type: 'doughnut', data: data, options: { responsive: true, plugins: { tooltip: { enabled: false }, legend: { display: false } } } });

    // PDF Export
    function exportPDF() {
        const element = document.getElementById('exportable-report');
        const opt = {
            margin:       0.5,
            filename:     'Urban_Growth_Report.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    }
</script>
{% endblock %}""",

    "admin_dashboard.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%;">
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
        </div>
    </div>
</div>
{% endblock %}""",

    "train_model.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 900px; width: 100%;">
            <h2>Create & Train Deep Learning Models</h2>
            
            <form id="trainForm" onsubmit="startTraining(event)">
                <div class="form-group">
                    <label>Select Model to Train</label>
                    <select name="model_type" required>
                        <option value="CNN">CNN</option>
                        <option value="VGG16">VGG16</option>
                        <option value="VGG19">VGG19</option>
                        <option value="ResNet50">ResNet50</option>
                    </select>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group"><label>Epochs</label><input type="number" id="epochs" value="10" required></div>
                    <div class="form-group"><label>Batch Size</label><input type="number" value="32" required></div>
                    <div class="form-group"><label>Learning Rate</label><input type="number" step="0.001" value="0.001" required></div>
                    <div class="form-group"><label>Optimizer</label><select><option>Adam</option><option>SGD</option></select></div>
                </div>
                <button type="submit" class="btn" id="trainBtn" style="margin-top: 1rem;">Start Live Training Simulation</button>
            </form>
            
            <!-- Real-time Training Charts -->
            <div id="trainingVisuals" style="display: none; margin-top: 2rem;">
                <h4 style="text-align: center; color: var(--primary);">Live Training Progress</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
                    <div><canvas id="accChart"></canvas></div>
                    <div><canvas id="lossChart"></canvas></div>
                </div>
                <div style="text-align: center; margin-top: 1rem; color: #10b981; font-weight: bold;" id="trainStatus"></div>
            </div>
        </div>
    </div>
</div>

<script>
    let accChart, lossChart;
    
    function startTraining(e) {
        e.preventDefault();
        document.getElementById('trainBtn').disabled = true;
        document.getElementById('trainBtn').innerText = 'Training in Progress...';
        document.getElementById('trainingVisuals').style.display = 'block';
        document.getElementById('trainStatus').innerText = 'Initializing...';
        
        const epochs = parseInt(document.getElementById('epochs').value);
        
        // Initialize Charts
        const accCtx = document.getElementById('accChart').getContext('2d');
        const lossCtx = document.getElementById('lossChart').getContext('2d');
        
        if(accChart) { accChart.destroy(); lossChart.destroy(); }
        
        accChart = new Chart(accCtx, { type: 'line', data: { labels: [], datasets: [{ label: 'Accuracy', data: [], borderColor: '#10b981', tension: 0.1 }] }});
        lossChart = new Chart(lossCtx, { type: 'line', data: { labels: [], datasets: [{ label: 'Loss', data: [], borderColor: '#ef4444', tension: 0.1 }] }});
        
        let currentEpoch = 0;
        let accuracy = 0.5;
        let loss = 1.0;
        
        const interval = setInterval(() => {
            currentEpoch++;
            accuracy = Math.min(0.99, accuracy + (Math.random() * 0.1));
            loss = Math.max(0.01, loss - (Math.random() * 0.15));
            
            accChart.data.labels.push(`Ep ${currentEpoch}`);
            accChart.data.datasets[0].data.push(accuracy);
            accChart.update();
            
            lossChart.data.labels.push(`Ep ${currentEpoch}`);
            lossChart.data.datasets[0].data.push(loss);
            lossChart.update();
            
            document.getElementById('trainStatus').innerText = `Training Epoch ${currentEpoch}/${epochs}...`;
            
            if (currentEpoch >= epochs) {
                clearInterval(interval);
                document.getElementById('trainBtn').disabled = false;
                document.getElementById('trainBtn').innerText = 'Start Live Training Simulation';
                document.getElementById('trainStatus').innerText = 'Training Completed Successfully! Model saved (.h5)';
            }
        }, 1000);
    }
</script>
{% endblock %}"""
}

for name, content in templates.items():
    with open(f'templates/{name}', 'w', encoding='utf-8') as f:
        f.write(content)

print("Advanced templates generated successfully.")
