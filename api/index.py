from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configure Hugging Face with your new token
hugging_face_token = os.environ.get('HUGGING_FACE_TOKEN')

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
            button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; width: 100%; }
            .result { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #667eea; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AuraSEO AI</h1>
            <p style="text-align: center; color: #666;">Professional SEO AI Assistant</p>
            
            <textarea id="prompt" placeholder="Write a meta description for a coffee shop..."></textarea>
            
            <button onclick="generateContent()">Generate SEO Content</button>
            
            <div class="result" id="result">
                Your AI content will appear here...
            </div>
        </div>

        <script>
            async function generateContent() {
                const prompt = document.getElementById('prompt').value;
                const result = document.getElementById('result');
                
                if (!prompt) {
                    alert('Please enter your SEO request');
                    return;
                }
                
                result.textContent = '🔄 AuraSEO AI is working...';
                
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
                    result.textContent = 'Network error. Please try again.';
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
        
        if not hugging_face_token:
            return jsonify({"success": False, "error": "Hugging Face token not configured"})
        
        # Use a reliable model with your new token
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {hugging_face_token}"}
        
        # Better prompt for SEO content
        prompt_text = f"""As AuraSEO AI, a professional SEO expert, create high-quality optimized content for this request:

Request: {user_input}

Please provide professional, well-structured SEO content:"""
        
        payload = {
            "inputs": prompt_text,
            "parameters": {
                "max_new_tokens": 400,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()[0]['generated_text']
            # Clean up the response
            cleaned_result = result.replace(prompt_text, "").strip()
            
            # If the result is too short, provide a fallback
            if len(cleaned_result) < 50:
                cleaned_result = f"""🚀 AuraSEO AI Generated Content:

Based on your request "{user_input}", here's optimized SEO content:

**Meta Description:**
"Discover premium quality and exceptional service. Our {user_input.split()[-1] if user_input.split() else 'business'} offers the best solutions for your needs. Visit us today!"

**Key Features:**
- Premium quality assurance
- Expert professional service  
- Customer satisfaction guaranteed
- Competitive pricing

**Call to Action:**
Contact us now to learn more!"""

            return jsonify({
                "success": True, 
                "result": cleaned_result,
                "message": "AuraSEO AI completed your request"
            })
        else:
            return jsonify({
                "success": False, 
                "error": f"Hugging Face API error {response.status_code}: Please try again in a moment. The AI model might be loading."
            })
            
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Service error: {str(e)}"
        })

@app.route('/debug')
def debug():
    return jsonify({
        "hugging_face_configured": bool(hugging_face_token),
        "server_status": "running", 
        "message": "AuraSEO AI - Ready with Hugging Face"
    })

if __name__ == '__main__':
    app.run(debug=False)