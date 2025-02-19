import requests
from pynput import keyboard
from playsound import playsound

# Webhook URL (Flask server)
WEBHOOK_URL = "http://localhost:5050/scan"
SCANNER_USER = "Scanner A"  # Change if using multiple scanners
SOUND_FILE = "beep.wav"  # Path to sound file

barcode_data = ""

def send_webhook(barcode):
    """Send the scanned QR code to the server."""
    payload = {
        "scanned_code": barcode,
        "scanner_user": SCANNER_USER  # Send scanner identifier
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ Webhook sent: {barcode}")
            playsound(SOUND_FILE)  # Play sound after scan
        else:
            print(f"❌ Failed to send webhook. Response: {response.text}")
    except Exception as e:
        print(f"❌ Error sending webhook: {str(e)}")

def on_press(key):
    """Capture barcode scanner input using pynput."""
    global barcode_data

    try:
        if key == keyboard.Key.enter:
            print(f"Scanned: {barcode_data}")
            send_webhook(barcode_data)
            barcode_data = ""  # Reset for next scan
        elif hasattr(key, 'char') and key.char:
            barcode_data += key.char
    except Exception as e:
        print(f"Error in key event: {str(e)}")

# Start listening for keypress events
print("Listening for barcode scans...")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
