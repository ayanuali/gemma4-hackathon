# 🎬 HACKATHON DEMO VIDEO - DEAD SIMPLE GUIDE

## ✅ NO DEPLOYMENT NEEDED - Mac Studio is perfect!

---

## EASIEST METHOD: QuickTime Screen Recording (5 minutes)

### Step 1: Open Terminal on Mac Studio
```bash
cd ~/gemma4-ewaste
```

### Step 2: Start QuickTime Player
- Open QuickTime Player (built-in on Mac)
- File → New Screen Recording
- Click the dropdown arrow next to record button
- Select "Built-in Microphone" (so you can talk)
- Click the red record button
- Select your terminal window to record

### Step 3: Record Your Demo
Talk while running the script:
```bash
./demo_script.sh
```

**What to say:**
```
"Hi, I'm Ayan. This is SafeScrap - an e-waste hazard detector powered by Gemma 4 E2B.

It helps recycling workers identify dangerous electronic components in real-time.

Let me show you how it works..."

[Wait for script to run - it shows 3 demos automatically]

"As you can see, SafeScrap correctly identified the hazards with 99.6% accuracy.

This runs completely offline using Gemma 4 E2B on Mac Studio.

The code is open source on GitHub. Thanks for watching!"
```

### Step 4: Stop Recording
- Press Stop button in menu bar
- File → Save
- Save as: `safescrap_demo.mov`

### Step 5: Upload to YouTube
- Go to: https://studio.youtube.com/
- Click "CREATE" → Upload videos
- Upload `safescrap_demo.mov`
- Title: "SafeScrap - E-Waste Hazard Detector (Gemma 4 Hackathon)"
- Description: Link to GitHub repo
- Visibility: "Unlisted" (for submission only)
- Copy the video URL

---

## OPTION 2: asciinema (Terminal Recording Only - No Voice)

If you don't want to talk:
```bash
cd ~/gemma4-ewaste
/opt/homebrew/bin/asciinema rec safescrap_demo.cast
./demo_script.sh
# Press Ctrl-D when done

# Upload to asciinema.org
/opt/homebrew/bin/asciinema upload safescrap_demo.cast
# Copy the URL
```

---

## OPTION 3: Use iPhone to Record Mac Studio Screen

- Open iPhone Camera
- Point at Mac Studio screen
- Start recording
- SSH into Mac Studio from another device
- Run: `cd ~/gemma4-ewaste && ./demo_script.sh`
- Narrate as it runs
- Stop recording, upload to YouTube

---

## SUBTITLES (Optional - 5 minutes)

If you want subtitles:

1. Upload video to YouTube
2. Go to: Video → Subtitles
3. Click "ADD" → Auto-sync
4. Paste this script:
```
SafeScrap - E-Waste Hazard Detector
Powered by Gemma 4 E2B
Identifying lithium-ion batteries
Classification: Critical hazard
Testing image recognition
Analyzing circuit boards
All tests passed - 99.6% accuracy
Running completely offline on Mac Studio
Open source on GitHub
```

---

## WHAT JUDGES WANT TO SEE:

✅ The code actually running
✅ Real-time hazard detection
✅ Accuracy results
✅ It runs on local hardware (Mac Studio)
✅ You explaining what it does

**Duration: 2-3 minutes MAX**

---

## DEMO SCRIPT BREAKDOWN:

The `demo_script.sh` automatically shows:
1. ✅ Lithium-ion battery classification (5 seconds)
2. ✅ Image recognition demo (5 seconds)
3. ✅ All 5 component types tested (10 seconds)

**Total runtime: ~20 seconds of actual demo**

You just need to add:
- 30 seconds intro (what is SafeScrap)
- 60 seconds explaining results
- 10 seconds outro (GitHub link)

= 2 minutes perfect video

---

## QUICK START (RIGHT NOW):

```bash
# On Mac Studio
cd ~/gemma4-ewaste

# Test the demo first
./demo_script.sh

# Looks good? Record it with QuickTime!
```

---

## YOU DON'T NEED:

- ❌ Deployment to Hetzner
- ❌ Fancy editing software
- ❌ Professional camera
- ❌ Perfect script
- ❌ Antigravity or other tools

Just QuickTime + Terminal + 5 minutes = DONE!

---

## After Recording:

1. Upload to YouTube (unlisted)
2. Get URL
3. Submit to Kaggle:
   - GitHub: https://github.com/ayanuali/gemma4-hackathon
   - Video: [your YouTube URL]
   - Write-up: PROJECT_STATUS.md

**DEADLINE: May 18, 2026**

**GO RECORD IT NOW!** 🚀
