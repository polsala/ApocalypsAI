import sys
import base64
import io

import qrcode

def generate_qr_base64(data: str) -> str:
    img = qrcode.make(data)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def main():
    if len(sys.argv) > 1:
        data = sys.argv[1]
    else:
        data = sys.stdin.read().strip()
    b64 = generate_qr_base64(data)
    print(b64)

if __name__ == "__main__":
    main()
