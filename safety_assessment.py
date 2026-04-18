#!/usr/bin/env python3
"""
Integrated Safety Assessment System for SafeScrap
Combines component classification with hazard knowledge base
"""
from component_classifier import ComponentClassifier, COMPONENT_CLASSES
from hazard_knowledge_base import HazardKnowledgeBase, HazardInfo
from typing import Dict, List, Optional
import json


class SafetyAssessment:
    """Complete safety assessment for e-waste components"""

    def __init__(self):
        self.classifier = ComponentClassifier()
        self.knowledge_base = HazardKnowledgeBase()

    def assess_component_text(self, description: str, language: str = "en") -> Dict:
        """
        Perform complete safety assessment from text description

        Args:
            description: Text description of component
            language: Language for safety information (default: en)

        Returns:
            Complete safety assessment dict
        """
        # Classify component
        classification = self.classifier.classify_text(description)

        if 'error' in classification:
            return classification

        # Build safety assessment
        return self._build_assessment(classification, language)

    def assess_component_image(self, image_path: str, description: Optional[str] = None, language: str = "en") -> Dict:
        """
        Perform complete safety assessment from image

        Args:
            image_path: Path to component image
            description: Optional text description
            language: Language for safety information

        Returns:
            Complete safety assessment dict
        """
        # Classify component from image
        classification = self.classifier.classify_image(image_path, description)

        if 'error' in classification:
            return classification

        # Build safety assessment
        return self._build_assessment(classification, language)

    def _build_assessment(self, classification: Dict, language: str) -> Dict:
        """Build complete safety assessment from classification"""

        component_class = classification.get('component_class')
        hazard_profile = classification.get('hazard_profile', {})

        # Get detailed hazard information for each hazard
        detailed_hazards = []
        for hazard_id in hazard_profile.get('key_hazards', []):
            hazard_info = self.knowledge_base.get_hazard_info(hazard_id)
            if hazard_info:
                detailed_hazards.append({
                    'hazard_id': hazard_id,
                    'description': hazard_info.description,
                    'ghs_pictograms': hazard_info.ghs_pictograms,
                    'ppe_required': hazard_info.ppe_required,
                    'prevention': hazard_info.prevention,
                    'first_aid': hazard_info.first_aid,
                    'emergency_response': hazard_info.emergency_response
                })

        # Get PPE requirements for hazard level
        hazard_level = hazard_profile.get('base_hazard', 'unknown')
        ppe_requirements = self.knowledge_base.get_ppe_requirements(hazard_level)

        # Get emergency contacts
        emergency_contacts = self.knowledge_base.get_emergency_contacts()

        # Build comprehensive assessment
        assessment = {
            'component': {
                'type': component_class,
                'name': hazard_profile.get('name'),
                'confidence': classification.get('confidence'),
                'identification_features': hazard_profile.get('identification', [])
            },
            'hazard_assessment': {
                'level': hazard_level.upper(),
                'key_hazards': hazard_profile.get('key_hazards', []),
                'safety_precautions': hazard_profile.get('safety_precautions', []),
                'detailed_hazards': detailed_hazards
            },
            'ppe_requirements': ppe_requirements,
            'emergency_contacts': emergency_contacts,
            'classification_metadata': {
                'duration': classification.get('duration'),
                'reasoning': classification.get('reasoning', ''),
                'visual_observations': classification.get('visual_observations', [])
            }
        }

        return assessment

    def generate_safety_warning(self, assessment: Dict, format: str = "text") -> str:
        """
        Generate user-friendly safety warning

        Args:
            assessment: Safety assessment dict
            format: Output format ('text', 'markdown', or 'json')

        Returns:
            Formatted safety warning
        """
        if format == "json":
            return json.dumps(assessment, indent=2)

        component = assessment['component']
        hazard = assessment['hazard_assessment']
        ppe = assessment['ppe_requirements']

        if format == "markdown":
            return self._format_markdown_warning(component, hazard, ppe)
        else:
            return self._format_text_warning(component, hazard, ppe)

    def _format_text_warning(self, component: Dict, hazard: Dict, ppe: Dict) -> str:
        """Format as plain text warning"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"⚠️  SAFETY ASSESSMENT: {component['name'].upper()}")
        lines.append("=" * 70)
        lines.append(f"\nHAZARD LEVEL: {hazard['level']}")
        lines.append(f"Confidence: {component['confidence']:.0%}")
        lines.append("")

        lines.append("KEY HAZARDS:")
        for h in hazard['key_hazards']:
            lines.append(f"  • {h.replace('_', ' ').title()}")
        lines.append("")

        lines.append("SAFETY PRECAUTIONS:")
        for i, precaution in enumerate(hazard['safety_precautions'], 1):
            lines.append(f"  {i}. {precaution}")
        lines.append("")

        if ppe:
            lines.append("REQUIRED PPE:")
            for item in ppe['minimum_required']:
                lines.append(f"  • {item}")
            lines.append("")

            lines.append(f"WORK ENVIRONMENT: {ppe['work_environment']}")
            lines.append("")

        lines.append("=" * 70)

        return "\n".join(lines)

    def _format_markdown_warning(self, component: Dict, hazard: Dict, ppe: Dict) -> str:
        """Format as markdown warning"""
        lines = []
        lines.append(f"# ⚠️ SAFETY ASSESSMENT: {component['name'].upper()}")
        lines.append("")
        lines.append(f"**Hazard Level:** {hazard['level']}")
        lines.append(f"**Confidence:** {component['confidence']:.0%}")
        lines.append("")

        lines.append("## Key Hazards")
        for h in hazard['key_hazards']:
            lines.append(f"- {h.replace('_', ' ').title()}")
        lines.append("")

        lines.append("## Safety Precautions")
        for i, precaution in enumerate(hazard['safety_precautions'], 1):
            lines.append(f"{i}. {precaution}")
        lines.append("")

        if ppe:
            lines.append("## Required PPE")
            for item in ppe['minimum_required']:
                lines.append(f"- {item}")
            lines.append("")

            lines.append(f"**Work Environment:** {ppe['work_environment']}")
            lines.append("")

        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    import sys

    assessor = SafetyAssessment()

    # Test case
    if len(sys.argv) > 1:
        description = " ".join(sys.argv[1:])
    else:
        description = "Swollen lithium-ion battery from smartphone, showing visible deformation"

    print("SafeScrap Integrated Safety Assessment")
    print("=" * 70)
    print(f"Assessing: {description}")
    print()

    # Perform assessment
    assessment = assessor.assess_component_text(description)

    if 'error' in assessment:
        print(f"Error: {assessment['error']}")
    else:
        # Generate warning
        warning = assessor.generate_safety_warning(assessment, format="text")
        print(warning)

        # Show one detailed hazard example
        if assessment['hazard_assessment']['detailed_hazards']:
            hazard = assessment['hazard_assessment']['detailed_hazards'][0]
            print("\nDETAILED HAZARD INFORMATION:")
            print("-" * 70)
            print(f"Hazard: {hazard['hazard_id'].replace('_', ' ').title()}")
            print(f"GHS Pictograms: {', '.join(hazard['ghs_pictograms'])}")
            print("\nFirst Aid:")
            for item in hazard['first_aid'][:3]:
                print(f"  • {item}")
            print("\nEmergency Response:")
            for item in hazard['emergency_response'][:3]:
                print(f"  • {item}")
