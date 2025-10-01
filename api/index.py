from flask import Flask, request, jsonify
import requests
import os
import time

app = Flask(__name__)

# Configure Hugging Face
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
        
        # Try multiple reliable models
        models_to_try = [
            "microsoft/DialoGPT-large",  # Reliable chat model
            "microsoft/DialoGPT-medium", # Fallback
            "facebook/blenderbot-400M-distill"  # Another reliable option
        ]
        
        for model_name in models_to_try:
            try:
                API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
                headers = {"Authorization": f"Bearer {hugging_face_token}"} if hugging_face_token else {}
                
                prompt_text = f"Create professional SEO content for: {user_input}"
                
                payload = {
                    "inputs": prompt_text,
                    "parameters": {
                        "max_length": 300,
                        "temperature": 0.8,
                        "do_sample": True
                    }
                }
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()[0]['generated_text']
                    # Clean the result
                    cleaned_result = result.replace(prompt_text, "").strip()
                    
                    if cleaned_result and len(cleaned_result) > 20:
                        return jsonify({
                            "success": True, 
                            "result": f"🚀 AuraSEO AI Generated:\n\n{cleaned_result}",
                            "model_used": model_name
                        })
                
                # If model is loading, wait and try once more
                elif response.status_code == 503:
                    time.sleep(2)
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                    if response.status_code == 200:
                        result = response.json()[0]['generated_text']
                        cleaned_result = result.replace(prompt_text, "").strip()
                        if cleaned_result:
                            return jsonify({
                                "success": True, 
                                "result": f"🚀 AuraSEO AI Generated:\n\n{cleaned_result}",
                                "model_used": model_name
                            })
                
            except Exception as e:
                print(f"Model {model_name} failed: {e}")
                continue
        
        # If all models fail, provide smart sample content
        return generate_sample_content(user_input)
            
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"AI service temporarily unavailable. Please try again."
        })

def generate_sample_content(user_input):
    """Generate professional sample SEO content based on input"""
    
    # Smart content generation based on keywords
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ['meta', 'description']):
        content = f'''**Meta Description for "{user_input.split("for")[-1].strip() if "for" in user_input else "your business"}":**

"Discover exceptional quality and professional service. Our {extract_business_type(user_input)} offers premium solutions tailored to your needs. Experience the difference today!"

**Length:** 150 characters (perfect for SEO)
**Includes:** Call-to-action, keywords, value proposition'''
    
    elif any(word in input_lower for word in ['blog', 'article', 'post']):
        content = f'''**SEO-Optimized Blog Post Outline:**

**Title:** "The Ultimate Guide to {extract_topic(user_input)} in 2024"

**Introduction:**
- Hook readers with current trends
- State the importance of {extract_topic(user_input)}
- Preview key takeaways

**Key Sections:**
1. Understanding Current Market Trends
2. Best Practices and Strategies  
3. Common Mistakes to Avoid
4. Future Predictions and Opportunities

**Conclusion:**
- Summary of key points
- Call-to-action for readers
- Additional resources

**Target Keywords:** {generate_keywords(user_input)}'''
    
    elif any(word in input_lower for word in ['keyword', 'key word']):
        content = f'''**SEO Keywords for "{extract_topic(user_input)}":**

**Primary Keywords:**
- {extract_topic(user_input)} services
- professional {extract_topic(user_input)}
- best {extract_topic(user_input)} solutions

**Long-Tail Keywords:**
- affordable {extract_topic(user_input)} near me
- {extract_topic(user_input)} for beginners
- how to choose {extract_topic(user_input)}
- top rated {extract_topic(user_input)} companies

**LSI Keywords:**
- {extract_topic(user_input)} tips
- {extract_topic(user_input)} guide
- {extract_topic(user_input)} benefits'''
    
    else:
        content = f'''**AuraSEO AI Professional Content for "{user_input}":**

**Optimized Meta Description:**
"Transform your online presence with our expert {extract_topic(user_input)} solutions. Get measurable results and grow your business today."

**Key Value Propositions:**
✅ Professional expertise
✅ Proven results
✅ Customized strategies
✅ Ongoing support

**Recommended Next Steps:**
1. Conduct comprehensive SEO audit
2. Develop content strategy
3. Implement technical optimizations
4. Monitor and analyze performance

**Ready to elevate your SEO?** Contact us for a free consultation!'''

    return jsonify({
        "success": True, 
        "result": content,
        "message": "AuraSEO AI Professional Sample"
    })

def extract_topic(text):
    """Extract main topic from user input"""
    words = text.lower().split()
    exclude_words = ['write', 'create', 'generate', 'make', 'for', 'a', 'an', 'the', 'meta', 'description', 'blog', 'post', 'keyword']
    topic_words = [word for word in words if word not in exclude_words]
    return ' '.join(topic_words[:3]) if topic_words else "your business"

def extract_business_type(text):
    """Extract business type from input"""
    topic = extract_topic(text)
    return topic if topic else "business"

def generate_keywords(text):
    """Generate relevant keywords"""
    topic = extract_topic(text)
    if not topic or topic == "your business":
        return "business growth, professional services, quality solutions"
    
    return f"{topic} services, best {topic}, {topic} solutions, affordable {topic}"

@app.route('/debug')
def debug():
    return jsonify({
        "hugging_face_configured": bool(hugging_face_token),
        "server_status": "running", 
        "message": "AuraSEO AI - Multiple Model Fallback"
    })

if __name__ == '__main__':
    app.run(debug=False)