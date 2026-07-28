import os

def create_favicon():
    target_dir = "frontend/public"
    os.makedirs(target_dir, exist_ok=True)
    
    # Valid structural ICO binary header map (16x16 palette matrix)
    ico_bytes = (
        b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00\x68\x04'
        b'\x00\x00\x16\x00\x00\x00\x28\x00\x00\x00\x10\x00\x00\x00\x20\x00'
        b'\x00\x00\x01\x00\x20\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + 
        (b'\x7c\x3a\xed\xff' * 256) + (b'\x00' * 64)
    )
    
    with open(os.path.join(target_dir, "favicon.ico"), "wb") as f:
        f.write(ico_bytes)
    print("[SUCCESS]: Real favicon.ico generated and saved inside frontend/public/")

if __name__ == "__main__":
    create_favicon()
