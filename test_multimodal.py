#!/usr/bin/env python3
"""
Test Gemma 4 E2B multimodal capabilities (image + text)
"""
import json
import base64
import time
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:e2b"

def classify_image(image_path, prompt):
    """Send image + text prompt to Gemma 4"""
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [image_data],
        "stream": False,
        "temperature": 0.1
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

print("Testing Gemma 4 E2B multimodal capabilities...")
print("=" * 60)

# First, let's create a simple test image using PIL
try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create test image of a battery warning
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple battery shape
    draw.rectangle([100, 80, 300, 220], outline='black', width=3)
    draw.rectangle([300, 120, 320, 180], fill='black')
    
    # Add warning symbol
    draw.ellipse([150, 100, 250, 200], outline='red', width=5)
    draw.text((180, 130), "!", fill='red', font=None)
    
    # Save test image
    test_img_path = '/tmp/test_battery.png'
    img.save(test_img_path)
    print(f"Created test image: {test_img_path}")
    
    # Test multimodal classification
    prompt = """Describe this image and identify any potential e-waste hazards. 
Provide your response as JSON with: component_type, hazard_level, and hazards."""
    
    print(f"\nSending image to Gemma 4 E2B...")
    result = classify_image(test_img_path, prompt)
    
    if "error" in result:
        print(f"ERROR: {result['error']}")
    else:
        print(f"\nResponse time: {result['duration']:.2f}s")
        print(f"Tokens generated: {result['tokens']}")
        print(f"\nOutput:\n{result['response']}")
    
except ImportError:
    print("PIL not available - installing pillow...")
    import subprocess
    subprocess.run(['pip3', 'install', '--user', 'pillow'], check=True)
    print("Pillow installed. Please run script again.")

print("\n" + "=" * 60)
