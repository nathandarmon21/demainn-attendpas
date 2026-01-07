# 🚀 Deploying to Streamlit Cloud

This guide will help you deploy the multi-agent system to Streamlit Cloud so you can share it with others via a simple link.

## ✨ What is Streamlit Cloud?

Streamlit Cloud is a **free hosting service** that allows you to deploy Streamlit apps and share them with anyone via a URL. No one needs to install anything - they just click a link!

## 📋 Prerequisites

1. A GitHub account (create one at github.com if you don't have one)
2. This repository on GitHub
3. Your API keys (Anthropic and OpenAI)

## 🔧 Step-by-Step Deployment

### Step 1: Push Your Code to GitHub

If you haven't already, make sure your code is on GitHub:

1. Go to github.com
2. Create a new repository called "demainn-attendpas"
3. Follow the instructions to push your local code

### Step 2: Sign Up for Streamlit Cloud

1. Go to **https://share.streamlit.io/**
2. Click **"Sign up"**
3. Sign up using your **GitHub account**
4. Authorize Streamlit to access your GitHub repositories

### Step 3: Deploy Your App

1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: Select `your-username/demainn-attendpas`
   - **Branch**: Select `main` or `claude/podcast-multi-agent-system-puXsD`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (e.g., `demain-nattend-pas-assistant`)

3. Click **"Advanced settings"** (before deploying)
4. Set **Python version**: `3.10` or higher

5. Click **"Deploy!"**

### Step 4: Add Your API Keys (Secrets)

This is the most important step!

1. Once the app is deploying, click the **"⋮"** menu (three dots) in the top right
2. Select **"Settings"**
3. Go to the **"Secrets"** section
4. Copy and paste this, **replacing with your actual API keys**:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-anthropic-key-here"
OPENAI_API_KEY = "sk-your-actual-openai-key-here"
```

5. Click **"Save"**
6. The app will automatically restart with your secrets

### Step 5: Share Your App!

Once deployed (takes 2-5 minutes), you'll get a URL like:

```
https://demain-nattend-pas-assistant.streamlit.app
```

You can share this URL with anyone! They can:
- Use all the agents
- Upload videos
- Generate content
- Everything works just like your local version

## 🔒 Security Notes

### API Key Security

- ✅ Your API keys are stored securely in Streamlit Cloud's encrypted secrets
- ✅ They are never visible in your code or to app users
- ✅ Only you (the app owner) can see/edit them

### Cost Management

⚠️ **IMPORTANT**: When you deploy publicly, anyone with the link can use your API keys!

**To control costs:**

1. **Add password protection** (recommended for public deployment)
2. **Set API usage limits** in your Anthropic/OpenAI dashboards
3. **Monitor usage** regularly
4. **Share the link only with trusted people**

### Adding Password Protection

If you want to restrict access, add this to your `app.py` (at the top of the `main()` function):

```python
def check_password():
    """Simple password protection"""
    def password_entered():
        if st.session_state["password"] == "your_chosen_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Mot de passe", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Mot de passe", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Mot de passe incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()
```

## 🎯 Sharing with Another Person

To give someone full access without them downloading anything:

1. **Deploy to Streamlit Cloud** (steps above)
2. **Share the URL** with them
3. **That's it!** They can:
   - Open the URL in their browser
   - Use all agents immediately
   - No installation required
   - Works on any device (computer, tablet, phone)

## 📊 Managing Your Deployed App

### Update Your App

When you push new code to GitHub, Streamlit Cloud will automatically redeploy!

Or manually:
1. Go to your app dashboard
2. Click "Reboot app" to restart
3. Click "Clear cache" if you've updated dependencies

### View Logs

To see what's happening:
1. Click "Manage app"
2. View logs in real-time
3. Check for errors

### Stop/Delete Your App

1. Go to your app dashboard
2. Click "⋮" menu
3. Select "Delete app"

## 🆓 Free Tier Limits

Streamlit Cloud's free tier includes:
- ✅ Unlimited public apps
- ✅ 1 GB of resources per app
- ✅ Community support
- ⚠️ Apps may sleep after inactivity (wake up when visited)
- ⚠️ Limited to 3 private apps

Perfect for this use case!

## 🐛 Troubleshooting

### "App is in an unhealthy state"
- Check that your `requirements.txt` is correct
- Verify Python version is 3.10+
- Check logs for errors

### "ModuleNotFoundError"
- Make sure all dependencies are in `requirements.txt`
- Check that package names are correct

### "API Keys not configured"
- Double-check secrets are set correctly
- Secrets must be EXACTLY as shown (no extra spaces)
- Restart the app after adding secrets

### App is very slow
- First load is always slower (building environment)
- Subsequent loads are faster
- Video processing will always take time (that's normal)

## 💡 Pro Tips

1. **Test locally first**: Make sure everything works on your computer before deploying
2. **Use environment variables**: Never hardcode API keys in your code
3. **Monitor costs**: Check your Anthropic/OpenAI usage regularly
4. **Share selectively**: Only share the URL with people who need it
5. **Update regularly**: Push improvements to GitHub and they'll auto-deploy

---

**You're all set!** Anyone with your link can now use the podcast assistant system! 🎉
