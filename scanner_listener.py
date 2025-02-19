from pynput import keyboard
import requests

# Webhook Configuration
WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/3227176/2wwctxj/"

# Store scanned barcode
barcode_data = ""

def send_webhook(barcode):
    """Send a webhook request with the scanned QR code details."""
    payload = {"scanned_code": barcode}

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ Webhook sent successfully for: {barcode}")
        else:
            print(f"❌ Failed to send webhook. Response: {response.text}")
    except Exception as e:
        print(f"❌ Error sending webhook: {str(e)}")

def on_press(key):
    """Capture barcode scanner input."""
    global barcode_data

    try:
        if key == keyboard.Key.enter:  # Scanner sends 'Enter' after scanning
            print(f"Scanned: {barcode_data}")
            send_webhook(barcode_data)
            barcode_data = ""  # Reset for next scan
        elif hasattr(key, 'char') and key.char is not None:
            barcode_data += key.char
    except Exception as e:
        print(f"Error in key event: {str(e)}")

# Start listening for barcode scans
print("Listening for barcode scans...")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
