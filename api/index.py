from flask import Flask, request, jsonify
import openai
import google.generativeai as genai
import requests
import os

app = Flask(__name__)

# Configure APIs
openai.api_key = os.environ.get('OPENAI_API_KEY')
google_api_key = os.environ.get('GOOGLE_AI_KEY')
hugging_face_token = os.environ.get('HUGGING_FACE_TOKEN')

if google_api_key:
    genai.configure(api_key=google_api_key)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AuraSEO AI Platform</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            textarea { width: 100%; height: 100px; margin: 10px 0; }
            button { background: #0070f3; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .result { background: white; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AuraSEO AI</h1>
            <p>Professional AI-Powered SEO Optimization</p>
            
            <textarea id="prompt" placeholder="Enter your SEO request..."></textarea>
            <br>
            <button onclick="generateContent()">Generate SEO Content</button>
            
            <div class="result" id="result">
                Your content will appear here...
            </div>
        </div>

        <script>
            async function generateContent() {
                const prompt = document.getElementById('prompt').value;
                const result = document.getElementById('result');
                
                if (!prompt) {
                    alert('Please enter a request');
                    return;
                }
                
                result.innerHTML = 'Generating...';
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        result.innerHTML = data.result;
                    } else {
                        result.innerHTML = 'Error: ' + data.error;
                    }
                } catch (error) {
                    result.innerHTML = 'Network error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        user_input = data.get('prompt', '')
        
        if not user_input:
            return jsonify({"success": False, "error": "No prompt provided"})
        
        # Try OpenAI first
        if openai.api_key:
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Create SEO content: {user_input}"}],
                    max_tokens=500
                )
                return jsonify({"success": True, "result": response.choices[0].message.content})
            except:
                pass
        
        # Try Google AI
        if google_api_key:
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Create SEO content: {user_input}")
                return jsonify({"success": True, "result": response.text})
            except:
                pass
        
        # Try Hugging Face
        if hugging_face_token:
            try:
                API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
                headers = {"Authorization": f"Bearer {hugging_face_token}"}
                response = requests.post(API_URL, headers=headers, json={"inputs": user_input})
                return jsonify({"success": True, "result": response.json()[0]['generated_text']})
            except:
                pass
        
        return jsonify({"success": False, "error": "All AI services failed"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Vercel requires this
if __name__ == '__main__':
    app.run(debug=False)
