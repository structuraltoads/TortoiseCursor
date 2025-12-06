
import struct

def create_blank_cursor():
    """Creates a 1x1 transparent cursor file."""
    with open("blank.cur", "wb") as f:
        # ICONDIR structure
        f.write(struct.pack("<HHH", 0, 2, 1))
        # ICONDIRENTRY structure
        f.write(struct.pack("<BBBBHHII", 1, 1, 0, 0, 0, 0, 40 + 8, 22))
        # BITMAPINFOHEADER
        f.write(struct.pack("<IiiHHIIiiII", 40, 1, 2, 1, 32, 0, 8, 0, 0, 0, 0))
        # XOR mask (1x1 transparent pixel)
        f.write(struct.pack("<I", 0))
        # AND mask (1x1 transparent pixel)
        f.write(struct.pack("<B", 255))

if __name__ == "__main__":
    create_blank_cursor()
    print("Created blank.cur")
