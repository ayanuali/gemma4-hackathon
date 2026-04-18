#!/usr/bin/env python3
"""
Component Classifier for SafeScrap E-waste Hazard Detector
Classifies e-waste components into 5 categories and provides hazard profiles
"""
import json
import base64
import time
import re
import requests
from typing import Dict, Optional, List

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:e2b"


def extract_json_from_response(response_text: str) -> str:
    """Extract JSON from markdown code blocks or plain text"""
    # Try to find JSON in markdown code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
        return json_match.group(1)

    # Try to find raw JSON object
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        return json_match.group(0)

    return response_text

# Define 5 component classes with hazard profiles
COMPONENT_CLASSES = {
    "lithium_ion_battery": {
        "name": "Lithium-ion Battery",
        "base_hazard": "critical",
        "key_hazards": [
            "fire_explosion_risk",
            "toxic_gas_release",
            "chemical_burns",
            "thermal_runaway"
        ],
        "safety_precautions": [
            "Do NOT puncture, crush, or disassemble",
            "Store in cool, dry place away from metal objects",
            "If swollen, treat as immediate fire hazard",
            "Discharge before disposal",
            "Use fire-resistant container for transport"
        ],
        "identification": [
            "Rectangular or cylindrical shape",
            "May be swollen or deformed",
            "Often labeled with voltage (3.7V, 7.4V, etc.)",
            "Found in phones, laptops, power tools"
        ]
    },
    "crt_screen": {
        "name": "CRT Monitor/TV Screen",
        "base_hazard": "high",
        "key_hazards": [
            "lead_content",
            "heavy_metals",
            "glass_fragmentation",
            "high_voltage_capacitor",
            "toxic_phosphor_coating"
        ],
        "safety_precautions": [
            "Wear safety goggles and gloves",
            "Do NOT break the vacuum tube",
            "Discharge high-voltage capacitor before handling",
            "Avoid breathing dust from screen coating",
            "Requires specialized recycling facility"
        ],
        "identification": [
            "Large, bulky glass screen",
            "Heavy weight (10-30 kg typical)",
            "Curved front glass",
            "Found in old monitors and TVs (pre-2010s)"
        ]
    },
    "pcb": {
        "name": "Printed Circuit Board",
        "base_hazard": "medium",
        "key_hazards": [
            "heavy_metal_contamination",
            "brominated_flame_retardants",
            "lead_solder",
            "toxic_fumes_when_heated"
        ],
        "safety_precautions": [
            "Wear gloves when handling",
            "Do NOT burn or heat PCBs",
            "Avoid breathing dust from damaged boards",
            "Wash hands after handling",
            "Remove batteries and capacitors before processing"
        ],
        "identification": [
            "Green, blue, or brown flat board",
            "Visible electronic components (chips, resistors, capacitors)",
            "Copper traces/circuits visible",
            "Found in all electronic devices"
        ]
    },
    "cable": {
        "name": "Electrical Cable",
        "base_hazard": "low",
        "key_hazards": [
            "electrical_shock",
            "fire_risk_if_damaged",
            "PVC_toxic_fumes_when_burned",
            "copper_theft_related_hazards"
        ],
        "safety_precautions": [
            "Ensure disconnected from power source",
            "Check for exposed wires",
            "Do NOT burn to recover copper",
            "Use proper wire cutters",
            "Recycle copper through certified facilities"
        ],
        "identification": [
            "Flexible insulated wire",
            "Various colors and thicknesses",
            "Copper or aluminum conductor inside",
            "Common in all electronic devices and appliances"
        ]
    },
    "capacitor": {
        "name": "Capacitor",
        "base_hazard": "medium",
        "key_hazards": [
            "stored_electrical_charge",
            "chemical_leakage",
            "explosion_if_overheated",
            "pcb_contamination_in_older_units"
        ],
        "safety_precautions": [
            "Discharge before handling (use insulated tool)",
            "Wear gloves if electrolyte visible",
            "Do NOT puncture or heat",
            "Older capacitors may contain PCBs - handle with extreme care",
            "Store in dry container"
        ],
        "identification": [
            "Cylindrical or rectangular component",
            "Two leads/terminals",
            "Often labeled with capacitance value",
            "May show rust, corrosion, or swelling",
            "Found on PCBs and in power supplies"
        ]
    }
}


class ComponentClassifier:
    """
    Classifies e-waste components and provides hazard information
    """

    def __init__(self, model: str = MODEL, ollama_url: str = OLLAMA_URL):
        self.model = model
        self.ollama_url = ollama_url

    def classify_text(self, description: str) -> Dict:
        """
        Classify component from text description

        Args:
            description: Text description of the component

        Returns:
            Dict with component_class, confidence, hazard_profile
        """
        component_list = ', '.join([v['name'] for v in COMPONENT_CLASSES.values()])

        prompt = f"""You are an e-waste component classifier. Classify this component into ONE of these categories:
{component_list}

Component description: {description}

Respond with ONLY a JSON object in this exact format:
{{
  "component_class": "one of: lithium_ion_battery, crt_screen, pcb, cable, capacitor",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}}"""

        result = self._call_model(prompt)

        if 'error' in result:
            return result

        try:
            # Extract JSON from markdown code blocks if present
            json_text = extract_json_from_response(result['response'])
            classification = json.loads(json_text)
            component_class = classification.get('component_class', 'unknown')

            # Get full hazard profile
            if component_class in COMPONENT_CLASSES:
                classification['hazard_profile'] = COMPONENT_CLASSES[component_class]

            classification['duration'] = result['duration']
            return classification

        except json.JSONDecodeError as e:
            return {
                'error': f'Failed to parse JSON response: {e}',
                'raw_response': result.get('response', '')
            }

    def classify_image(self, image_path: str, description: Optional[str] = None) -> Dict:
        """
        Classify component from image (with optional text description)

        Args:
            image_path: Path to image file
            description: Optional text description to supplement image

        Returns:
            Dict with component_class, confidence, hazard_profile
        """
        component_list = ', '.join([v['name'] for v in COMPONENT_CLASSES.values()])

        context = f"Additional context: {description}" if description else ""

        prompt = f"""You are an e-waste component classifier. Analyze this image and classify the component into ONE of these categories:
{component_list}

{context}

Respond with ONLY a JSON object in this exact format:
{{
  "component_class": "one of: lithium_ion_battery, crt_screen, pcb, cable, capacitor",
  "confidence": 0.0-1.0,
  "visual_observations": ["list of what you see"],
  "reasoning": "brief explanation"
}}"""

        # Read and encode image
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            return {'error': f'Failed to read image: {e}'}

        result = self._call_model(prompt, images=[image_data])

        if 'error' in result:
            return result

        try:
            # Extract JSON from markdown code blocks if present
            json_text = extract_json_from_response(result['response'])
            classification = json.loads(json_text)
            component_class = classification.get('component_class', 'unknown')

            # Get full hazard profile
            if component_class in COMPONENT_CLASSES:
                classification['hazard_profile'] = COMPONENT_CLASSES[component_class]

            classification['duration'] = result['duration']
            return classification

        except json.JSONDecodeError as e:
            return {
                'error': f'Failed to parse JSON response: {e}',
                'raw_response': result.get('response', '')
            }

    def get_hazard_profile(self, component_class: str) -> Optional[Dict]:
        """
        Get detailed hazard profile for a component class

        Args:
            component_class: One of the 5 component classes

        Returns:
            Hazard profile dict or None if not found
        """
        return COMPONENT_CLASSES.get(component_class)

    def list_component_classes(self) -> List[str]:
        """Return list of all component classes"""
        return list(COMPONENT_CLASSES.keys())

    def _call_model(self, prompt: str, images: Optional[List[str]] = None) -> Dict:
        """
        Internal method to call Ollama API

        Args:
            prompt: Text prompt
            images: Optional list of base64-encoded images

        Returns:
            Dict with response, duration, tokens
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1  # Low temperature for consistent classification
        }

        if images:
            payload['images'] = images

        try:
            start = time.time()
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            duration = time.time() - start

            if response.status_code == 200:
                result = response.json()
                return {
                    "response": result.get("response", ""),
                    "duration": duration,
                    "tokens": result.get("eval_count", 0)
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text,
                    "duration": duration
                }
        except Exception as e:
            return {"error": f"Request failed: {e}"}


# Example usage
if __name__ == "__main__":
    classifier = ComponentClassifier()

    print("SafeScrap Component Classifier")
    print("=" * 50)
    print(f"Available classes: {', '.join(classifier.list_component_classes())}")
    print()

    # Test classification
    test_description = "A swollen rectangular battery pack from a smartphone"
    print(f"Testing: {test_description}")
    result = classifier.classify_text(test_description)

    if 'error' not in result:
        print(f"\nClassification: {result['component_class']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"Duration: {result['duration']:.2f}s")

        if 'hazard_profile' in result:
            profile = result['hazard_profile']
            print(f"\nHazard Level: {profile['base_hazard'].upper()}")
            print(f"Key Hazards: {', '.join(profile['key_hazards'])}")
    else:
        print(f"Error: {result['error']}")
