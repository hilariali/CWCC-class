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
        """Initialize the LLM service with OpenAI client"""
        try:
            self.client = openai.OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"],
                base_url=st.secrets.get("OPENAI_BASE_URL"),
            )
            self.model = "DeepSeek-R1-Distill-Qwen-32B"  # Default model
            st.success("🧠 LLM Service initialized successfully")
        except Exception as e:
            st.error(f"Failed to initialize LLM service: {e}")
            st.text(traceback.format_exc())
            self.client = None
    
    def create_system_prompt(self, safe_resource_index: List[Dict]) -> str:
        """Create system prompt with safe resource information"""
        resources_json = json.dumps(safe_resource_index, indent=2)
        
        return f"""You are a helpful AI assistant for the CWCC Resources Hub. Your job is to help users find the right resources by matching their questions to available resources.

AVAILABLE RESOURCES:
{resources_json}

INSTRUCTIONS:
1. Analyze the user's question and find ALL relevant resources (up to 5 results)
2. Return ONLY a JSON response with this exact format (results MUST be ordered by confidence, highest first):
{{
    "results": [
        {{
            "resource_id": "exact-resource-id-from-list",
            "confidence": 0.95,
            "reasoning": "Brief explanation of why this resource matches",
            "rank": 1
        }},
        {{
            "resource_id": "another-resource-id-from-list",
            "confidence": 0.80,
            "reasoning": "Brief explanation of why this resource matches",
            "rank": 2
        }},
        {{
            "resource_id": "third-resource-id-from-list",
            "confidence": 0.65,
            "reasoning": "Brief explanation of why this resource matches",
            "rank": 3
        }}
    ],
    "response": "Friendly response mentioning how many matches were found and encouraging user to check them"
}}

3. If no good match is found (confidence < 0.4), return:
{{
    "results": [],
    "response": "I couldn't find any specific resources matching your query. Could you try rephrasing your question or browse the resources below?"
}}

MATCHING GUIDELINES:
- Look for keywords in titles, groups, and access information
- Consider synonyms and related terms
- Prioritize exact matches over partial matches
- Consider the context and intent of the user's question
- Return up to 5 results, ranked by confidence (highest first)
- Only include results with confidence > 0.4
- Be comprehensive - include all potentially relevant resources
- Order results by confidence level (highest confidence first)

SECURITY:
- Never make up resource IDs that don't exist in the list
- Only use the resource information provided above
- Don't expose sensitive details beyond what's in the safe index

RESPONSE STYLE:
- Be friendly and helpful
- Use natural language
- Explain why the resource is relevant
- If multiple resources could work, pick the best one
"""

    def match_resource(self, user_question: str, safe_resource_index: List[Dict]) -> Tuple[List[Dict], str]:
        """Use LLM to match user question to resources, returning up to 3 ranked results"""
        if not self.client:
            st.warning("⚠️ LLM client not available - using fallback")
            return [], "AI service is not available. Please try browsing the resources below."
        
        try:
            system_prompt = self.create_system_prompt(safe_resource_index)
            
            st.info(f"🤖 Sending query to LLM: {user_question[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.3,  # Lower temperature for more consistent responses
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content.strip()
            st.success(f"✅ LLM Response received: {len(ai_response)} characters")
            
            # Log the raw response for debugging
            with st.expander("🔍 Debug: Raw LLM Response", expanded=False):
                st.code(ai_response, language="json")
            
            # Parse JSON response
            try:
                result = json.loads(ai_response)
                results = result.get("results", [])
                ai_message = result.get("response", "I found some resources that might help!")
                
                # Validate and process results
                valid_results = []
                valid_ids = [r["id"] for r in safe_resource_index]
                
                for res in results:
                    resource_id = res.get("resource_id")
                    confidence = res.get("confidence", 0.0)
                    reasoning = res.get("reasoning", "")
                    rank = res.get("rank", 999)
                    
                    if resource_id and resource_id in valid_ids:
                        valid_results.append({
                            "resource_id": resource_id,
                            "confidence": confidence,
                            "reasoning": reasoning,
                            "rank": rank
                        })
                        st.info(f"📊 Match #{rank}: {resource_id} (confidence: {confidence:.2f})")
                    elif resource_id:
                        st.warning(f"⚠️ Invalid resource ID returned: {resource_id}")
                
                # Sort by confidence (higher confidence first), then by rank
                valid_results.sort(key=lambda x: (-x["confidence"], x["rank"]))
                
                return valid_results, ai_message
                
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON parsing failed: {e}")
                st.error(f"Raw response: {ai_response}")
                return [], "I'm having trouble processing your request. Please try rephrasing your question or browse the resources below."
        
        except Exception as e:
            st.error(f"❌ LLM service error: {e}")
            st.text(traceback.format_exc())
            return [], "I'm experiencing technical difficulties. Please try browsing the resources below."

    def generate_conversational_response(self, user_question: str, matched_resource: Dict, conversation_history: List[Dict]) -> str:
        """Generate a more conversational response about the matched resource"""
        if not self.client:
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

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Conversational response error: {e}")
            st.text(traceback.format_exc())
            # Fallback to simple response
            return f"Great! I found **{matched_resource['title']}** which should help with your question. Let me show you the details!"

# Global instance
llm_service = ResourceLLMService()