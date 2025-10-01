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
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            textarea { width: 100%; height: 120px; padding: 15px; border: 2px solid #ddd; border-radius: 10px; font-size: 16px; margin: 15px 0; }
            button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; border: none; border-radius: 1010px; font-size: 16px; cursor: pointer; width: 100%; }
            .result { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #667eea; white-space: pre-wrap; }
            .loading { display: none; text-align: center; color: #667eea; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AuraSEO AI</h1>
            <p style="text-align: center; color: #666;">Professional AI-Powered SEO Optimization</p>
            
            <textarea id="prompt" placeholder="Describe your SEO needs...&#10;Examples:&#10;- Write meta descriptions for a coffee shop&#10;- Create SEO-optimized blog post&#10;- Generate keywords for local business"></textarea>
            
            <button onclick="generateContent()">Generate SEO Content</button>
            
            <div class="loading" id="loading">
                🔄 AuraSEO AI is working...
            </div>
            
            <div class="result" id="result">
                Your AI-optimized content will appear here...
            </div>
        </div>

        <script>
            async function generateContent() {
                const prompt = document.getElementById('prompt').value;
                const result = document.getElementById('result');
                const loading = document.getElementById('loading');
                
                if (!prompt) {
                    alert('Please enter your SEO request');
                    return;
                }
                
                loading.style.display = 'block';
                result.textContent = 'Loading...';
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: prompt })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        result.textContent = data.result;
                    } else {
                        result.textContent = 'Error: ' + data.error;
                    }
                } catch (error) {
                    result.textContent = 'Network error: ' + error.message;
                } finally {
                    loading.style.display = 'none';
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
        
        # Try AI services in order
        result = None
        engine_used = None
        
        # Try OpenAI (version 0.28.1 compatible)
        if openai.api_key:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are AuraSEO AI, a professional SEO expert. Create high-quality, optimized SEO content."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                result = response.choices[0].message.content
                engine_used = "openai"
            except Exception as e:
                print(f"OpenAI error: {e}")
        
        # Try Google AI
        if not result and google_api_key:
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"As a professional SEO expert, create optimized content for: {user_input}")
                result = response.text
                engine_used = "google"
            except Exception as e:
                print(f"Google AI error: {e}")
        
        # Try Hugging Face
        if not result and hugging_face_token:
            try:
                API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
                headers = {"Authorization": f"Bearer {hugging_face_token}"}
                payload = {"inputs": f"Create SEO content: {user_input}"}
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()[0]['generated_text']
                    engine_used = "huggingface"
            except Exception as e:
                print(f"Hugging Face error: {e}")
        
        if result:
            return jsonify({
                "success": True, 
                "result": result,
                "engine_used": engine_used
            })
        else:
            return jsonify({
                "success": False, 
                "error": "All AI services are currently unavailable. Please try again later."
            })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Service error: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=False)