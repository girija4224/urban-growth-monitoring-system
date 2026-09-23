import os
import requests
import json

def _call_gemini_api(prompt):
    api_key = os.environ.get('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-robotics-er-1.6-preview:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts":[{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip().replace("```html", "").replace("```", ""), None
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None, str(e)

def generate_suggestions(prediction_text):
    prompt = f"""
    You are an expert urban planner and remote sensing analyst. 
    The satellite image analysis system has output the following prediction: '{prediction_text}'.
    Provide a concise, professional HTML unordered list (<ul>) with 3-5 bullet points of suggestions/actions to take based on this result. Do not include markdown formatting like ```html, just the raw <li> tags inside a <ul>.
    """
    
    response_text, err = _call_gemini_api(prompt)
    if response_text:
        return response_text
        
    # Fallback
    if "Detected" in prediction_text:
        return "<ul><li>Urban expansion detected.</li><li>Monitor land use changes.</li><li>Improve city planning.</li><li>Analyze environmental impact.</li><li>Protect green areas.</li></ul>"
    else:
        return "<ul><li>No significant urban growth detected.</li><li>Continue periodic monitoring.</li><li>Preserve natural resources.</li></ul>"

def generate_report(prediction_text, confidence, model_used, time_taken):
    prompt = f"""
    Write a highly professional, structured executive summary for an Urban Growth Monitoring Report.
    Use HTML formatting (without markdown code blocks). 
    Include the following sections (use <h3> for headings):
    1. Executive Summary (2 sentences)
    2. Technical Analysis (Discuss what it means to have {prediction_text} with {confidence}% confidence using a {model_used} architecture in {time_taken}.)
    3. Recommendations (2 actionable bullet points)
    """
    
    response_text, err = _call_gemini_api(prompt)
    if response_text:
        return response_text
        
    return f"<h3>Executive Summary</h3><p>Report generated locally: {prediction_text} with {confidence}% confidence using {model_used}.</p>"

def chat_with_bot(user_message, context=""):
    prompt = f"""
    You are an Urban Planning AI Assistant integrated into a satellite image monitoring system.
    System Context: {context}
    User Message: {user_message}
    Provide a concise, helpful, and professional response.
    """
    response_text, err = _call_gemini_api(prompt)
    if response_text:
        return response_text
    return f"I am currently offline. (API Error: {err})"
