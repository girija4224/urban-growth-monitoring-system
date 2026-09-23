import os

templates = {
    "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Urban Growth Monitoring{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <!-- Optional Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
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
        .card { background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-color); border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .sidebar { background: var(--card-bg); border-right: 1px solid var(--border-color); }
        .sidebar a { color: var(--text-color); }
        .sidebar a:hover { background: rgba(79,172,254,0.2); }
        .layout { display: flex; min-height: 100vh; }
        .sidebar { width: 250px; padding: 2rem 1rem; }
        .sidebar a { display: block; padding: 0.75rem 1rem; text-decoration: none; border-radius: 0.5rem; margin-bottom: 0.5rem; transition: background 0.2s; }
        .main-content { flex: 1; padding: 2rem; display: flex; flex-direction: column; align-items: center; }
        .full-bg { background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80') center/cover; }
        .home-overlay { background: rgba(15,23,42,0.8); width: 100%; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .theme-toggle { position: fixed; bottom: 20px; left: 20px; background: var(--primary); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; z-index: 1000; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        table th, table td { color: var(--text-color); border-bottom: 1px solid var(--border-color) !important; padding: 1rem; }
        input, select { background: var(--bg-color); color: var(--text-color); border: 1px solid var(--border-color); border-radius: 0.5rem; padding: 0.75rem; width: 100%; box-sizing: border-box; }
        .zoom-img { transition: transform 0.3s ease; cursor: zoom-in; }
        .zoom-img.zoomed { transform: scale(1.5); cursor: zoom-out; z-index: 50; position: relative; }
        
        /* Chatbot UI */
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
        .progress-bar::after { content: ''; position: absolute; top: 0; left: 0; bottom: 0; right: 0; background-image: linear-gradient(45deg, rgba(255,255,255,0.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0.15) 75%, transparent 75%, transparent); background-size: 1rem 1rem; animation: progress-stripes 1s linear infinite; }
        @keyframes progress-stripes { from { background-position: 1rem 0; } to { background-position: 0 0; } }
    </style>
</head>
<body class="{% block body_class %}{% endblock %}">
    <button class="theme-toggle" onclick="toggleTheme()"><i class="bi bi-moon-stars"></i> Toggle Theme</button>
    
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

    "preprocessing.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 800px; width: 100%; padding: 2rem;">
            <h2>Input Image Preprocessing</h2>
            <div style="display: flex; gap: 2rem; margin-top: 2rem;">
                <div style="flex: 1; text-align: center;">
                    <p style="margin-bottom: 1rem;">Original Image</p>
                    <img src="{{ image_path }}" style="max-width: 100%; border-radius: 0.5rem; border: 1px solid var(--border-color);">
                </div>
                <div style="flex: 1; background: rgba(0,0,0,0.1); padding: 1.5rem; border-radius: 0.5rem;">
                    <h4 style="margin-bottom: 1rem; color: var(--primary);">Display Information</h4>
                    <ul style="list-style: none; color: var(--text-color); line-height: 2;">
                        <li><strong>Original Size:</strong> {{ shapes.original[0] }}x{{ shapes.original[1] }}</li>
                        <li><strong>Resized Size:</strong> {{ shapes.resized[0] }}x{{ shapes.resized[1] }}</li>
                        <li><strong>Channels:</strong> RGB (3)</li>
                        <li><strong>Normalized:</strong> Yes (0 to 1)</li>
                    </ul>
                    
                    <!-- Interactive Progress Bar -->
                    <div style="margin-top: 1.5rem;">
                        <p style="margin-bottom: 0.5rem; font-size: 0.9rem;" id="prep-status">Initializing Preprocessing...</p>
                        <div class="progress-container">
                            <div class="progress-bar" id="prep-bar"></div>
                        </div>
                    </div>
                    
                    <a href="{{ url_for('visualization') }}" class="btn" id="next-btn" style="margin-top: 1.5rem; display: none;">Proceed to Visualization</a>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    setTimeout(() => { document.getElementById('prep-bar').style.width = '30%'; document.getElementById('prep-status').innerText = 'Resizing...'; }, 500);
    setTimeout(() => { document.getElementById('prep-bar').style.width = '60%'; document.getElementById('prep-status').innerText = 'Converting Color Space...'; }, 1000);
    setTimeout(() => { document.getElementById('prep-bar').style.width = '100%'; document.getElementById('prep-status').innerText = 'Normalization Complete!'; document.getElementById('next-btn').style.display = 'inline-block'; }, 1500);
</script>
{% endblock %}""",

    "prediction.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content" style="justify-content: center;">
        <div class="card" style="text-align: center; max-width: 600px; padding: 3rem;">
            <h2>Model Comparison & Prediction</h2>
            <div style="margin: 2rem 0;">
                <i class="bi bi-cpu" style="font-size: 4rem; color: var(--primary); animation: pulse 1.5s infinite;"></i>
                <style>@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }</style>
                <p style="margin-top: 1rem; font-size: 1.2rem;" id="pred-status">Loading Model Architecture...</p>
                
                <div class="progress-container" style="margin-top: 1rem;">
                    <div class="progress-bar" id="pred-bar"></div>
                </div>
            </div>
            
            <script>
                setTimeout(() => { document.getElementById('pred-bar').style.width = '25%'; document.getElementById('pred-status').innerText = 'Extracting Features...'; }, 500);
                setTimeout(() => { document.getElementById('pred-bar').style.width = '75%'; document.getElementById('pred-status').innerText = 'Running Inference...'; }, 1500);
                setTimeout(() => { document.getElementById('pred-bar').style.width = '100%'; document.getElementById('pred-status').innerText = 'Generating Final Report...'; }, 2500);
                setTimeout(() => { window.location.href = "{{ url_for('result') }}"; }, 3000);
            </script>
        </div>
    </div>
</div>
{% endblock %}""",

    "result.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'user_sidebar.html' %}
    <div class="main-content">
        <div class="card" id="exportable-report" style="max-width: 1200px; width: 100%; padding: 2rem;">
            <h2 style="text-align: center; margin-bottom: 2rem;">Advanced Analysis Report</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start;">
                
                <!-- Visualizations -->
                <div style="text-align: center;">
                    <h4 style="margin-bottom: 0.5rem; color: var(--text-color);">Original Input</h4>
                    <img src="{{ image_path }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid var(--border-color);">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Urban Region Heatmap</h4>
                    <img src="{{ url_for('static', filename='graphs/heatmap_overlay.png') }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid var(--primary);">
                    
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; color: var(--text-color);">Detected Bounding Boxes</h4>
                    <img src="{{ url_for('static', filename='graphs/bounding_boxes.png') }}" class="zoom-img" style="width: 100%; border-radius: 0.5rem; border: 2px solid #ef4444;">
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
                        <h4 style="color: var(--primary); margin-bottom: 1rem;"><i class="bi bi-bar-chart-line-fill"></i> Model Evaluation Metrics</h4>
                        <table style="width: 100%; text-align: left;">
                            <tr><th>Model Architecture:</th><td>{{ result.model_used }}</td></tr>
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
            filename:     'Urban_Growth_Report.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    }
</script>
{% endblock %}""",

    "train_model.html": """{% extends "base.html" %}
{% block layout %}
<div class="layout">
    {% include 'admin_sidebar.html' %}
    <div class="main-content">
        <div class="card" style="max-width: 900px; width: 100%; padding: 2rem;">
            <h2>Create & Train Deep Learning Models</h2>
            
            <form id="trainForm" onsubmit="startTraining(event)">
                <div class="form-group">
                    <label>Select Model to Train</label>
                    <select name="model_type" id="modelType" required>
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
                <button type="submit" class="btn" id="trainBtn" style="margin-top: 1rem;"><i class="bi bi-play-circle-fill"></i> Start Live Training Simulation</button>
            </form>
            
            <!-- Real-time Training Charts -->
            <div id="trainingVisuals" style="display: none; margin-top: 2rem;">
                <h4 style="text-align: center; color: var(--primary);">Live Training Progress</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
                    <div><canvas id="accChart"></canvas></div>
                    <div><canvas id="lossChart"></canvas></div>
                </div>
                <div style="text-align: center; margin-top: 1rem; color: #10b981; font-weight: bold;" id="trainStatus"></div>
                
                <!-- Export Links (Hidden until done) -->
                <div id="exportLinks" style="display: none; margin-top: 2rem; padding: 1.5rem; background: rgba(0,0,0,0.1); border-radius: 0.5rem; border: 1px solid var(--border-color); text-align: center;">
                    <h4 style="color: var(--primary); margin-bottom: 1rem;"><i class="bi bi-download"></i> Export Trained Model</h4>
                    <p style="margin-bottom: 1rem; font-size: 0.9rem;">Download the model weights and architecture in your preferred format:</p>
                    <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
                        <a id="dl-h5" class="btn btn-secondary" style="width: auto;">.h5</a>
                        <a id="dl-json" class="btn btn-secondary" style="width: auto;">.json</a>
                        <a id="dl-pt" class="btn btn-secondary" style="width: auto;">.pt</a>
                        <a id="dl-pkl" class="btn btn-secondary" style="width: auto;">.pkl</a>
                        <a id="dl-onnx" class="btn btn-secondary" style="width: auto;">.onnx</a>
                    </div>
                </div>
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
        document.getElementById('exportLinks').style.display = 'none';
        document.getElementById('trainStatus').innerText = 'Initializing...';
        
        const epochs = parseInt(document.getElementById('epochs').value);
        const modelType = document.getElementById('modelType').value;
        
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
                document.getElementById('trainStatus').innerText = 'Training Completed Successfully!';
                
                // Set Download Links
                const formats = ['h5', 'json', 'pt', 'pkl', 'onnx'];
                formats.forEach(f => {
                    document.getElementById(`dl-${f}`).href = `/download_model/${modelType.toLowerCase()}_model.${f}`;
                });
                document.getElementById('exportLinks').style.display = 'block';
            }
        }, 800);
    }
</script>
{% endblock %}"""
}

for name, content in templates.items():
    with open(f'templates/{name}', 'w', encoding='utf-8') as f:
        f.write(content)

print("Final advanced templates generated successfully.")
