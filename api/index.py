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
            <p style="text-align: center; color: #666;">Professional SEO & Content AI Assistant</p>
            
            <textarea id="prompt" placeholder="Ask me about SEO, content creation, or general questions..."></textarea>
            
            <button onclick="generateContent()">Generate Content</button>
            
            <div class="result" id="result">
                Your AI-generated content will appear here...
            </div>
        </div>

        <script>
            async function generateContent() {
                const prompt = document.getElementById('prompt').value;
                const result = document.getElementById('result');
                
                if (!prompt) {
                    alert('Please enter your question or request');
                    return;
                }
                
                result.textContent = '🔄 AuraSEO AI is thinking...';
                
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
            return jsonify({"success": False, "error": "Please enter your question or request"})
        
        # Smart content detection - is this SEO-related or general question?
        response = generate_smart_response(user_input)
        
        return jsonify({
            "success": True, 
            "result": response,
            "message": "AuraSEO AI completed your request"
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": "Service temporarily unavailable. Please try again."
        })

def generate_smart_response(user_input):
    """Generate appropriate response based on question type"""
    
    input_lower = user_input.lower()
    
    # Detect if it's an SEO-related question
    seo_keywords = ['seo', 'meta', 'description', 'keyword', 'blog', 'content', 'website', 'google', 'rank', 'search', 'optimiz', 'traffic']
    is_seo_question = any(keyword in input_lower for keyword in seo_keywords)
    
    # Detect general questions
    general_questions = {
        'why people sleep at night': '''🌙 **Why People Sleep at Night?**

**Biological Reasons:**
• **Circadian Rhythm:** Our internal body clock is programmed for daytime activity and nighttime rest
• **Melatonin Production:** Darkness triggers melatonin, the sleep hormone
• **Evolution:** Humans evolved to be daytime hunters/gatherers - night was dangerous

**Practical Benefits:**
• **Safety:** Reduced risk of accidents in darkness
• **Social Coordination:** Aligns with societal schedules
• **Temperature:** Cooler nights promote better sleep

**SEO Connection:** While this isn't directly SEO-related, understanding human behavior helps create content that matches when people are actively searching!''',

        'how to make coffee': '''☕ **How to Make Great Coffee**

**Basic Steps:**
1. **Choose Quality Beans:** Freshly roasted coffee beans
2. **Proper Grinding:** Grind just before brewing
3. **Correct Measurements:** 2 tablespoons coffee per 6 ounces water
4. **Water Temperature:** 195-205°F (90-96°C)
5. **Brew Time:** 4-5 minutes for optimal extraction

**Pro Tips:**
• Use filtered water for better taste
• Clean equipment regularly
• Experiment with grind size

**SEO Angle:** "How to make coffee" gets over 100,000 monthly searches - perfect for food blogs or coffee shop content!''',

        'what is seo': '''🚀 **What is SEO? (Search Engine Optimization)**

**SEO Definition:** 
SEO is the practice of optimizing websites to rank higher in search engine results, driving organic (free) traffic.

**Main Components:**
✅ **On-Page SEO:** Content, meta tags, headings
✅ **Technical SEO:** Site speed, mobile-friendliness, structure  
✅ **Off-Page SEO:** Backlinks, social signals, authority
✅ **Local SEO:** Google Business Profile, local citations

**Why It Matters:**
• 93% of online experiences begin with search engines
• SEO leads have a 14.6% close rate vs. 1.7% for outbound
• Cost-effective long-term strategy''',

        'hello': '''👋 **Hello! I'm AuraSEO AI**

I'm your professional SEO and content assistant! I can help you with:

**SEO Services:**
• Meta descriptions and title tags
• Keyword research and strategy
• Content optimization
• SEO audits and recommendations

**Content Creation:**
• Blog post outlines
• Marketing copy
• Social media content
• General writing assistance

**Just ask me anything related to SEO, content marketing, or general questions!**

*Try: "Write a meta description for a coffee shop" or "What are the best SEO practices?"*'''
    }
    
    # Check if it's a known general question
    for question, answer in general_questions.items():
        if question in input_lower:
            return answer
    
    # If it's clearly an SEO question, provide SEO content
    if is_seo_question:
        return generate_seo_content(user_input)
    
    # Otherwise, provide helpful general response
    return f'''🤔 **AuraSEO AI Response**

I see you asked: "*{user_input}*"

**As an SEO expert, here's my perspective:**

While your question isn't directly about SEO, understanding various topics helps create comprehensive content that answers real user questions.

**How This Relates to SEO:**
• People search for information on countless topics
• Quality content that answers questions ranks well in Google
• Understanding diverse subjects makes you a better content creator

**SEO Tip:** If you're writing about this topic, consider:
- Researching what people actually search for
- Creating comprehensive, authoritative content
- Using relevant keywords naturally
- Structuring content with clear headings

**Need SEO-specific help? Try:**
• "Write meta description for [business]"
• "Create blog post about [topic]"
• "Generate keywords for [industry]"'''

def generate_seo_content(user_input):
    """Generate professional SEO content"""
    
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

    # Meta description request
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
- professional {topic} solutions'''

    # General SEO content
    else:
        return f'''**AuraSEO AI Professional Content**

Based on your request: "*{user_input}*"

**Optimized Meta Description:**
"Transform your online presence with expert solutions. Get measurable results, professional guidance, and sustainable growth. Start your journey today!"

**Comprehensive SEO Approach:**

**Content Strategy:**
✅ Keyword research and optimization
✅ Blog posts and articles
✅ Landing page content
✅ FAQ sections for featured snippets

**Technical Optimization:**
✅ Website speed and performance
✅ Mobile responsiveness
✅ Schema markup implementation
✅ Internal linking structure

**Ready to begin?** Start with a comprehensive SEO audit!'''

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