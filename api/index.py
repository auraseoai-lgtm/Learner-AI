from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configure OpenAI
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
            .result { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #667eea; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 AuraSEO AI</h1>
            <p style="text-align: center; color: #666;">Professional AI-Powered SEO Optimization</p>
            
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
        
        # Check if OpenAI key is configured
        if not openai.api_key:
            return jsonify({"success": False, "error": "OpenAI API key not configured in environment variables"})
        
        # Simple OpenAI call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are AuraSEO AI, a professional SEO expert. Create high-quality SEO content."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            "success": True, 
            "result": result,
            "message": "AuraSEO AI completed your request"
        })
        
    except Exception as e:
        error_msg = str(e)
        return jsonify({
            "success": False, 
            "error": f"OpenAI API error: {error_msg}",
            "help": "Check your API key and billing"
        })

@app.route('/debug')
def debug():
    return jsonify({
        "openai_configured": bool(openai.api_key),
        "server_status": "running",
        "message": "Debug endpoint working"
    })

if __name__ == '__main__':
    app.run(debug=False)