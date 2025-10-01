from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)

# Configure API
openai.api_key = os.environ.get('OPENAI_API_KEY')

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
            .result { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #667eea; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AuraSEO AI</h1>
            <p style="text-align: center; color: #666;">Professional AI-Powered SEO Optimization</p>
            
            <textarea id="prompt" placeholder="Type your SEO request here..."></textarea>
            
            <button onclick="generateContent()">Generate SEO Content</button>
            
            <div class="result" id="result">
                AI content will appear here...
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
                
                result.innerHTML = '🔄 AuraSEO AI is working...';
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        body: JSON.stringify({ prompt: prompt })
                    });
                    
                    console.log('Response status:', response.status);
                    const data = await response.json();
                    console.log('Response data:', data);
                    
                    if (data.success) {
                        result.innerHTML = data.result;
                    } else {
                        result.innerHTML = 'Error: ' + data.error;
                    }
                } catch (error) {
                    console.error('Fetch error:', error);
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
        print("API endpoint called")
        data = request.get_json()
        print("Received data:", data)
        
        if not data or 'prompt' not in data:
            return jsonify({"success": False, "error": "No prompt provided"})
        
        user_input = data['prompt']
        print("User input:", user_input)
        
        if not openai.api_key:
            return jsonify({"success": False, "error": "OpenAI API key not configured"})
        
        print("Calling OpenAI...")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": f"You are AuraSEO AI, a professional SEO expert. Respond to this request: {user_input}"
            }],
            max_tokens=300
        )
        
        result = response.choices[0].message.content
        print("OpenAI response received")
        
        return jsonify({
            "success": True, 
            "result": result,
            "message": "AuraSEO AI completed your request"
        })
        
    except Exception as e:
        print("Error in generate_content:", str(e))
        return jsonify({
            "success": False, 
            "error": f"AI service error: {str(e)}"
        })

@app.route('/debug')
def debug():
    return jsonify({
        "server_status": "running",
        "openai_configured": bool(openai.api_key),
        "message": "Server is working correctly"
    })

if __name__ == '__main__':
    app.run(debug=False)