#!/usr/bin/env python3
import os
import glob
import subprocess
import sys
from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def find_images(directory="~"):
    directory = os.path.expanduser(directory)
    patterns = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp', '*.bmp']
    images = []
    for pattern in patterns:
        images.extend(glob.glob(os.path.join(directory, pattern)))
    return sorted(images)

def clear():
    os.system('clear')

def show_selector(images, selected_idx):
    sys.stdout.write('\033[2J\033[H')  # Clear and reset
    sys.stdout.flush()
    
    print("\033[96m\033[1m")
    print("="*80)
    print("  👁️  MOONDREAM2 VISION AI (Sixel - Real Images)")
    print("="*80)
    print("\033[0m\n")
    
    print("\033[2mW/S: Navigate | A/D: Jump | ENTER: Analyze | Q: Quit\033[0m\n")
    
    print("\033[94m\033[1m📂 Images:\033[0m")
    print("\033[2m" + "─" * 70 + "\033[0m")
    
    visible_count = 7
    start = max(0, min(selected_idx - 3, len(images) - visible_count))
    end = min(len(images), start + visible_count)
    
    for i in range(start, end):
        fn = os.path.basename(images[i])[:60]
        sz = os.path.getsize(images[i]) / 1024
        
        if i == selected_idx:
            print(f"\033[93m  ▶ {i+1:3d}. {fn:<55} {sz:>6.1f}K\033[0m")
        else:
            print(f"\033[2m    {i+1:3d}. {fn:<55} {sz:>6.1f}K\033[0m")
    
    print("\033[2m" + "─" * 70 + "\033[0m")
    print(f"\033[96m[{selected_idx + 1}/{len(images)}]\033[0m\n")
    
    filename = os.path.basename(images[selected_idx])
    size = os.path.getsize(images[selected_idx]) / 1024
    img = Image.open(images[selected_idx])
    print(f"\033[92m▶\033[0m \033[1m{filename}\033[0m \033[2m({img.width}×{img.height}, {size:.1f}KB)\033[0m\n")
    
    subprocess.run(['convert', images[selected_idx], '-resize', '800x400', 'sixel:-'], 
                   stderr=subprocess.DEVNULL)
    
    print()
    sys.stdout.flush()

def get_key():
    """Get keypress - completely self-contained, no global terminal changes"""
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        
        if ch == '\x1b':
            # Consume the entire escape sequence
            next1 = sys.stdin.read(1)
            if next1 == '[':
                next2 = sys.stdin.read(1)
                if next2 == 'A': return 'up'
                elif next2 == 'B': return 'down'
                elif next2 == 'C': return 'right'
                elif next2 == 'D': return 'left'
        return ch
    finally:
        # Always restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def analyze_image(model, tokenizer, image_path):
    clear()
    
    print("\033[96m\033[1m")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              👁️  ANALYZING IMAGE                        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\033[0m\n")
    
    filename = os.path.basename(image_path)
    img = Image.open(image_path)
    print(f"\033[92m✓\033[0m \033[1m{filename}\033[0m \033[2m({img.width}×{img.height})\033[0m\n")
    
    subprocess.run(['convert', image_path, '-resize', '1000x600', 'sixel:-'])
    print()
    
    enc_image = model.encode_image(img)
    
    while True:
        question = input("\033[96m💬 Question (or 'back'):\033[0m ").strip()
        
        if question.lower() in ['back', 'b', 'exit', 'quit']:
            break
        
        if not question:
            question = "Describe this image in detail."
        
        print("\n\033[93m🤔 Analyzing...\033[0m\n")
        answer = model.answer_question(enc_image, question, tokenizer)
        
        print("\033[94m\033[1m👁️  Analysis:\033[0m")
        print("\033[2m" + "─" * 60 + "\033[0m")
        print(answer)
        print("\033[2m" + "─" * 60 + "\033[0m\n")

def main():
    clear()
    print("\033[96m🔄 Loading Moondream2...\033[0m\n")
    
    model_id = "vikhyatk/moondream2"
    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True, torch_dtype=torch.float16,
        low_cpu_mem_usage=True, device_map={"": "cuda"}
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    print("\033[92m✓ Model loaded!\033[0m\n")
    
    images = find_images("~")
    if not images:
        print("\033[91m✗ No images found!\033[0m\n")
        return
    
    selected_idx = 0
    
    while True:
        try:
            show_selector(images, selected_idx)
            key = get_key()
            
            if key in ['w', 'W', 'up']:
                selected_idx = max(0, selected_idx - 1)
            elif key in ['s', 'S', 'down']:
                selected_idx = min(len(images) - 1, selected_idx + 1)
            elif key in ['a', 'A']:
                selected_idx = max(0, selected_idx - 5)
            elif key in ['d', 'D']:
                selected_idx = min(len(images) - 1, selected_idx + 5)
            elif key in ['\r', '\n']:
                analyze_image(model, tokenizer, images[selected_idx])
            elif key in ['q', 'Q']:
                clear()
                print("\n\033[96m👋 Goodbye!\033[0m\n")
                break
                
        except KeyboardInterrupt:
            clear()
            print("\n\033[96m👋 Goodbye!\033[0m\n")
            break

if __name__ == "__main__":
    main()
