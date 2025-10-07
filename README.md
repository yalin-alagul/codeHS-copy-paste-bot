Download the repo to your computer.
Unzip the archive
You have 2 options to run
  Terminal:
      Use claude if you don't know how to do something.
      Download python if you don't have it.
        I preffer homebrew to download it
      Add python to device paths if not added.
      Add pip to device paths if not added.
      Use this command: pip install pynput
      Write: python3 
      Then drag and drop the file to terminal.
      it should look something like this: python3 /Users/username/desktop/fast_typer_hotkey.py

  IDE:
    Use claude if you don't know how to do something.
    Download python if you don't have it.
      In IDE's you can use extensions to set up python.
    Open the folder: codeHS-copy-paste-bot-main in the IDE and run it

Important Warnings

Running this code requires access to certain settings

Method 1: Through System Preferences (Detailed Steps)

  1. Open System Preferences
    - Click the Apple menu → System Preferences
    - Or press Cmd + Space, type "System Preferences", press Enter
  2. Navigate to Privacy Settings
    - Click "Security & Privacy"
    - Click the "Privacy" tab at the top
  3. Enable Accessibility Permissions
    - In the left sidebar, scroll down and click "Accessibility"
    - Click the lock icon (🔒) in the bottom-left corner
    - Enter your Mac password when prompted
  4. Add Your Application
    - Click the "+" button below the app list
    - Navigate to and select one of these:
        - Terminal (if running the script from Terminal)
      - Python (if running directly with Python)
      - Your IDE (VS Code, PyCharm, etc. if running from there)
  5. Enable the Permission
    - Make sure the checkbox next to your app is ✅ checked
    - Click the lock icon again to save changes

  Method 2: When First Running the Script

  1. Run the Python script: python3 fast_typer_hotkey.py
  2. macOS may show a permission dialog automatically
  3. Click "Open System Preferences" if prompted
  4. Follow the steps above to grant permission
  5. Restart the script after granting permission

  Troubleshooting

  If the hotkey doesn't work:
  - Restart the Python script after granting permissions
  - Make sure the correct application (Terminal/Python/IDE) is added
  to Accessibility
  - Check that the checkbox is enabled

  Multiple Python installations:
  - If using Homebrew Python: Look for /usr/local/bin/python3 or
  /opt/homebrew/bin/python3
  - If using system Python: Look for /usr/bin/python3
  - Add the specific Python executable you're using

  Still not working:
  - Restart your Mac after granting permissions
  - Remove and re-add the application in Accessibility settings

  The script will automatically check permissions and guide you
  through this process when you run it.
