import os
import subprocess

file = subprocess.check_output(["find", ".", "-type", "f", "-name", "cover.*"]).decode().strip()

if not file:
    print("Error: File 'cover' not found.")
    exit(1)

extension = file.split(".")[-1]

# WebP route
if extension=="webp":
    print("Detected WebP format which cannot be converted due to libjxl's refusal to support it. Opting for other formats will result in larger file sizes. Proceeding without JpegXl.")
    os.system(f"magick convert cover.webp -resize 1080x1080 cover-1080p.jpeg")

    originalFile = os.stat("cover.webp").st_size / 1024 /1024
    jpegFile = os.stat("cover-1080p.jpeg").st_size / 1024 /1024
    print(f"Done:\nOriginal file:\t{originalFile:.2f} MB\n1080p file:\t{jpegFile:.2f} MB")
    exit(0)
# AVIF route
elif extension=="avif":
    print("Detected AVIF format which cannot be converted due to libjxl's refusal to support it. Opting for other formats will result in larger file sizes. Proceeding without JpegXl.")
    os.system(f"magick convert cover.avif -resize 1080x1080 cover-1080p.jpeg")

    originalFile = os.stat("cover.avif").st_size / 1024 /1024
    jpegFile = os.stat("cover-1080p.jpeg").st_size / 1024 /1024
    print(f"Done:\nOriginal file:\t{originalFile:.2f} MB\n1080p file:\t{jpegFile:.2f} MB")
    exit(0)
# JXL route
elif extension=="jxl":
    print("Detected JpegXL format. Proceeding without conversion.")
    os.system(f"magick convert cover.jxl -resize 1080x1080 cover-1080p.jpeg")

    originalFile = os.stat("cover.jxl").st_size / 1024 /1024
    jpegFile = os.stat("cover-1080p.jpeg").st_size / 1024 /1024
    print(f"Done:\nOriginal file:\t{originalFile:.2f} MB\n1080p file:\t{jpegFile:.2f} MB")
    exit(0)

os.system(f"cp cover.{extension} coverBKP.{extension}")

os.system(f"magick mogrify -strip cover.{extension}")   #metadata strip, actually seen some quality downgrade in select cases, but needs more testing

os.system(f"cjxl cover.{extension} -q 100 -e 9 cover.jxl")

os.system(f"magick convert cover.{extension} -resize 1080x1080 cover-1080p.jpeg")

os.remove(f"cover.{extension}")

originalFile = os.stat("coverBKP." + extension).st_size / 1024 /1024
jxlFile = os.stat("cover.jxl").st_size / 1024 /1024
jpegFile = os.stat("cover-1080p.jpeg").st_size / 1024 /1024

print(f"Done:\nOriginal file:\t{originalFile:.2f} MB\nJpegXl file:\t{jxlFile:.2f} MB\n1080p file:\t{jpegFile:.2f} MB")
