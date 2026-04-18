#!/usr/bin/env python3
"""
SafeScrap Proof-of-Concept Demo
Simulates: Camera → AI Analysis → Hazard Warning
"""
import sys
import time
from safety_assessment import SafetyAssessment
from PIL import Image, ImageDraw, ImageFont


def print_header():
    """Print demo header"""
    print("\n" + "=" * 70)
    print("  SafeScrap - E-waste Hazard Detector")
    print("  Powered by Gemma 4 E2B")
    print("=" * 70)
    print()


def print_progress(message: str, duration: float = 1.0):
    """Animated progress indicator"""
    print(f"{message}...", end="", flush=True)
    dots = [".", "..", "..."]
    for i in range(3):
        time.sleep(duration / 3)
        print(f"\r{message}{dots[i]}   ", end="", flush=True)
    print("\r" + " " * 80, end="\r")  # Clear line


def create_demo_image(component_type: str) -> str:
    """Create demo image for testing (when no camera available)"""
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)

    if component_type == "battery":
        # Draw swollen battery
        draw.rectangle([100, 80, 300, 220], outline='black', width=3, fill='#FFE5E5')
        draw.rectangle([300, 120, 320, 180], fill='black')
        draw.ellipse([150, 100, 250, 200], outline='red', width=5)
        draw.text((185, 130), "!", fill='red', font=None)
        draw.text((140, 240), "SWOLLEN BATTERY", fill='black', font=None)

    elif component_type == "crt":
        # Draw CRT monitor
        draw.rectangle([80, 80, 320, 220], outline='black', width=3)
        draw.arc([100, 90, 300, 210], 0, 360, fill='gray', width=2)
        draw.text((150, 240), "CRT MONITOR", fill='black', font=None)

    elif component_type == "pcb":
        # Draw circuit board
        draw.rectangle([80, 80, 320, 220], fill='#006400', outline='black', width=2)
        # Draw components
        for x in range(100, 300, 40):
            for y in range(100, 200, 40):
                draw.rectangle([x, y, x+20, y+10], fill='black')
        draw.text((160, 240), "PCB", fill='black', font=None)

    elif component_type == "cable":
        # Draw cable
        draw.line([(80, 150), (320, 150)], fill='orange', width=15)
        draw.ellipse([70, 140, 90, 160], fill='orange')
        draw.ellipse([310, 140, 330, 160], fill='orange')
        draw.text((160, 240), "CABLE", fill='black', font=None)

    elif component_type == "capacitor":
        # Draw capacitor
        draw.rectangle([160, 100, 240, 200], fill='blue', outline='black', width=2)
        draw.line([(200, 200), (200, 220)], fill='black', width=3)
        draw.line([(200, 80), (200, 100)], fill='black', width=3)
        draw.text((150, 240), "CAPACITOR", fill='black', font=None)

    filepath = f"/tmp/demo_{component_type}.png"
    img.save(filepath)
    return filepath


def run_demo_image(component_type: str):
    """Run demo with generated image"""
    print_header()

    # Create demo image
    print(f"📷 Simulating camera capture of {component_type}...")
    image_path = create_demo_image(component_type)
    time.sleep(0.5)
    print(f"✓ Image captured: {image_path}\n")

    # Initialize assessment system
    print_progress("🤖 Initializing AI model (Gemma 4 E2B)", 1.0)
    assessor = SafetyAssessment()
    print("✓ AI model ready\n")

    # Perform analysis
    print_progress("🔍 Analyzing component with multimodal AI", 2.0)
    start_time = time.time()
    assessment = assessor.assess_component_image(image_path)
    duration = time.time() - start_time

    if 'error' in assessment:
        print(f"\n❌ Error: {assessment['error']}")
        return

    print(f"✓ Analysis complete ({duration:.1f}s)\n")

    # Generate and display warning
    warning = assessor.generate_safety_warning(assessment, format="text")
    print(warning)

    # Show classification details
    component = assessment['component']
    print("\nAI ANALYSIS DETAILS:")
    print("-" * 70)
    print(f"Identified as: {component['name']}")
    print(f"Confidence: {component['confidence']:.0%}")
    if component.get('identification_features'):
        print("\nIdentification features:")
        for feature in component['identification_features'][:3]:
            print(f"  • {feature}")

    # Show emergency contacts
    print("\n🚨 EMERGENCY CONTACTS:")
    print("-" * 70)
    contacts = assessment['emergency_contacts']
    print(f"  Emergency Services: {contacts['emergency_services']}")
    print(f"  Poison Control (US): {contacts['poison_control_us']}")
    print()


def run_demo_text(description: str):
    """Run demo with text description"""
    print_header()

    print(f"📝 Processing description: '{description}'\n")

    # Initialize assessment system
    print_progress("🤖 Initializing AI model (Gemma 4 E2B)", 1.0)
    assessor = SafetyAssessment()
    print("✓ AI model ready\n")

    # Perform analysis
    print_progress("🔍 Analyzing component with AI", 2.0)
    start_time = time.time()
    assessment = assessor.assess_component_text(description)
    duration = time.time() - start_time

    if 'error' in assessment:
        print(f"\n❌ Error: {assessment['error']}")
        return

    print(f"✓ Analysis complete ({duration:.1f}s)\n")

    # Generate and display warning
    warning = assessor.generate_safety_warning(assessment, format="text")
    print(warning)

    # Show emergency contacts
    print("\n🚨 EMERGENCY CONTACTS:")
    print("-" * 70)
    contacts = assessment['emergency_contacts']
    print(f"  Emergency Services: {contacts['emergency_services']}")
    print(f"  Poison Control (US): {contacts['poison_control_us']}")
    print()


def interactive_demo():
    """Interactive demo mode"""
    print_header()
    print("SafeScrap Interactive Demo")
    print("-" * 70)
    print("\nChoose demo mode:")
    print("  1. Test with simulated battery image")
    print("  2. Test with simulated CRT monitor image")
    print("  3. Test with simulated PCB image")
    print("  4. Test with text description")
    print("  5. Exit")
    print()

    while True:
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            run_demo_image("battery")
            break
        elif choice == "2":
            run_demo_image("crt")
            break
        elif choice == "3":
            run_demo_image("pcb")
            break
        elif choice == "4":
            description = input("\nEnter component description: ").strip()
            if description:
                run_demo_text(description)
            break
        elif choice == "5":
            print("\nThank you for using SafeScrap!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-5.")


def main():
    """Main demo function"""
    if len(sys.argv) > 1:
        # Command-line mode
        mode = sys.argv[1].lower()

        if mode in ["battery", "crt", "pcb", "cable", "capacitor"]:
            run_demo_image(mode)
        elif mode == "text":
            if len(sys.argv) > 2:
                description = " ".join(sys.argv[2:])
                run_demo_text(description)
            else:
                print("Usage: python3 safescrap_demo.py text <description>")
        else:
            print("Usage:")
            print("  python3 safescrap_demo.py [battery|crt|pcb|cable|capacitor]")
            print("  python3 safescrap_demo.py text <description>")
            print("  python3 safescrap_demo.py  (interactive mode)")
    else:
        # Interactive mode
        interactive_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
