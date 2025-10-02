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
    
    # Otherwise, provide helpful general response with business focus
    return f'''🤔 **AuraSEO AI Response**

I see you asked: "*{user_input}*"

**Here's my business perspective:**

**General Business Advice:**
• Start with thorough market research
• Identify a specific target audience
• Create a unique value proposition
• Develop a solid business plan
• Focus on customer experience

**SEO & Digital Marketing Angle:**
• Build a professional website with clear messaging
• Optimize for local search if serving specific areas
• Create valuable content that addresses customer needs
• Use social media to build community and awareness
• Collect and showcase customer reviews

**Need more specific advice? Try:**
• "Food business marketing strategy"
• "Restaurant SEO tips" 
• "How to write a business plan"
• "Digital marketing for small business"

I'm here to help your business succeed through smart strategies and effective online presence!'''