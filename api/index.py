from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Simple configuration
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/')
def home():
    return '''
    <html>
    <body>
        <h1>🚀 AuraSEO AI - TEST</h1>
        <textarea id="prompt"></textarea>
        <button onclick="test()">Test</button>
        <div id="result"></div>
        <script>
            async function test() {
                const response = await fetch('/test');
                const data = await response.json();
                document.getElementById('result').innerHTML = data.message;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return jsonify({
        "message": "Server is working!",
        "openai_configured": bool(openai.api_key),
        "next_step": "Now test AI"
    })

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        if not openai.api_key:
            return jsonify({"success": False, "error": "OpenAI API key not configured"})
        
        user_input = request.json.get('prompt', '')
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Say 'AuraSEO AI is working! You asked: {user_input}'"}],
            max_tokens=50
        )
        
        return jsonify({
            "success": True, 
            "result": response.choices[0].message.content
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=False)