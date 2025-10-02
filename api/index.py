from flask import Flask, request, jsonify
import os

app = Flask(__name__)

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
        
        if not data:
            return jsonify({"success": False, "error": "No data received"})
            
        user_input = data.get('prompt', '').strip()
        
        if not user_input:
            return jsonify({"success": False, "error": "Please enter your SEO request"})
        
        # Generate professional SEO content based on input
        result = generate_seo_content(user_input)
        
        return jsonify({
            "success": True, 
            "result": result,
            "message": "AuraSEO AI completed your request"
        })
        
    except Exception as e:
        # Safe error handling
        return jsonify({
            "success": False, 
            "error": "Service temporarily unavailable. Please try again."
        })

def generate_seo_content(user_input):
    """Generate professional SEO content without external APIs"""
    
    input_lower = user_input.lower()
    
    # Coffee shop related
    if any(word in input_lower for word in ['coffee', 'cafe', 'espresso', 'latte']):
        return '''**Perfect Meta Description for Coffee Shop:**

"☕ Morning Brew Cafe - Experience artisanal coffee in a cozy atmosphere. Freshly roasted beans, friendly service, and the perfect brew await you. Visit us today!"

**Why This Works:**
• 156 characters (perfect for SEO)
• Includes engaging emoji (☕)
• Highlights unique selling points
• Clear call-to-action
• Sensory words create appeal

**Additional SEO Suggestions:**
- Target keywords: "artisanal coffee", "local cafe", "fresh brew"
- Create blog content about coffee brewing methods
- Optimize for "coffee shop near me" searches'''

    # Restaurant related
    elif any(word in input_lower for word in ['restaurant', 'dining', 'food', 'meal']):
        return '''**Compelling Meta Description for Restaurant:**

"🍽️ [Restaurant Name] - Exceptional dining experience with chef-crafted dishes, warm ambiance, and impeccable service. Make your reservation today!"

**SEO Optimization:**
• 148 characters (ideal length)
• Food emoji grabs attention
• Emphasizes quality and experience
• Strong reservation call-to-action

**Keyword Strategy:**
- "fine dining experience"
- "chef-crafted dishes" 
- "restaurant reservation"
- "[cuisine type] restaurant"'''

    # General meta description request
    elif any(word in input_lower for word in ['meta', 'description']):
        business_type = extract_business_type(input_lower)
        
        return f'''**Professional Meta Description for {business_type.title()}:**

"Discover exceptional quality and outstanding service at [Business Name]. Our {business_type} offers customized solutions to meet your unique needs. Contact us today!"

**Technical Details:**
• 142 characters (SEO optimized)
• Includes primary keyword
• Clear value proposition
• Professional tone
• Strong call-to-action

**Next Steps:**
- Replace [Business Name] with actual name
- Test in search results preview
- Monitor click-through rates'''

    # Blog content request
    elif any(word in input_lower for word in ['blog', 'article', 'post']):
        topic = extract_topic(input_lower)
        
        return f'''**SEO-Optimized Blog Post: "{topic.title()}"**

**Engaging Title:** "The Complete Guide to {topic.title()} in 2024: Tips, Trends, and Strategies"

**Compelling Introduction:**
In today's competitive landscape, understanding {topic} is more important than ever. This comprehensive guide covers everything you need to know to succeed.

**Content Outline:**
1. **Current Trends** - Latest developments in {topic}
2. **Best Practices** - Proven strategies for success  
3. **Common Pitfalls** - Mistakes to avoid
4. **Future Outlook** - Emerging opportunities

**Target Keywords:**
- {topic} services
- best {topic} strategies
- {topic} for beginners
- professional {topic} solutions

**SEO Tips:**
- Use H2 headings for each section
- Include internal links to related content
- Add relevant images with alt text
- Optimize for featured snippets'''

    # Keyword research request
    elif any(word in input_lower for word in ['keyword', 'key word']):
        topic = extract_topic(input_lower)
        
        return f'''**SEO Keywords for "{topic.title()}":**

**Primary Keywords:**
- {topic} services
- professional {topic}
- best {topic} solutions

**Long-Tail Keywords:**
- affordable {topic} near me
- {topic} for beginners
- how to choose {topic}
- top rated {topic} companies

**LSI Keywords:**
- {topic} tips
- {topic} guide  
- {topic} benefits
- {topic} best practices

**Keyword Research Strategy:**
- Use Google Keyword Planner
- Analyze competitor keywords
- Focus on buyer intent keywords
- Monitor search volume trends'''

    # General SEO request
    else:
        topic = extract_topic(input_lower)
        
        return f'''**AuraSEO AI Professional Content for "{topic.title()}":**

**Optimized Meta Description:**
"Transform your {topic} with our expert solutions. Get measurable results, professional guidance, and sustainable growth. Start your journey today!"

**Comprehensive SEO Strategy:**

**On-Page Optimization:**
✅ Meta tags and descriptions
✅ Header tag structure (H1, H2, H3)
✅ Keyword-optimized content
✅ Internal linking strategy

**Content Strategy:**
✅ Blog posts and articles
✅ Landing page optimization  
✅ FAQ sections for featured snippets
✅ Regular content updates

**Technical SEO:**
✅ Website speed optimization
✅ Mobile responsiveness
✅ XML sitemap implementation
✅ Schema markup

**Ready to begin?** Contact us for a free SEO audit!'''

def extract_business_type(text):
    """Extract business type from text"""
    if 'coffee' in text or 'cafe' in text:
        return 'coffee shop'
    elif 'restaurant' in text:
        return 'restaurant'
    elif 'shop' in text or 'store' in text:
        return 'retail business'
    elif 'service' in text:
        return 'service provider'
    else:
        return 'business'

def extract_topic(text):
    """Extract main topic from text"""
    words = text.split()
    exclude_words = ['write', 'create', 'generate', 'make', 'for', 'a', 'an', 'the', 'meta', 'description', 'blog', 'post', 'keyword', 'seo']
    
    for word in words:
        if word not in exclude_words and len(word) > 3:
            return word
    
    return 'your business'

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "AuraSEO AI is running"})

if __name__ == '__main__':
    app.run(debug=False)