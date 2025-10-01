def generate_sample_content(user_input):
    """Generate professional, natural-sounding SEO content"""
    
    input_lower = user_input.lower()
    
    # Extract the main topic more intelligently
    if "coffee" in input_lower or "cafe" in input_lower:
        content = f'''**Perfect Meta Description for Coffee Shop:**

"☕ Morning Brew Cafe - Experience artisanal coffee in a cozy atmosphere. Freshly roasted beans, friendly service, and the perfect brew await you. Visit us today!"

**Why This Works:**
• Includes emoji (☕) for visual appeal
• Highlights unique selling points (artisanal, freshly roasted)
• Clear call-to-action ("Visit us today")
• Perfect length for SEO (under 160 characters)
• Uses sensory words (cozy atmosphere, perfect brew)'''

    elif "restaurant" in input_lower or "dining" in input_lower:
        content = f'''**Compelling Meta Description for Restaurant:**

"🍽️ [Restaurant Name] - Exceptional dining experience with chef-crafted dishes, warm ambiance, and impeccable service. Make your reservation today!"

**Key Elements:**
• Food emoji (🍽️) grabs attention
• Emphasizes quality (chef-crafted, impeccable service)
• Creates desire (exceptional dining experience)
• Strong call-to-action (reservation)'''

    elif any(word in input_lower for word in ['meta', 'description']):
        # Extract the business type more accurately
        business_type = extract_business_type_v2(user_input)
        
        content = f'''**Professional Meta Description for {business_type.title()}:**

"Discover exceptional quality and outstanding service at [Business Name]. Our {business_type} offers customized solutions to meet your unique needs. Contact us today!"

**SEO Optimized Features:**
• Includes primary keyword "{business_type}"
• Clear value proposition
• Call-to-action drives conversions
• Professional tone builds trust
• Ideal length for search results'''

    elif any(word in input_lower for word in ['blog', 'article', 'post']):
        topic = extract_topic_v2(user_input)
        content = f'''**SEO-Optimized Blog Post: "{topic.title()}"**

**Engaging Title:** "The Complete Guide to {topic.title()} in 2024: Tips, Trends, and Strategies"

**Compelling Introduction:**
In today's competitive landscape, understanding {topic} is more important than ever. This comprehensive guide covers everything you need to know to succeed.

**Key Sections:**
1. Current Market Trends and Insights
2. Proven Strategies for Success
3. Common Mistakes to Avoid
4. Future Outlook and Opportunities

**Target Keywords:**
- {topic} services
- best {topic} strategies  
- {topic} for beginners
- professional {topic} solutions'''

    else:
        topic = extract_topic_v2(user_input)
        content = f'''**AuraSEO AI Professional Content for "{topic.title()}":**

**Optimized Meta Description:**
"Transform your {topic} with our expert solutions. Get measurable results, professional guidance, and sustainable growth. Start your journey today!"

**Content Strategy:**
✅ **Primary Focus:** {topic} optimization and results
✅ **Target Audience:** Businesses seeking {topic} improvement
✅ **Key Messaging:** Professional expertise + measurable outcomes
✅ **Call-to-Action:** Begin with consultation/assessment

**Recommended Approach:**
1. Comprehensive {topic} audit and analysis
2. Customized strategy development
3. Implementation with ongoing support
4. Performance monitoring and optimization'''

    return jsonify({
        "success": True, 
        "result": content,
        "message": "AuraSEO AI Professional Content"
    })

def extract_topic_v2(text):
    """Better topic extraction"""
    text_lower = text.lower()
    
    # Common business types
    business_types = ['coffee', 'cafe', 'restaurant', 'shop', 'store', 'service', 'consulting', 'agency']
    
    for business in business_types:
        if business in text_lower:
            return business
    
    # Extract words after "for" or the main nouns
    words = text_lower.split()
    if 'for' in words:
        index = words.index('for')
        return ' '.join(words[index+1:index+3]) if index + 1 < len(words) else "your business"
    
    # Return the most substantial word
    substantial_words = [word for word in words if len(word) > 3 and word not in ['write', 'create', 'make', 'generate', 'meta', 'description', 'blog']]
    return substantial_words[0] if substantial_words else "your business"

def extract_business_type_v2(text):
    """Better business type extraction"""
    text_lower = text.lower()
    
    business_mapping = {
        'coffee': 'coffee shop',
        'cafe': 'coffee shop', 
        'restaurant': 'restaurant',
        'shop': 'retail store',
        'store': 'retail store',
        'service': 'service provider',
        'consult': 'consulting firm',
        'agency': 'marketing agency'
    }
    
    for key, value in business_mapping.items():
        if key in text_lower:
            return value
    
    return "business"