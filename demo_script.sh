#!/bin/bash
# SafeScrap Demo Video Script - Automated

clear
echo "=========================================="
echo "   SafeScrap E-Waste Hazard Detector"
echo "   Powered by Gemma 4 E2B"
echo "=========================================="
echo ""
sleep 2

echo "🔋 Demo 1: Lithium-ion Battery Classification"
echo "----------------------------------------------"
sleep 1
python3 test_hazard_classification.py
echo ""
sleep 3

echo "📸 Demo 2: Image Classification"
echo "----------------------------------------------"
sleep 1
python3 test_multimodal.py
echo ""
sleep 3

echo "🎯 Demo 3: All Component Types"
echo "----------------------------------------------"
sleep 1
python3 test_all_classes.py
echo ""
sleep 2

echo "=========================================="
echo "   ✅ SafeScrap Demo Complete!"
echo "   GitHub: github.com/ayanuali/gemma4-hackathon"
echo "=========================================="
