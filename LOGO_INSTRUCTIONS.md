# Adding Your Logo

To add your podcast logo to the app:

## Local Setup (Your Computer):

1. Save your logo image as `logo.png`
2. Place it in the `assets/` folder in your project directory
   - Full path should be: `demainn-attendpas/assets/logo.png`
3. Restart the app (close Command Prompt and run `run.bat` again)

## Streamlit Cloud Setup:

1. Save your logo as `logo.png`
2. Add it to the `assets/` folder in your project
3. Commit and push to GitHub:
   ```bash
   git add assets/logo.png
   git commit -m "Add podcast logo"
   git push
   ```
4. Streamlit Cloud will automatically reload with your logo!

**Note:** The logo image should be roughly 300x100 pixels for best fit, but it will automatically resize to fit the sidebar.
