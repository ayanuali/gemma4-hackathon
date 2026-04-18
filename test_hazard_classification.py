#!/usr/bin/env python3
"""
Test Gemma 4 E2B for e-waste hazard classification
"""
import json
import time
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:e2b"

def classify_hazard(component_description):
    """Classify hazard level of e-waste component"""
    prompt = f"""You are an e-waste safety expert. Classify the hazard level of this component:

Component: {component_description}

Respond with ONLY a JSON object in this format:
{{
  "hazard_level": "low"|"medium"|"high"|"critical",
  "hazards": ["list", "of", "hazards"],
  "safety_precautions": ["list", "of", "precautions"]
}}"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1  # Low temperature for consistent classification
    }
    
    start = time.time()
    response = requests.post(OLLAMA_URL, json=payload)
    duration = time.time() - start
    
    if response.status_code == 200:
        result = response.json()
        return {
            "response": result.get("response", ""),
            "duration": duration,
            "tokens": result.get("eval_count", 0)
        }
    else:
        return {"error": response.text, "duration": duration}

# Test cases
test_components = [
    "Lithium-ion battery from smartphone (swollen)",
    "CRT monitor screen",
    "Printed circuit board with visible capacitors",
    "Standard copper electrical cable",
    "Old capacitor with visible rust"
]

print("Testing Gemma 4 E2B for hazard classification...\n")
print("=" * 60)

for i, component in enumerate(test_components, 1):
    print(f"\n[Test {i}/5] Component: {component}")
    print("-" * 60)
    
    result = classify_hazard(component)
    
    if "error" in result:
        print(f"ERROR: {result['error']}")
    else:
        print(f"Response time: {result['duration']:.2f}s")
        print(f"Tokens generated: {result['tokens']}")
        print(f"Output:\n{result['response']}")

print("\n" + "=" * 60)
print("Test complete!")
