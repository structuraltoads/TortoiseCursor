
from PIL import Image, ImageDraw
import math

def create_tortoise_frames():
    for i in range(16):
        im = Image.new("RGBA", (60, 60), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)

        # Shell
        draw.ellipse((10, 15, 50, 45), fill="#654321", outline="#432100", width=2)
        # Shell pattern
        draw.line((30, 15, 30, 45), fill="#432100", width=1)
        draw.line((20, 17, 40, 17), fill="#432100", width=1)
        draw.line((15, 25, 45, 25), fill="#432100", width=1)
        draw.line((15, 35, 45, 35), fill="#432100", width=1)


        # Head bobbing
        head_y = 28 + math.sin(i / 16 * 2 * math.pi) * 2
        draw.ellipse((45, head_y - 5, 60, head_y + 5), fill="#6B8E23", outline="#556B2F", width=2)

        # Leg animation
        # 0-3: right legs forward
        # 4-7: all legs centered
        # 8-11: left legs forward
        # 12-15: all legs centered
        
        # Right front leg
        if 0 <= i < 4:
            draw.rectangle((35, 10, 40, 20), fill="#6B8E23", outline="#556B2F", width=1)
        elif 8 <= i < 12:
            draw.rectangle((30, 15, 35, 25), fill="#6B8E23", outline="#556B2F", width=1)
        else:
            draw.rectangle((32, 12, 37, 22), fill="#6B8E23", outline="#556B2F", width=1)
            
        # Left front leg
        if 8 <= i < 12:
            draw.rectangle((35, 40, 40, 50), fill="#6B8E23", outline="#556B2F", width=1)
        elif 0 <= i < 4:
            draw.rectangle((30, 35, 35, 45), fill="#6B8E23", outline="#556B2F", width=1)
        else:
            draw.rectangle((32, 38, 37, 48), fill="#6B8E23", outline="#556B2F", width=1)

        # Right back leg
        if 0 <= i < 4:
            draw.rectangle((15, 10, 20, 20), fill="#6B8E23", outline="#556B2F", width=1)
        elif 8 <= i < 12:
            draw.rectangle((10, 15, 15, 25), fill="#6B8E23", outline="#556B2F", width=1)
        else:
            draw.rectangle((12, 12, 17, 22), fill="#6B8E23", outline="#556B2F", width=1)

        # Left back leg
        if 8 <= i < 12:
            draw.rectangle((15, 40, 20, 50), fill="#6B8E23", outline="#556B2F", width=1)
        elif 0 <= i < 4:
            draw.rectangle((10, 35, 15, 45), fill="#6B8E23", outline="#556B2F", width=1)
        else:
            draw.rectangle((12, 38, 17, 48), fill="#6B8E23", outline="#556B2F", width=1)


        im.save(f"tortoise_frame_{i}.png")

if __name__ == "__main__":
    create_tortoise_frames()
    print("Generated 16 new tortoise frames.")
