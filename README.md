# 🎙️ Demain N'Attend Pas - Multi-Agent Podcast Assistant

A powerful multi-agent system designed to help grow the audience of the French podcast "Demain N'Attend Pas" through intelligent content analysis, optimization, and creation.

## 🌟 Features

This system includes **four specialized AI agents**:

### 1. 🎬 Short Video Agent
Creates viral short-form content from full episodes
- Automatically identifies the most engaging 10-15 second clips
- Generates 4-8 ready-to-post video clips optimized for YouTube Shorts and Instagram Reels
- Adds captions and suggests titles and hashtags
- Balances provocative, insightful, and emotionally resonant moments

### 2. 🔍 SEO Agent
Maximizes episode discoverability across all platforms
- Generates optimized titles (2-3 options)
- Creates platform-specific descriptions (Spotify, Apple Podcasts, YouTube, Instagram)
- Identifies relevant keywords and hashtags in French and English
- Provides comprehensive SEO recommendations

### 3. 📚 Prep Agent
Helps prepare for upcoming guest interviews
- Identifies essential reading materials, essays, and articles
- Finds most valuable interviews, talks, and videos
- Prioritizes resources by importance (ESSENTIAL, HIGH, MEDIUM)
- Suggests interview angles and questions

### 4. 📊 Analytics Agent
Analyzes episode performance and identifies patterns
- Analyzes engagement metrics across episodes
- Identifies what works and what doesn't
- Provides actionable recommendations
- Learns from data to optimize future content

## 🚀 Quick Start Guide (For Non-Technical Users)

### Step 1: Download the Project

1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer

### Step 2: Install Python (if not already installed)

1. Visit https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. During installation, **IMPORTANT**: Check the box "Add Python to PATH"

### Step 3: Run the Setup

**On Windows:**
1. Double-click `setup.bat`
2. Wait for installation to complete

**On Mac/Linux:**
1. Open Terminal
2. Navigate to the project folder: `cd path/to/demainn-attendpas`
3. Run: `./setup.sh`

### Step 4: Get Your API Keys

You need two API keys to use this system:

#### Claude API Key (Anthropic)
1. Go to https://console.anthropic.com/settings/keys
2. Sign in or create an account
3. Click "Create Key"
4. Copy the key

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key

**Cost Note:** Both APIs charge per use. Typical costs:
- Short Video Agent: ~$0.50-2.00 per episode
- SEO Agent: ~$0.30-1.00 per episode
- Prep Agent: ~$0.20-0.50 per guest
- Analytics Agent: ~$0.10-0.30 per analysis

### Step 5: Add Your API Keys

1. Open the `.env` file in a text editor (Notepad, TextEdit, etc.)
2. Replace `your_claude_api_key_here` with your actual Claude API key
3. Replace `your_openai_api_key_here` with your actual OpenAI API key
4. Save the file

Example:
```
ANTHROPIC_API_KEY=sk-ant-abc123...
OPENAI_API_KEY=sk-xyz789...
```

### Step 6: Run the Application

**On Windows:**
- Double-click `run.bat`

**On Mac/Linux:**
- Open Terminal
- Navigate to the project folder
- Run: `./run.sh`

The application will open in your web browser at `http://localhost:8501`

## 📖 How to Use Each Agent

### 🎬 Short Video Agent

1. Navigate to the "Short Video" tab
2. Upload your full episode video file (MP4, MP3, or MOV)
3. Select how many clips you want (4-10)
4. Click "Générer les clips"
5. Wait 5-15 minutes (depending on video length)
6. Review and download your clips
7. Use the provided instructions to post on social media

**Tips:**
- Works best with videos where there's clear speaking/conversation
- The longer the video, the longer the processing time
- Clips are automatically formatted for vertical video (9:16 aspect ratio)

### 🔍 SEO Agent

1. Navigate to the "SEO" tab
2. Upload your episode video/audio file
3. Optionally add guest name and episode topic
4. Click "Générer le package SEO"
5. Review the generated titles, keywords, and descriptions
6. Copy and paste into your podcast platforms

**Tips:**
- Provides content in both French and English
- Different descriptions optimized for each platform
- Use suggested hashtags for social media posts

### 📚 Prep Agent

1. Navigate to the "Prep" tab
2. Enter the name of your upcoming guest
3. Optionally add context (e.g., "focus on their latest book")
4. Click "Générer le guide de préparation"
5. Review the prioritized list of resources
6. Start with ESSENTIAL items, then HIGH priority

**Tips:**
- The agent searches in both French and English
- Resources are ordered by importance
- Time estimates help you plan your prep

### 📊 Analytics Agent

1. Navigate to the "Analytics" tab
2. Download your analytics data from Ausha or YouTube Analytics
3. Upload the CSV or JSON file
4. Select which episodes to analyze
5. Click "Analyser les performances"
6. Review insights and recommendations

**Tips:**
- The more episodes you analyze, the better the insights
- Look for patterns in top-performing content
- Use recommendations to guide future episodes

## 🛠️ Additional Setup (Optional)

### Installing ffmpeg (Required for Short Video Agent)

**On Mac (with Homebrew):**
```bash
brew install ffmpeg
```

**On Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add to PATH (search "Environment Variables" in Windows)

**On Ubuntu/Linux:**
```bash
sudo apt-get install ffmpeg
```

## ❓ Troubleshooting

### "API Keys not configured" error
- Make sure you've edited the `.env` file with your real API keys
- Restart the application after editing `.env`

### "Module not found" error
- Run the setup script again: `./setup.sh` or `setup.bat`
- Make sure you're running the app from the correct folder

### Video processing fails
- Check that ffmpeg is installed: `ffmpeg -version`
- Make sure your video file is not corrupted
- Try with a smaller video file first

### Slow performance
- Video transcription takes time (1-hour video = 5-10 min processing)
- SEO and Prep agents are faster (1-2 minutes)
- First run downloads models (slower), subsequent runs are faster

## 💰 Cost Management

To keep costs low:
1. Test with short videos first
2. Only generate clips when you're ready to post
3. Reuse SEO packages across similar episodes
4. Batch your analytics reviews

Estimated monthly costs (assuming 4 episodes/month):
- Short Video: ~$4-8
- SEO: ~$2-4
- Prep: ~$1-2
- Analytics: ~$1

Total: ~$8-15/month for full usage

## 🔒 Privacy & Data

- All processing happens via API calls to Anthropic and OpenAI
- No data is stored permanently on external servers
- Generated clips and files are saved locally on your computer
- Your API keys are stored locally in the `.env` file (never shared)

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the error message carefully
3. Make sure all prerequisites are installed
4. Check that API keys are valid and have credits

## 📋 System Requirements

- **Operating System:** Windows 10+, macOS 10.14+, or Linux
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 2GB for software + space for videos
- **Internet:** Required for API calls

## 🔄 Updating

To update the system:
1. Download the latest version from GitHub
2. Replace all files except `.env` (keep your API keys)
3. Run the setup script again

## 📝 License

This project is for personal use with the "Demain N'Attend Pas" podcast.

---

**Made with ❤️ for Demain N'Attend Pas**

🎙️ Bonne chance avec votre podcast!
