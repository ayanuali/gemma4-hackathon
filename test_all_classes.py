#!/usr/bin/env python3
"""Test all 5 component classes"""
from component_classifier import ComponentClassifier

classifier = ComponentClassifier()

test_cases = [
    "A large bulky CRT monitor with curved glass screen",
    "Green circuit board with visible chips and capacitors",
    "Standard copper electrical cable with plastic insulation",
    "Old cylindrical capacitor with rust and visible corrosion"
]

print("Testing all 5 component classes:")
print()
print("=" * 60)

for desc in test_cases:
    result = classifier.classify_text(desc)
    if 'error' not in result:
        print(f"\nInput: {desc}")
        print(f"Classification: {result['component_class']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Hazard: {result['hazard_profile']['base_hazard'].upper()}")
        print(f"Time: {result['duration']:.2f}s")
    else:
        print(f"\nError: {result['error']}")

print("\n" + "=" * 60)
