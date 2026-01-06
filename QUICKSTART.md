# 🚀 Quick Start - Demain N'Attend Pas

**For users with zero technical knowledge - follow these 6 simple steps:**

## ✅ Step 1: Download This Project

1. Click the green "Code" button at the top right
2. Click "Download ZIP"
3. Extract the ZIP to your Desktop or Documents folder

## ✅ Step 2: Install Python

1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT:** Check the box that says "Add Python to PATH"
5. Click "Install Now"

## ✅ Step 3: Run Setup

### On Windows:
- Double-click the file called `setup.bat`
- Wait for it to finish (2-5 minutes)

### On Mac:
1. Open "Terminal" (search for it in Spotlight)
2. Type: `cd ` (with a space after cd)
3. Drag the project folder into the Terminal window
4. Press Enter
5. Type: `./setup.sh` and press Enter

## ✅ Step 4: Get API Keys

### Claude API Key:
1. Go to: **https://console.anthropic.com/settings/keys**
2. Create account or sign in
3. Click "Create Key"
4. Copy the key (starts with `sk-ant-`)

### OpenAI API Key:
1. Go to: **https://platform.openai.com/api-keys**
2. Create account or sign in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

💰 **Cost:** About $10-15/month for regular usage (4 episodes)

## ✅ Step 5: Add Your Keys

1. In the project folder, find the file called `.env`
2. Right-click it and open with Notepad (Windows) or TextEdit (Mac)
3. Replace these lines:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   With your actual keys:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
4. Save the file

## ✅ Step 6: Launch the App

### On Windows:
- Double-click `run.bat`

### On Mac:
1. Open Terminal
2. Type: `cd ` (with space)
3. Drag the project folder into Terminal
4. Press Enter
5. Type: `./run.sh` and press Enter

**The app will open in your web browser!** 🎉

---

## 🎬 Using the Short Video Agent

1. Click the "Short Video" tab
2. Click "Browse files" and select your episode video
3. Choose how many clips (4-10)
4. Click "Générer les clips"
5. ☕ Take a coffee break (5-15 minutes)
6. Download your clips and post them!

---

## 🔍 Using the SEO Agent

1. Click the "SEO" tab
2. Upload your episode video/audio
3. Add guest name (optional)
4. Click "Générer le package SEO"
5. Copy the descriptions for each platform

---

## 📚 Using the Prep Agent

1. Click the "Prep" tab
2. Type the guest's name
3. Click "Générer le guide de préparation"
4. Start reading the ESSENTIAL resources first!

---

## 📊 Using the Analytics Agent

1. Download your podcast analytics from Ausha
2. Click the "Analytics" tab
3. Upload your CSV or JSON file
4. Click "Analyser les performances"
5. Review what's working and what's not

---

## ❓ Having Problems?

### "API Keys not configured"
→ Make sure you saved the `.env` file after adding your keys
→ Restart the application

### "Python not found"
→ Reinstall Python and CHECK the "Add to PATH" box

### "ffmpeg not found"
→ For now, skip the Short Video Agent
→ SEO, Prep, and Analytics agents will still work

### Need more help?
→ Check the full README.md file
→ All error messages are in English - copy them to search online

---

**C'est tout!** You're ready to grow your podcast audience! 🎙️

