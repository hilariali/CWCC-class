#!/usr/bin/env python3
"""
Simple test to verify the lesson plan generator functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lesson_plan_generator import create_lesson_plan_prompt

def test_lesson_plan_prompt():
    """Test that the lesson plan prompt includes Science and Technology"""
    
    # Test with Science and Technology as a learning area
    age_group = "K2"
    theme = "Exploring Plants"
    num_sessions = 1
    language = "English"
    learning_areas = ["Science and Technology", "Nature and Living"]
    approaches = ["Hands-on experiments", "Outdoor exploration"]
    additional_notes = "Focus on local plants"
    
    prompt = create_lesson_plan_prompt(
        age_group, theme, num_sessions, language,
        learning_areas, approaches, additional_notes
    )
    
    # Verify the prompt contains the key elements
    assert "Science and Technology" in prompt
    assert "K2" in prompt
    assert "Exploring Plants" in prompt
    assert "English" in prompt
    assert "Hands-on experiments" in prompt
    assert "Focus on local plants" in prompt
    
    # Verify EDB curriculum requirements are included
    assert "Hong Kong EDB Kindergarten Education Curriculum Guide" in prompt
    assert "child-centred, play-based" in prompt
    assert "7 learning areas" in prompt
    
    # Verify all 7 EDB learning areas are listed
    expected_areas = [
        "Physical Fitness and Health",
        "Language (Chinese, English, or Putonghua)",
        "Early Mathematics",
        "Science and Technology",
        "Self and Society", 
        "Arts",
        "Nature and Living"
    ]
    
    for area in expected_areas:
        assert area in prompt
    
    print("✅ All tests passed!")
    print(f"✅ Science and Technology is included as learning area")
    print(f"✅ Prompt correctly formatted with all EDB requirements")
    return True

if __name__ == "__main__":
    test_lesson_plan_prompt()