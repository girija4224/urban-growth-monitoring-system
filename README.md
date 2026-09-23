# 🏙️ AIML-Based Urban Growth Monitoring System

An AI/ML-based web application for analyzing satellite or urban images and classifying areas as **Urban** or **Non-Urban**. The system uses deep learning models for image classification and provides prediction results along with visual analysis and AI-powered insights.

## 📌 Project Overview

Rapid urbanization leads to significant changes in land use and the environment. Monitoring urban growth manually from large amounts of satellite imagery can be time-consuming.

The **AIML-Based Urban Growth Monitoring System** provides an automated approach to identify urban and non-urban regions from images using deep learning techniques.

The system is developed as a Flask web application and integrates machine learning models, image preprocessing, visualization, database functionality, and AI-generated insights.

## 🎯 Objectives

* Detect urban and non-urban regions from images.
* Apply deep learning techniques for image classification.
* Provide automated prediction results through a web interface.
* Visualize model predictions and analysis.
* Generate AI-powered suggestions and reports.
* Provide a simple interface for users to upload images and obtain results.

## 🚀 Key Features

* 🖼️ Image upload and preprocessing
* 🤖 Deep learning-based image classification
* 🏙️ Urban / Non-Urban prediction
* 📊 Prediction visualization
* 🔥 Model visualization and analysis
* 🧠 AI-powered suggestions and report generation
* 💬 AI chatbot functionality
* 👤 User authentication
* 🗄️ Database integration
* 🌐 Flask-based web interface

## 🧠 Machine Learning

The project uses deep learning techniques for image classification.

The workflow includes:

```text
Input Image
     ↓
Image Preprocessing
     ↓
Deep Learning Model
     ↓
Feature Extraction
     ↓
Classification
     ↓
Urban / Non-Urban
     ↓
Visualization & AI Insights
```

## 📂 Project Structure

```text
urban-growth-monitoring-system/
│
├── app.py
├── database.py
├── requirements.txt
├── generate_templates.py
├── update_templates.py
├── update_templates_2.py
├── update_templates_3.py
│
├── dataset/
│   ├── train/
│   │   ├── urban/
│   │   └── non-urban/
│   │
│   └── test/
│       ├── urban/
│       └── non-urban/
│
├── ml/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── inference.py
│   ├── models.py
│   ├── train.py
│   └── visualization.py
│
├── prediction/
│   ├── __init__.py
│   ├── gemini_helper.py
│   ├── infer.py
│   └── visualize.py
│
├── preprocessing/
│   ├── __init__.py
│   └── process.py
│
├── training/
│   ├── __init__.py
│   └── models.py
│
├── static/
│   ├── css/
│   └── graphs/
│
└── templates/
```

## 🗂️ Dataset

The dataset contains two major categories:

* **Urban**
* **Non-Urban**

Example structure:

```text
dataset/
├── train/
│   ├── urban/
│   └── non-urban/
│
└── test/
    ├── urban/
    └── non-urban/
```

Images are processed and converted into a suitable format before being provided to the deep learning model.

## ⚙️ Technologies Used

| Technology         | Purpose                   |
| ------------------ | ------------------------- |
| Python             | Core programming language |
| Flask              | Web application framework |
| TensorFlow / Keras | Deep learning             |
| NumPy              | Numerical processing      |
| OpenCV / PIL       | Image processing          |
| HTML               | Web page structure        |
| CSS                | User interface styling    |
| JavaScript         | Frontend interactions     |
| SQLite             | Database functionality    |
| Gemini API         | AI-powered insights       |

## 🔄 System Workflow

1. User accesses the web application.
2. User uploads an image.
3. The image is preprocessed.
4. The processed image is passed to the trained model.
5. The model predicts whether the image represents an **Urban** or **Non-Urban** area.
6. Prediction results are displayed on the web interface.
7. Visualization techniques are used to analyze the prediction.
8. AI-based functionality can generate additional suggestions and reports.

## 🖥️ Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/girija4224/urban-growth-monitoring-system.git
```

### 2. Open the project

```bash
cd urban-growth-monitoring-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

⚠️ **Do not upload `.env` to GitHub.**

### 7. Run the application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000/
```

## 🔐 Security

API keys and sensitive configuration files are excluded from the GitHub repository using `.gitignore`.

The project uses environment variables for API credentials.

Never place API keys directly inside Python source code.

## 📊 Output

The system provides:

* Predicted class
* Prediction information
* Visualization results
* AI-generated suggestions
* AI-generated reports
* Interactive web interface

## 🔮 Future Scope

The system can be enhanced by:

* Integrating real-time satellite imagery from **Sentinel** and **Landsat**.
* Using transformer-based deep learning models.
* Implementing semantic segmentation for detailed land-use analysis.
* Integrating Geographic Information System (GIS) technologies.
* Deploying the application on cloud platforms.
* Supporting large-scale urban monitoring.
* Developing a mobile application.
* Adding temporal analysis to monitor urban growth over multiple years.

## 🏗️ Applications

The system can potentially support:

* Urban planning
* Land-use monitoring
* Smart city development
* Environmental monitoring
* Infrastructure planning
* Geographic analysis
* Urban expansion studies

## 📚 Academic Project

**Project:** AIML-Based Urban Growth Monitoring System

**Domain:** Artificial Intelligence and Machine Learning

**Application Type:** Flask Web Application

## 👩‍💻 Author

**Girijeswari Kavuri**

CSE – Artificial Intelligence & Machine Learning

GitHub: [@girija4224](https://github.com/girija4224)

---

⭐ If you find this project useful, consider giving the repository a star!
