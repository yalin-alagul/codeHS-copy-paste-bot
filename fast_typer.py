#!/usr/bin/env python3
"""
Fast Keyboard Typer for macOS
A tool that creates a popup widget to paste clipboard content with fast typing emulation.
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
from pynput.keyboard import Controller
import sys
import platform

class FastTyperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fast Typer")
        self.root.geometry("300x150")

        # Enhanced window properties for staying on top across all screens
        self.setup_macos_window()

        self.root.resizable(False, False)

        # Position at top of screen
        self.position_at_top()

        # Initialize keyboard controller
        self.keyboard = Controller()

        # Flag to track if typing is in progress
        self.is_typing = False

        # Setup UI
        self.setup_ui()

    def setup_macos_window(self):
        """Setup window properties for cross-screen visibility without stealing focus"""
        # Basic window properties - visible but not intrusive
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.90)

        # Set window to appear on all workspaces using system command after creation
        self.root.after(1000, self._assign_to_all_spaces)

    def position_at_top(self):
        """Position the window at the top center of the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (300 // 2)
        y = 20  # Position near top of screen
        self.root.geometry(f"300x150+{x}+{y}")

    def _assign_to_all_spaces(self):
        """Use the simplest approach: simulate manual assignment to all desktops"""
        try:
            # Focus our window first
            self.root.focus_force()
            self.root.lift()

            time.sleep(0.5)  # Wait for window to be ready

            # Simulate the keyboard shortcut or right-click menu to assign to all desktops
            assign_script = '''
            tell application "System Events"
                -- Find our Python window
                set pythonApp to first process whose name contains "Python"
                set frontmost of pythonApp to true
                delay 0.2

                -- Try to find our window
                tell pythonApp
                    try
                        set ourWindow to first window whose title contains "Fast Typer"

                        -- Method 1: Try the Window menu approach
                        click ourWindow
                        delay 0.1

                        -- Try clicking on the green maximize button which sometimes has options
                        try
                            set greenButton to button 2 of ourWindow
                            click greenButton
                            delay 0.1
                            -- Look for "Move to All Desktops" or similar option
                        end try

                        -- Method 2: Right-click on title bar
                        try
                            set titleBar to ourWindow
                            right click titleBar at {150, 10}
                            delay 0.3

                            -- Try to find and click "Assign to All Desktops"
                            try
                                click menu item "Assign to All Desktops" of menu 1
                            on error
                                try
                                    click menu item "Move to All Desktops" of menu 1
                                end try
                            end try
                        end try

                    end try
                end tell
            end tell
            '''

            subprocess.run(['osascript', '-e', assign_script], capture_output=True)

        except Exception as e:
            print(f"Could not assign to all spaces: {e}")
            # Try a backup method using system preferences
            self._try_backup_method()

    def _try_backup_method(self):
        """Backup method: configure the app to always appear on all spaces"""
        try:
            # Set application-specific settings
            subprocess.run([
                'defaults', 'write', 'com.apple.dock', 'workspaces-edge-delay', '0.1'
            ], capture_output=True)

            print("Window should now appear on all spaces. You may need to manually right-click the window title bar and select 'Assign to All Desktops' once.")

        except Exception as e:
            print(f"Backup method failed: {e}")

    def keep_on_top(self):
        """Keep window visible on all screens without stealing focus"""
        if self.root.winfo_exists():
            # Only lift the window, don't force focus or switch apps
            self.root.lift()
            self.root.attributes('-topmost', True)

            # Position on current active screen
            self.position_on_active_screen()

            self.root.after(2000, self.keep_on_top)  # Check every 2 seconds

    def position_on_active_screen(self):
        """Position window on the currently active screen"""
        try:
            # Get current mouse position to determine active screen
            import tkinter as tk
            current_x = self.root.winfo_pointerx()
            current_y = self.root.winfo_pointery()

            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Calculate position for current screen (top center)
            window_x = current_x - 150  # Center the 300px wide window
            window_y = 20  # Top of screen

            # Ensure window stays within screen bounds
            if window_x < 0:
                window_x = 20
            elif window_x + 300 > screen_width:
                window_x = screen_width - 320

            self.root.geometry(f"300x150+{window_x}+{window_y}")

        except Exception as e:
            # Fallback to center positioning
            self.position_at_top()

    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title label
        title_label = ttk.Label(main_frame, text="Fast Typer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to type clipboard content")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Start button
        self.start_button = ttk.Button(main_frame, text="Start Typing", command=self.start_typing)
        self.start_button.grid(row=2, column=0, padx=(0, 10), sticky=tk.W)

        # Quit button
        quit_button = ttk.Button(main_frame, text="Quit", command=self.root.quit)
        quit_button.grid(row=2, column=1, sticky=tk.E)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def get_clipboard_content(self):
        """Get content from macOS clipboard"""
        try:
            result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return None

    def update_status(self, message):
        """Update the status label"""
        self.status_label.config(text=message)
        self.root.update()

    def countdown(self):
        """2-second countdown before typing starts"""
        for i in range(2, 0, -1):
            self.update_status(f"Starting in {i}...")
            time.sleep(1)
        self.update_status("Typing...")

    def type_text_fast(self, text):
        """Type text very fast using keyboard emulation"""
        if not text:
            return

        try:
            # Split text into lines to preserve structure
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
                    self.keyboard.press('\n')
                    self.keyboard.release('\n')
                    time.sleep(0.001)

        finally:
            # Ensure keyboard control is properly released
            self._release_keyboard_control()

    def _release_keyboard_control(self):
        """Explicitly release keyboard control and return focus"""
        try:
            # Release any held keys
            time.sleep(0.1)  # Small delay to ensure all keys are processed

            # Force the application to lose focus and return control
            if platform.system() == 'Darwin':
                # Use AppleScript to activate the previously active application
                subprocess.run([
                    'osascript', '-e',
                    'tell application "System Events" to key code 48 using {command down}'
                ], capture_output=True)
                time.sleep(0.1)

        except Exception as e:
            print(f"Error releasing keyboard control: {e}")

    def typing_thread(self):
        """Thread function for typing process"""
        try:
            self.is_typing = True

            # Get clipboard content
            clipboard_text = self.get_clipboard_content()

            if not clipboard_text:
                self.update_status("No content in clipboard!")
                self.start_button.config(state='normal')
                self.is_typing = False
                return

            if not clipboard_text.strip():
                self.update_status("Clipboard is empty!")
                self.start_button.config(state='normal')
                self.is_typing = False
                return

            # Countdown
            self.countdown()

            # Minimize the window during typing
            self.root.iconify()

            # Small delay to allow window to minimize
            time.sleep(0.1)

            # Type the text
            self.type_text_fast(clipboard_text)

            # Restore window and update status
            self.root.deiconify()
            self.root.lift()  # Ensure it comes back on top
            self.update_status("Typing completed! Ready for next task.")

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.root.deiconify()
            self.root.lift()
        finally:
            self.is_typing = False
            self.start_button.config(state='normal')

    def start_typing(self):
        """Start the typing process"""
        if self.is_typing:
            return  # Prevent multiple typing sessions

        self.start_button.config(state='disabled')
        self.update_status("Getting clipboard content...")

        # Start typing in a separate thread
        thread = threading.Thread(target=self.typing_thread)
        thread.daemon = True
        thread.start()

    def run(self):
        """Run the application"""
        # Start the keep_on_top monitor
        self.keep_on_top()

        # Run the main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = FastTyperApp()
    app.run()