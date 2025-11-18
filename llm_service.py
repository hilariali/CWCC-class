"""
LLM Service for Resource Chatbot
Handles AI-powered resource matching and conversation
"""

import streamlit as st
import openai
import json
import traceback
from typing import Dict, List, Optional, Tuple

class ResourceLLMService:
    """Service class for LLM-powered resource matching"""
    
    def __init__(self):
        """Initialize the LLM service"""
        self.client = None
        self.model = "meta-llama/Llama-3.3-70B-Instruct"  # Default model
    
    def _get_client(self):
        """Lazy initialization of OpenAI client"""
        if self.client is None:
            try:
                # Use the same configuration as other working tools
                self.client = openai.OpenAI(
                    api_key=st.secrets["OPENAI_API_KEY"],
                    base_url=st.secrets.get("OPENAI_BASE_URL"),
                )
            except Exception as e:
                self.client = None
        return self.client
    
    def create_system_prompt(self, safe_resource_index: List[Dict]) -> str:
        """Create system prompt with safe resource information"""
        # Create a simple list of resources for the AI
        resources_text = ""
        for resource in safe_resource_index:
            resources_text += f"- ID: {resource['id']}\n"
            resources_text += f"  Title: {resource['title']}\n"
            resources_text += f"  Group: {resource['group']}\n"
            resources_text += f"  Keywords: {', '.join(resource.get('keywords', []))}\n\n"
        
        return f"""You are a helpful AI assistant for the CWCC Resources Hub. Help users find the right resources.

AVAILABLE RESOURCES:
{resources_text}

INSTRUCTIONS:
1. Analyze the user's question and find the most relevant resource(s)
2. Return your response in this EXACT format:

RESOURCE_IDS: [list the resource IDs that match, separated by commas]
CONFIDENCE: [your confidence level from 0.0 to 1.0]
REASONING: [brief explanation of why these resources match]
RESPONSE: [friendly response to the user]

Example:
RESOURCE_IDS: venue-booking-form, facility-report-form
CONFIDENCE: 0.85
REASONING: User is asking about booking facilities and reporting issues
RESPONSE: I found resources for venue booking and facility reporting that should help you!

If no good match is found:
RESOURCE_IDS: 
CONFIDENCE: 0.0
REASONING: No suitable resources found
RESPONSE: I couldn't find specific resources for that. Could you try rephrasing your question?

MATCHING GUIDELINES:
- Look for keywords in titles, groups, and keywords
- Consider synonyms and related terms
- Only suggest resources that truly match the user's question
- Be helpful and accurate"""

    def match_resource(self, user_question: str, safe_resource_index: List[Dict]) -> Tuple[List[Dict], str]:
        """Use LLM to match user question to resources, returning up to 5 ranked results"""
        client = self._get_client()
        if not client:
            return [], "AI service is not available. Please try browsing the resources below."
        
        try:
            system_prompt = self.create_system_prompt(safe_resource_index)
            
            # Use the exact same format as working tools (dummy_tool1, dummy_tool2, youtube_quiz)
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
            )
            
            # Handle response exactly like working tools
            ai_response = response.choices[0].message.content
            if not ai_response:
                return [], "I received an empty response. Please try again."
            
            # Parse the structured response
            try:
                lines = ai_response.strip().split('\n')
                resource_ids_line = ""
                confidence_line = ""
                reasoning_line = ""
                response_line = ""
                
                for line in lines:
                    if line.startswith("RESOURCE_IDS:"):
                        resource_ids_line = line.replace("RESOURCE_IDS:", "").strip()
                    elif line.startswith("CONFIDENCE:"):
                        confidence_line = line.replace("CONFIDENCE:", "").strip()
                    elif line.startswith("REASONING:"):
                        reasoning_line = line.replace("REASONING:", "").strip()
                    elif line.startswith("RESPONSE:"):
                        response_line = line.replace("RESPONSE:", "").strip()
                
                # Process resource IDs
                valid_results = []
                valid_ids = [r["id"] for r in safe_resource_index]
                
                if resource_ids_line and resource_ids_line.strip():
                    resource_ids = [rid.strip() for rid in resource_ids_line.split(',') if rid.strip()]
                    confidence = float(confidence_line) if confidence_line else 0.5
                    
                    for i, resource_id in enumerate(resource_ids):
                        if resource_id in valid_ids:
                            valid_results.append({
                                "resource_id": resource_id,
                                "confidence": confidence - (i * 0.1),  # Slightly lower confidence for subsequent results
                                "reasoning": reasoning_line,
                                "rank": i + 1
                            })
                
                ai_message = response_line if response_line else "I found some resources that might help!"
                return valid_results, ai_message
                
            except Exception as e:
                return [], "I'm having trouble processing your request. Please try rephrasing your question or browse the resources below."
        
        except Exception as e:
            return [], "I'm experiencing technical difficulties. Please try browsing the resources below."

    def generate_conversational_response(self, user_question: str, matched_resource: Dict, conversation_history: List[Dict]) -> str:
        """Generate a more conversational response about the matched resource"""
        client = self._get_client()
        if not client:
            return f"I found **{matched_resource['title']}** which should help with your question!"
        
        try:
            # Create a focused prompt for conversational response
            prompt = f"""You are a helpful assistant for CWCC Resources Hub. 

The user asked: "{user_question}"

You found this resource:
- Title: {matched_resource['title']}
- Group: {matched_resource['group']}
- ID: {matched_resource['id']}

Generate a brief, friendly response (max 2 sentences) that:
1. Confirms you found the right resource
2. Briefly explains why it's relevant
3. Encourages the user to check the details

Be conversational and helpful, but don't make up details about the resource.
"""

            # Use the exact same format as working tools
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            
            result = response.choices[0].message.content
            return result if result else f"I found **{matched_resource['title']}** which should help with your question!"
            
        except Exception as e:
            st.error(f"Conversational response error: {e}")
            st.text(traceback.format_exc())
            # Fallback to simple response
            return f"Great! I found **{matched_resource['title']}** which should help with your question. Let me show you the details!"

    def test_connection(self):
        """Test the LLM connection with a simple request"""
        st.info("🧪 Testing LLM connection...")
        client = self._get_client()
        if not client:
            st.error("❌ Cannot test - client not available")
            return False
        
        try:
            st.info("📡 Sending test request...")
            # Use the exact same format as working tools
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello, respond with just 'OK'"}],
            )
            
            # Handle response exactly like working tools
            test_response = response.choices[0].message.content
            if test_response:
                st.success(f"✅ Test successful! Response: '{test_response}'")
                return True
            else:
                st.error("❌ Test failed: Received empty response")
                return False
            
        except Exception as e:
            st.error(f"❌ Test failed: {e}")
            st.error(f"🔍 Error type: {type(e).__name__}")
            st.text(traceback.format_exc())
            return False

# Global instance
llm_service = ResourceLLMService()