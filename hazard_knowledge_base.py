#!/usr/bin/env python3
"""
Offline Hazard Knowledge Base for SafeScrap
GHS pictograms, safety data, first aid, and emergency procedures
"""
from typing import Dict, List, Optional
from dataclasses import dataclass

# GHS (Globally Harmonized System) Pictograms for E-waste Hazards
GHS_PICTOGRAMS = {
    "GHS02": {
        "name": "Flame",
        "description": "Flammable materials, self-reactive substances",
        "hazard_classes": ["Flammables", "Self-Reactives", "Pyrophorics", "Self-Heating", "Emits Flammable Gas", "Organic Peroxides"],
        "signal_word": "Danger",
        "examples_in_ewaste": ["Lithium-ion batteries", "Capacitors with certain electrolytes", "Magnesium components"]
    },
    "GHS03": {
        "name": "Flame Over Circle",
        "description": "Oxidizers that can cause or intensify fire",
        "hazard_classes": ["Oxidizing Gases", "Oxidizing Liquids", "Oxidizing Solids"],
        "signal_word": "Danger",
        "examples_in_ewaste": ["Certain battery chemistries", "Oxidizing agents in old batteries"]
    },
    "GHS04": {
        "name": "Gas Cylinder",
        "description": "Gases under pressure",
        "hazard_classes": ["Compressed Gas", "Liquefied Gas", "Dissolved Gas", "Refrigerated Liquefied Gas"],
        "signal_word": "Warning",
        "examples_in_ewaste": ["Aerosol cans", "Pressurized components", "CFC-containing refrigerants"]
    },
    "GHS05": {
        "name": "Corrosion",
        "description": "Corrosive to metals and causes severe skin burns/eye damage",
        "hazard_classes": ["Skin Corrosion/Burns", "Eye Damage", "Corrosive to Metals"],
        "signal_word": "Danger",
        "examples_in_ewaste": ["Battery acid", "Capacitor electrolyte", "Corroded component residues"]
    },
    "GHS06": {
        "name": "Skull and Crossbones",
        "description": "Acute toxicity (fatal or toxic)",
        "hazard_classes": ["Acute Toxicity (oral, dermal, inhalation)"],
        "signal_word": "Danger",
        "examples_in_ewaste": ["Mercury switches", "Lead solder", "Cadmium in batteries", "Beryllium oxide ceramics"]
    },
    "GHS07": {
        "name": "Exclamation Mark",
        "description": "Harmful, irritant, skin sensitizer, acute toxicity",
        "hazard_classes": ["Irritant (skin and eye)", "Skin Sensitizer", "Acute Toxicity (harmful)", "Narcotic Effects", "Respiratory Tract Irritation"],
        "signal_word": "Warning",
        "examples_in_ewaste": ["Plastic additives", "Flame retardants", "Certain solvents in electronics"]
    },
    "GHS08": {
        "name": "Health Hazard",
        "description": "Serious health hazards including carcinogenicity, respiratory sensitization, reproductive toxicity",
        "hazard_classes": ["Carcinogen", "Mutagenicity", "Reproductive Toxicity", "Respiratory Sensitizer", "Target Organ Toxicity", "Aspiration Hazard"],
        "signal_word": "Danger",
        "examples_in_ewaste": ["Asbestos in old components", "Brominated flame retardants", "PVC plastics", "Lead", "PCBs in old capacitors"]
    },
    "GHS09": {
        "name": "Environment",
        "description": "Hazardous to aquatic environment",
        "hazard_classes": ["Aquatic Toxicity (Acute and Chronic)"],
        "signal_word": "Warning",
        "examples_in_ewaste": ["Heavy metals", "Persistent organic pollutants", "PCBs", "Mercury"]
    }
}

# Hazard-specific safety information
HAZARD_SAFETY_DATA = {
    "fire_explosion_risk": {
        "ghs_pictograms": ["GHS02"],
        "description": "Risk of fire or explosion from thermal runaway, short circuit, or physical damage",
        "ppe_required": ["Fire-resistant gloves", "Safety goggles", "Fire extinguisher nearby"],
        "prevention": [
            "Store in cool, dry place away from heat sources",
            "Avoid physical damage or puncture",
            "Keep away from metal objects that could short circuit",
            "Use fire-resistant containers for storage and transport",
            "Do not expose to temperatures above 60°C (140°F)"
        ],
        "first_aid": [
            "If fire occurs, evacuate immediately",
            "Use Class D fire extinguisher for lithium fires",
            "Do NOT use water on lithium battery fires",
            "For burns, cool with running water for 10-20 minutes",
            "Seek immediate medical attention for burns"
        ],
        "emergency_response": [
            "Evacuate area and call emergency services",
            "Use ABC or Class D fire extinguisher",
            "If battery is smoking but not burning, move to open area if safe",
            "Allow to cool for several hours",
            "Do not handle until completely cooled"
        ]
    },
    "toxic_gas_release": {
        "ghs_pictograms": ["GHS06", "GHS08"],
        "description": "Release of toxic gases including hydrogen fluoride, phosphorus pentafluoride, or other harmful vapors",
        "ppe_required": ["Respirator (P100 or better)", "Chemical-resistant gloves", "Safety goggles", "Work in ventilated area"],
        "prevention": [
            "Work in well-ventilated area or outdoors",
            "Do not puncture or burn batteries",
            "Avoid heating components",
            "Use proper respiratory protection",
            "Keep away from sources of heat"
        ],
        "first_aid": [
            "Move to fresh air immediately",
            "If breathing is difficult, administer oxygen if available",
            "Call emergency services if exposure occurred",
            "For eye contact: Flush with water for 15 minutes",
            "Do not induce vomiting if swallowed",
            "Seek immediate medical attention"
        ],
        "emergency_response": [
            "Evacuate to fresh air",
            "Ventilate area thoroughly",
            "Use respiratory protection to approach source",
            "Isolate damaged component in sealed container",
            "Contact poison control: 1-800-222-1222 (US)"
        ]
    },
    "chemical_burns": {
        "ghs_pictograms": ["GHS05"],
        "description": "Corrosive chemicals can cause severe skin burns and eye damage",
        "ppe_required": ["Chemical-resistant gloves (nitrile or neoprene)", "Safety goggles or face shield", "Long sleeves and pants", "Closed-toe shoes"],
        "prevention": [
            "Wear appropriate PPE when handling",
            "Inspect for leaks or damage before handling",
            "Keep neutralizing agents nearby (baking soda for acids)",
            "Work on non-porous surface for easy cleanup",
            "Wash hands immediately after handling"
        ],
        "first_aid": [
            "Flush affected area with large amounts of water for 15-20 minutes",
            "Remove contaminated clothing while flushing",
            "For eyes: Flush with water for at least 15 minutes, seek immediate medical care",
            "Do NOT attempt to neutralize on skin",
            "Cover burns with clean, dry dressing",
            "Seek immediate medical attention for all chemical burns"
        ],
        "emergency_response": [
            "Isolate spilled material",
            "Use absorbent material to contain spill",
            "Neutralize acids with baking soda",
            "Dispose of waste according to local regulations",
            "Ventilate area"
        ]
    },
    "heavy_metal_contamination": {
        "ghs_pictograms": ["GHS06", "GHS08", "GHS09"],
        "description": "Exposure to toxic heavy metals including lead, mercury, cadmium, chromium",
        "ppe_required": ["Nitrile gloves", "Safety goggles", "Dust mask (N95 or better)", "Wash facilities"],
        "prevention": [
            "Minimize dust generation",
            "Work in well-ventilated area",
            "Use wet methods to control dust",
            "Wash hands thoroughly after handling",
            "Do not eat, drink, or smoke while handling",
            "Change clothes and shower after extended exposure"
        ],
        "first_aid": [
            "For skin contact: Wash with soap and water",
            "For inhalation: Move to fresh air",
            "For eye contact: Flush with water for 15 minutes",
            "If ingested: Do NOT induce vomiting, seek medical attention",
            "Seek medical attention if symptoms develop"
        ],
        "emergency_response": [
            "Contain spilled material without creating dust",
            "Use HEPA vacuum for cleanup",
            "Do not sweep dry material",
            "Seal contaminated materials in plastic bags",
            "Dispose through certified hazardous waste facility"
        ],
        "long_term_health_effects": {
            "lead": "Neurological damage, reproductive harm, developmental delays in children",
            "mercury": "Neurological damage, kidney damage, developmental harm",
            "cadmium": "Kidney damage, bone disease, cancer",
            "chromium_vi": "Lung cancer, skin ulcers, respiratory issues",
            "beryllium": "Chronic lung disease, cancer"
        }
    },
    "electrical_shock": {
        "ghs_pictograms": ["GHS02"],
        "description": "Risk of electric shock from capacitors, power supplies, or live circuits",
        "ppe_required": ["Insulated tools", "Non-conductive gloves", "Safety glasses"],
        "prevention": [
            "Verify power is disconnected",
            "Discharge capacitors before handling",
            "Use insulated tools",
            "Test circuits with multimeter before touching",
            "Avoid working on wet surfaces",
            "Never work alone on high-voltage equipment"
        ],
        "first_aid": [
            "Do NOT touch victim if still in contact with power source",
            "Turn off power source if possible",
            "Call emergency services (911) immediately",
            "Check for breathing and pulse",
            "Begin CPR if trained and needed",
            "Treat burns as thermal burns"
        ],
        "emergency_response": [
            "Cut power at main source if safe",
            "Use non-conductive object to separate victim from power",
            "Do not approach if high voltage is present",
            "Wait for emergency services with high-voltage situations"
        ]
    },
    "glass_fragmentation": {
        "ghs_pictograms": ["GHS07"],
        "description": "Risk of cuts and injuries from broken glass, especially CRT implosion",
        "ppe_required": ["Safety goggles or face shield", "Cut-resistant gloves", "Long sleeves", "Closed-toe shoes"],
        "prevention": [
            "Handle CRTs with extreme care",
            "Do not strike or drop glass components",
            "Transport in padded containers",
            "Discharge CRT before handling",
            "Work on padded surface"
        ],
        "first_aid": [
            "For cuts: Apply direct pressure to stop bleeding",
            "Do not remove embedded glass",
            "Clean wound with clean water",
            "Apply sterile dressing",
            "Seek medical attention for deep cuts or embedded glass",
            "For eye injuries: Do not rub, seek immediate medical care"
        ],
        "emergency_response": [
            "Carefully collect large pieces",
            "Use damp paper towels for small fragments",
            "Dispose in puncture-proof container",
            "Mark container as broken glass"
        ]
    },
    "toxic_fumes_when_heated": {
        "ghs_pictograms": ["GHS06", "GHS08"],
        "description": "Release of toxic fumes including dioxins, furans, and other harmful compounds when heated or burned",
        "ppe_required": ["Respirator with organic vapor cartridge", "Safety goggles", "Work outdoors or in fume hood"],
        "prevention": [
            "NEVER burn e-waste or plastics",
            "NEVER heat circuit boards to remove components",
            "Avoid soldering in poorly ventilated areas",
            "Do not use heat guns on plastics",
            "Work in well-ventilated area"
        ],
        "first_aid": [
            "Move to fresh air immediately",
            "If breathing is difficult, seek medical attention",
            "For eye irritation: Flush with water",
            "Monitor for delayed symptoms (24-48 hours)"
        ],
        "emergency_response": [
            "Evacuate area",
            "Ventilate thoroughly",
            "Do not re-enter until air is clear",
            "Seek medical evaluation if exposure occurred"
        ]
    }
}

# PPE (Personal Protective Equipment) recommendations by hazard level
PPE_BY_HAZARD_LEVEL = {
    "critical": {
        "minimum_required": [
            "Fire-resistant gloves (Kevlar or Nomex)",
            "Safety goggles with side shields or face shield",
            "Respirator (P100 or supplied air)",
            "Fire extinguisher (Class D for metals)",
            "Fire-resistant apron or clothing",
            "Non-conductive tools",
            "First aid kit"
        ],
        "recommended": [
            "Fire blanket",
            "Safety shower nearby",
            "Eye wash station",
            "Flame-resistant container for transport",
            "Buddy system (never work alone)"
        ],
        "work_environment": "Well-ventilated area or outdoors, fire-resistant work surface, fire extinguisher within 10 feet"
    },
    "high": {
        "minimum_required": [
            "Cut-resistant gloves",
            "Safety goggles or face shield",
            "Dust mask (N95 or P100)",
            "Long sleeves and pants",
            "Closed-toe shoes",
            "Insulated tools for electrical work"
        ],
        "recommended": [
            "Face shield for CRT work",
            "Rubber mat for electrical work",
            "Spill kit for chemical leaks",
            "Eye wash station access"
        ],
        "work_environment": "Well-ventilated area, padded work surface for glass, non-conductive surface for electrical"
    },
    "medium": {
        "minimum_required": [
            "Nitrile or latex gloves",
            "Safety glasses",
            "Dust mask (N95)",
            "Closed-toe shoes"
        ],
        "recommended": [
            "Long sleeves",
            "Work apron",
            "Hand washing station"
        ],
        "work_environment": "Ventilated area, clean work surface"
    },
    "low": {
        "minimum_required": [
            "Light-duty gloves",
            "Safety glasses"
        ],
        "recommended": [
            "Long sleeves if handling sharp edges",
            "Closed-toe shoes"
        ],
        "work_environment": "Clean, organized work area"
    }
}

# Emergency contact information
EMERGENCY_CONTACTS = {
    "global": {
        "emergency_services": "Check local emergency number",
        "poison_control_us": "1-800-222-1222",
        "poison_control_uk": "111",
        "poison_control_india": "1066 or 15454",
        "who_info": "https://www.who.int/emergencies"
    },
    "resources": {
        "safety_data_sheets": "https://pubchem.ncbi.nlm.nih.gov",
        "ewaste_recycling": "https://www.epa.gov/recycle/electronics-donation-and-recycling",
        "basel_convention": "https://www.basel.int (international e-waste guidance)",
        "osha_safety": "https://www.osha.gov/etools/computer-workstations"
    }
}


@dataclass
class HazardInfo:
    """Complete hazard information package"""
    hazard_id: str
    ghs_pictograms: List[str]
    description: str
    ppe_required: List[str]
    prevention: List[str]
    first_aid: List[str]
    emergency_response: List[str]
    additional_info: Optional[Dict] = None


class HazardKnowledgeBase:
    """Query offline hazard knowledge base"""

    def get_hazard_info(self, hazard_id: str) -> Optional[HazardInfo]:
        """Get complete information for a specific hazard"""
        if hazard_id not in HAZARD_SAFETY_DATA:
            return None

        data = HAZARD_SAFETY_DATA[hazard_id]
        return HazardInfo(
            hazard_id=hazard_id,
            ghs_pictograms=data["ghs_pictograms"],
            description=data["description"],
            ppe_required=data["ppe_required"],
            prevention=data["prevention"],
            first_aid=data["first_aid"],
            emergency_response=data["emergency_response"],
            additional_info=data.get("long_term_health_effects")
        )

    def get_ghs_pictogram(self, pictogram_id: str) -> Optional[Dict]:
        """Get GHS pictogram information"""
        return GHS_PICTOGRAMS.get(pictogram_id)

    def get_ppe_requirements(self, hazard_level: str) -> Optional[Dict]:
        """Get PPE requirements for hazard level"""
        return PPE_BY_HAZARD_LEVEL.get(hazard_level)

    def get_emergency_contacts(self, region: str = "global") -> Dict:
        """Get emergency contact information"""
        return EMERGENCY_CONTACTS.get(region, EMERGENCY_CONTACTS["global"])

    def get_all_hazards(self) -> List[str]:
        """List all available hazard IDs"""
        return list(HAZARD_SAFETY_DATA.keys())

    def search_hazards(self, keyword: str) -> List[str]:
        """Search hazards by keyword"""
        keyword_lower = keyword.lower()
        matches = []

        for hazard_id, data in HAZARD_SAFETY_DATA.items():
            if (keyword_lower in hazard_id.lower() or
                keyword_lower in data["description"].lower()):
                matches.append(hazard_id)

        return matches


# Example usage and CLI
if __name__ == "__main__":
    import sys

    kb = HazardKnowledgeBase()

    print("SafeScrap Offline Hazard Knowledge Base")
    print("=" * 60)
    print(f"\nAvailable hazards: {len(kb.get_all_hazards())}")
    print(f"GHS pictograms: {len(GHS_PICTOGRAMS)}")
    print()

    # Example: Fire hazard information
    if len(sys.argv) > 1:
        hazard_id = sys.argv[1]
    else:
        hazard_id = "fire_explosion_risk"

    print(f"Example: {hazard_id.upper()}")
    print("-" * 60)

    hazard = kb.get_hazard_info(hazard_id)
    if hazard:
        print(f"\nDescription: {hazard.description}")
        print(f"\nGHS Pictograms: {', '.join(hazard.ghs_pictograms)}")

        print("\nPPE Required:")
        for item in hazard.ppe_required:
            print(f"  • {item}")

        print("\nPrevention:")
        for item in hazard.prevention[:3]:  # Show first 3
            print(f"  • {item}")

        print("\nFirst Aid:")
        for item in hazard.first_aid[:3]:  # Show first 3
            print(f"  • {item}")

        print("\nEmergency Response:")
        for item in hazard.emergency_response[:3]:  # Show first 3
            print(f"  • {item}")

        if hazard.additional_info:
            print("\nAdditional Information:")
            for key, value in hazard.additional_info.items():
                print(f"  {key}: {value}")

    # Show PPE for critical hazard level
    print("\n" + "=" * 60)
    print("PPE Requirements for CRITICAL hazards:")
    print("-" * 60)
    ppe = kb.get_ppe_requirements("critical")
    if ppe:
        print("\nMinimum Required:")
        for item in ppe["minimum_required"]:
            print(f"  • {item}")

    # Emergency contacts
    print("\n" + "=" * 60)
    print("Emergency Contacts:")
    print("-" * 60)
    contacts = kb.get_emergency_contacts()
    for key, value in contacts.items():
        print(f"  {key}: {value}")
