#!/usr/bin/env python3
"""
Fast Keyboard Typer with Global Hotkey for macOS
A tool that uses a global hotkey (Cmd+Shift+U) to trigger fast typing from any application.
"""

import subprocess
import threading
import time
from pynput.keyboard import Controller, Key, Listener
from pynput import keyboard
import sys
import platform

class FastTyperHotkey:
    def __init__(self):
        # Initialize keyboard controller
        self.keyboard = Controller()

        # Flag to track if typing is in progress
        self.is_typing = False

        # Global hotkey combination: Cmd+Shift+U
        self.hotkey_combination = {Key.cmd, Key.shift}
        self.hotkey_key = 'u'
        self.current_keys = set()

        # Check accessibility permissions
        self.check_accessibility_permissions()

        print("🚀 Fast Typer started!")
        print("📋 Copy text to clipboard, then press Cmd+Shift+U to start fast typing")
        print("⚡ Typing starts immediately after hotkey")
        print("❌ Press Ctrl+C to quit")

    def check_accessibility_permissions(self):
        """Check and guide user for accessibility permissions"""
        print("\n🔒 Checking accessibility permissions...")

        # Test if we can listen to global key events
        try:
            # Try to create a test listener
            test_script = '''
            tell application "System Events"
                set accessibilityEnabled to UI elements enabled
                return accessibilityEnabled
            end tell
            '''

            result = subprocess.run(['osascript', '-e', test_script],
                                  capture_output=True, text=True)

            if "true" not in result.stdout.lower():
                self.show_permission_instructions()
            else:
                print("✅ Accessibility permissions are enabled!")

        except Exception as e:
            print("⚠️  Could not verify accessibility permissions")
            self.show_permission_instructions()

    def show_permission_instructions(self):
        """Show instructions for enabling accessibility permissions"""
        print("\n" + "="*60)
        print("🚨 IMPORTANT: Accessibility Permissions Required")
        print("="*60)
        print("For global hotkeys to work across all applications, you need to:")
        print()
        print("1. Open System Preferences → Security & Privacy → Privacy")
        print("2. Click 'Accessibility' in the left sidebar")
        print("3. Click the lock icon and enter your password")
        print("4. Add Terminal (or your Python app) to the list")
        print("5. Make sure the checkbox next to it is checked")
        print()
        print("Alternative quick method:")
        print("• Press Cmd+Space, type 'accessibility', press Enter")
        print("• This opens the right settings page directly")
        print()
        print("After enabling permissions, restart this app!")
        print("="*60)

        # Also trigger the system permission request
        try:
            subprocess.run([
                'osascript', '-e',
                'tell application "System Preferences" to reveal anchor "Privacy_Accessibility" of pane id "com.apple.preference.security"'
            ], capture_output=True)
        except Exception:
            pass

    def get_clipboard_content(self):
        """Get content from macOS clipboard"""
        try:
            result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return None

    def countdown(self):
        """Start typing immediately"""
        # Show notification
        subprocess.run([
            'osascript', '-e',
            'display notification "Typing now!" with title "Fast Typer"'
        ], capture_output=True)

    def type_text_fast(self, text):
        """Type text very fast using keyboard emulation"""
        if not text:
            return

        try:
            # Normalize line breaks and split text into lines to preserve structure
            # Handle different line break types (Windows, Mac, Unix)
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            lines = text.split('\n')

            for i, line in enumerate(lines):
                # Check if we should stop typing
                if not self.is_typing:
                    break

                # Type each character very quickly
                for char in line:
                    if not self.is_typing:
                        break
                    self.keyboard.type(char)
                    # Very small delay for ultra-fast typing (0.001 seconds)
                    time.sleep(0.001)

                # Add newline if not the last line
                if i < len(lines) - 1:
                    if not self.is_typing:
                        break
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)
                    time.sleep(0.001)

        finally:
            # Ensure keyboard control is properly released
            self._release_keyboard_control()

    def _release_keyboard_control(self):
        """Explicitly release keyboard control and return focus"""
        try:
            # Release any held keys
            time.sleep(0.1)  # Small delay to ensure all keys are processed
            print("✅ Typing completed!")

        except Exception as e:
            print(f"Error releasing keyboard control: {e}")

    def typing_thread(self):
        """Thread function for typing process"""
        try:
            self.is_typing = True
            print("📋 Getting clipboard content...")

            # Get clipboard content
            clipboard_text = self.get_clipboard_content()

            if not clipboard_text:
                print("❌ No content in clipboard!")
                self.is_typing = False
                return

            if not clipboard_text.strip():
                print("❌ Clipboard is empty!")
                self.is_typing = False
                return

            print(f"📄 Found {len(clipboard_text)} characters to type")

            # Countdown
            self.countdown()

            # Type the text
            self.type_text_fast(clipboard_text)

        except Exception as e:
            print(f"❌ Error: {str(e)}")
        finally:
            self.is_typing = False

    def on_press(self, key):
        """Handle key press events"""
        try:
            # Add key to current pressed keys
            self.current_keys.add(key)

            # Check if hotkey combination is pressed
            if (self.hotkey_combination.issubset(self.current_keys) and
                hasattr(key, 'char') and key.char == self.hotkey_key):

                if not self.is_typing:
                    print("🔥 Hotkey triggered! Starting fast typing...")
                    # Start typing in a separate thread
                    thread = threading.Thread(target=self.typing_thread)
                    thread.daemon = True
                    thread.start()
                else:
                    print("⚠️  Already typing! Please wait...")

        except AttributeError:
            # Special keys (like ctrl, alt, etc.) don't have char attribute
            pass

    def on_release(self, key):
        """Handle key release events"""
        try:
            # Remove key from current pressed keys
            self.current_keys.discard(key)

            # Check for quit
            if key == Key.ctrl_l or key == Key.ctrl_r:
                # Handle Ctrl+C to quit
                pass

        except AttributeError:
            pass

    def run(self):
        """Run the hotkey listener"""
        print("🎯 Listening for global hotkey: Cmd+Shift+U")

        try:
            # Start the global key listener
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("\n👋 Fast Typer stopped!")
            sys.exit(0)

if __name__ == "__main__":
    try:
        app = FastTyperHotkey()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Fast Typer stopped!")
        sys.exit(0)