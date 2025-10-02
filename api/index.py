from flask import Flask, request, jsonify
import os
import requests
import json

app = Flask(__name__)

# DeepSeek API configuration
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_smart_response(user_input):
    """Generate appropriate response based on question type"""
    
    input_lower = user_input.lower()
    
    # Detect question types
    seo_keywords = ['seo', 'meta', 'description', 'keyword', 'blog', 'content', 'website', 'google', 'rank', 'search', 'optimiz', 'traffic']
    business_keywords = ['business', 'startup', 'company', 'enterprise', 'venture', 'profit', 'revenue', 'industry', 'market']
    food_keywords = ['food', 'restaurant', 'cafe', 'coffee', 'culinary', 'menu', 'dining', 'eat', 'food truck']
    
    is_seo_question = any(keyword in input_lower for keyword in seo_keywords)
    is_business_question = any(keyword in input_lower for keyword in business_keywords)
    is_food_question = any(keyword in input_lower for keyword in food_keywords)
    
    # Check if it's a known general question first
    general_questions = {
        'why people sleep at night': '''🌙 **Why People Sleep at Night?**

**Biological Reasons:**
• **Circadian Rhythm:** Our internal body clock is programmed for daytime activity and nighttime rest
• **Melatonin Production:** Darkness triggers melatonin, the sleep hormone
• **Evolution:** Humans evolved to be daytime hunters/gatherers - night was dangerous

**Practical Benefits:**
• **Safety:** Reduced risk of accidents in darkness
• **Social Coordination:** Aligns with societal schedules
• **Temperature:** Cooler nights promote better sleep''',

        'how can make a good business in food industry': '''🍽️ **How to Build a Successful Food Business**

**Step 1: Market Research & Niche Selection**
• **Identify Your Niche:** Restaurant, food truck, catering, bakery, specialty foods
• **Target Audience:** Families, students, professionals, health-conscious consumers
• **Location Analysis:** Foot traffic, competition, demographics

**Step 2: Business Foundation**
• **Unique Selling Proposition:** What makes you different?
• **Business Plan:** Financial projections, marketing strategy, operations
• **Legal Structure:** LLC, corporation, sole proprietorship
• **Licenses & Permits:** Health department, business license, food handler certificates

**Step 3: Menu & Operations**
• **Signature Dishes:** Create memorable, photogenic menu items
• **Supplier Relationships:** Reliable, quality ingredient sources
• **Kitchen Efficiency:** Streamlined processes for consistency
• **Pricing Strategy:** Competitive yet profitable

**Step 4: Marketing & Customer Experience**
• **Brand Identity:** Logo, colors, packaging, atmosphere
• **Digital Presence:** Website, social media, online ordering
• **Customer Service:** Training staff for exceptional experiences
• **Loyalty Programs:** Repeat customer incentives

**Step 5: SEO & Online Visibility**
• **Google Business Profile:** Complete optimization with photos and reviews
• **Local SEO:** "Food near me" keyword targeting
• **Content Marketing:** Blog about recipes, food trends, behind-the-scenes
• **Review Management:** Encourage and respond to customer reviews

**Common Food Business Mistakes to Avoid:**
❌ Underestimating startup costs
❌ Poor location choice  
❌ Inconsistent food quality
❌ Neglecting online presence
❌ Not adapting to customer feedback

**Success Formula:** Great Food + Excellent Service + Smart Marketing = Profitable Business!''',

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
• Experiment with grind size''',

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

I'm your professional SEO and business assistant! I can help you with:

**SEO Services:**
• Meta descriptions and title tags
• Keyword research and strategy  
• Content optimization
• SEO audits and recommendations

**Business Advice:**
• Business planning and strategy
• Marketing and branding
• Industry-specific insights
• Growth strategies

**Content Creation:**
• Blog post outlines
• Marketing copy
• Social media content

**Just ask me anything! I'm here to help your business grow.**'''
    }
    
    # Check if it's a known general question
    for question, answer in general_questions.items():
        if question in input_lower:
            return answer
    
    # Food business questions
    if is_food_question and is_business_question:
        return '''🍕 **Food Business Success Guide**

**Essential Steps for Food Business Success:**

**1. Find Your Unique Angle**
• **Specialty Focus:** Vegan, gluten-free, ethnic cuisine, fusion
• **Experience-Based:** Live cooking, interactive dining, themed events
• **Convenience-Focused:** Delivery-only, meal kits, grab-and-go

**2. Master the Fundamentals**
• **Consistent Quality:** Every customer gets the same great experience
• **Cost Control:** Food costs (28-35%), labor (25-30%), overhead (15-20%)
• **Supplier Management:** Reliable, quality-focused partnerships

**3. Build Your Brand**
• **Memorable Name & Logo:** Easy to remember and recognize
• **Atmosphere & Ambiance:** Matches your target audience
• **Storytelling:** Share your passion and journey

**4. Digital Marketing Strategy**
• **Google Business Optimization:** Complete profile with photos and menu
• **Social Media Presence:** Instagram-friendly food photos
• **Local SEO:** "Best [cuisine] near me" optimization
• **Review Management:** 4+ star ratings are essential

**5. Customer Experience Excellence**
• **Staff Training:** Knowledgeable, friendly, efficient
• **Cleanliness:** Spotless facilities build trust
• **Feedback Systems:** Listen and adapt to customer needs

**Food Industry SEO Tips:**
• Optimize for "food delivery near me" searches
• Create blog content about local ingredients
• Use schema markup for menus and reviews
• Target long-tail keywords like "best pizza in [city]"

**Remember:** In food business, your reputation is everything!'''
    
    # Business strategy questions
    elif is_business_question:
        return '''💼 **Business Success Framework**

**Building a Successful Business:**

**Phase 1: Foundation**
• **Market Research:** Identify needs, competition, opportunities
• **Business Model:** How you'll make money and deliver value
• **Target Audience:** Specific customer profiles and pain points

**Phase 2: Planning**
• **Value Proposition:** Why customers should choose you
• **Financial Projections:** Realistic revenue and expense forecasts
• **Marketing Strategy:** How you'll attract and retain customers

**Phase 3: Execution**
• **Minimum Viable Product:** Start small, test, and iterate
• **Customer Acquisition:** Cost-effective channels that work
• **Operations:** Efficient processes and systems

**Phase 4: Growth**
• **Scale Smartly:** Don't grow faster than you can manage
• **Team Building:** Hire for culture and competence
• **Innovation:** Continuously improve and adapt

**Business SEO Connection:**
• Create content that answers customer questions
• Build authority in your industry
• Use local SEO if serving specific areas
• Leverage reviews and testimonials

**Key Success Factors:**
✅ Solve real problems
✅ Exceptional customer service  
✅ Smart financial management
✅ Adaptability to market changes'''
    
    # If it's clearly an SEO question, provide SEO content
    if is_seo_question:
        return generate_seo_content(user_input)
    
    # Otherwise, use DeepSeek API for more complex queries
    return call_deepseek_api(user_input)

def generate_seo_content(user_input):
    """Generate SEO-specific content"""
    seo_responses = {
        'meta': '''📝 **Meta Description Best Practices**

**What Makes Great Meta Descriptions:**
• **Length:** 150-160 characters (Google may truncate longer ones)
• **Keyword Placement:** Include primary keyword naturally
• **Call-to-Action:** Encourage clicks with action words
• **Unique:** Every page should have different meta descriptions

**Formula:** Primary Keyword + Value Proposition + CTA

**Example:** "Professional SEO services to boost your website traffic and rankings. Get more qualified leads. Free audit available!"''',

        'keyword': '''🔍 **Keyword Research Strategy**

**Types of Keywords:**
• **Short-tail:** Broad, high-competition (e.g., "SEO")
• **Long-tail:** Specific, lower competition (e.g., "SEO for small business in Chicago")
• **Location-based:** Include geographic modifiers
• **Question-based:** Answer user queries directly

**Tools to Use:**
• Google Keyword Planner
• SEMrush
• Ahrefs
• UberSuggest

**Pro Tip:** Focus on user intent, not just search volume!''',

        'content': '''📄 **SEO Content Creation**

**Pillar Content Strategy:**
1. **Pillar Page:** Comprehensive guide on core topic
2. **Cluster Content:** Supporting articles on subtopics
3. **Internal Linking:** Connect related content

**Content Quality Factors:**
✅ Original research and insights
✅ Comprehensive coverage of topic
✅ Readable structure with headings
✅ Visual elements (images, videos)
✅ Regular updates for freshness'''
    }
    
    input_lower = user_input.lower()
    for keyword, response in seo_responses.items():
        if keyword in input_lower:
            return response
    
    return call_deepseek_api(user_input)

def call_deepseek_api(user_input):
    """Call DeepSeek API for advanced responses"""
    
    if not DEEPSEEK_API_KEY:
        return "🔧 **AuraSEO AI Update**\n\nI'm currently being upgraded with advanced AI capabilities. Please check back soon for enhanced responses!"
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": """You are AuraSEO AI, a professional SEO and business consultant. 
                    Provide helpful, actionable advice about SEO, digital marketing, business strategy, 
                    and entrepreneurship. Keep responses professional yet approachable. 
                    Use bullet points and emojis where appropriate. Focus on practical, 
                    implementable strategies."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")  # For debugging
        return f"⚠️ **I'm experiencing technical difficulties**\n\nPlease try again in a moment. For now, here's my standard advice:\n\n{generate_fallback_response(user_input)}"

def generate_fallback_response(user_input):
    """Generate fallback response when API fails"""
    return f'''🤔 **AuraSEO AI Response**

I see you asked: "*{user_input}*"

**General Business & SEO Advice:**

**For Business Success:**
• Start with thorough market research
• Identify your unique value proposition  
• Create a customer-focused business plan
• Build strong online presence

**For SEO Success:**
• Optimize your website for user experience
• Create valuable, relevant content
• Build quality backlinks naturally
• Use local SEO if serving specific areas

**Need specific help? Try asking about:**
• "Restaurant marketing strategy"
• "Small business SEO tips"
• "Content marketing for beginners"
• "Social media marketing"

I'm here to help your business grow through smart digital strategies!'''

@app.route('/')
def home():
    return jsonify({
        "message": "AuraSEO AI API is running!",
        "status": "success",
        "endpoints": {
            "/chat": "POST - Send user messages to AI",
            "/health": "GET - Check API status"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "AuraSEO AI"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' in request body",
                "status": "error"
            }), 400
        
        user_message = data['message']
        
        if not user_message.strip():
            return jsonify({
                "error": "Message cannot be empty",
                "status": "error"
            }), 400
        
        # Generate response using our smart system
        response = generate_smart_response(user_message)
        
        return jsonify({
            "response": response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)