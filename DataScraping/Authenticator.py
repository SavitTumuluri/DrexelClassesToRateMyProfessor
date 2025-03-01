import cv2
from pyzbar.pyzbar import decode
import pyotp

# Load the QR code image (screenshot it and save it first)
image = cv2.imread("image.png")

# Decode QR code
decoded_objects = decode(image)
for obj in decoded_objects:
    print("Decoded Data:", obj.data.decode("utf-8"))

secret = "7mrx5y2nvvvbrrgk"  # Use your extracted secret key
totp = pyotp.TOTP(secret)
mfa_code = totp.now()

print(f"Generated MFA Code: {mfa_code}")
