# Automatic Login Setup (Windows via netplwiz)

1.  **Configure Windows Hello Sign-in Options:**
    *   Navigate to: `Settings` > `Accounts` > `Sign-in options`.
    *   Scroll down to **'Additional Settings'**.
    *   Ensure the switch for **'For improved security, only allow Windows Hello Sign-in for Microsoft accounts on this device'** is toggled **OFF**.
2.  **Set Up Automatic Login (via `netplwiz`):**
    *   Press `Win + R`, type `netplwiz`, and press `Enter`.
    *   Select your user account in the list.
    *   Toggle **'Users must enter a user name and password to use this computer'** on and off to trigger the popup.
    *   **Enter Credentials:** Use your FULL Microsoft email and password.
3.  **Restart** the computer.
