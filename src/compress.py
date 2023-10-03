import logging
import os
import argparse
import subprocess  # to call ffmpeg and install pillow if needed

try:
    from PIL import Image
except ImportError:
    print("oh no! Pillow (a python image library) not found, installing... (this may take a moment!)")
    try:
        subprocess.run(['pip', 'install', 'Pillow'], check=True)
        from PIL import Image
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install Pillow: {e}")
        exit(1)  # Exit the script if Pillow installation fails


def compress_file(file_path):
    file_ext = file_path.split('.')[-1].lower()
    output_path = file_path.replace(f'.{file_ext}', f'_compressed.{file_ext}')
    ffmpeg_command = []

    if file_ext in ['jpg', 'jpeg']:
        try:
            with Image.open(file_path) as img:
                # Adjust quality for compression
                img.save(output_path, quality=60, optimize=True)
        except Exception as e:
            logging.error(f'Error during JPEG compression: {e}')
            return
    elif file_ext == 'png':
        try:
            with Image.open(file_path) as img:
                # Check if the png uses the alpha channel
                if img.mode == 'RGBA':
                    img = img.convert(
                        'RGBA', colors=256, dither=Image.Dither.FLOYDSTEINBERG)
                else:
                    img = img.convert(
                        'RGB', colors=256, dither=Image.Dither.FLOYDSTEINBERG)

                img.save(output_path, optimize=True, format='PNG')
        except Exception as e:
            logging.error(f'Error during PNG compression: {e}')
            return
    elif file_ext in ['mp4', 'mov', 'wav', 'avi', 'webp']:
        # Output always in mp4 format for these types
        output_path = file_path.replace(f'.{file_ext}', f'_compressed.mp4')
        ffmpeg_command = [
            'ffmpeg',
            '-i', file_path,
            '-vcodec', 'libx264',
            '-crf', '23',  # CRF value can be adjusted for different levels of compression
            output_path
        ]
    else:
        logging.error(f'Unsupported file type: {file_ext}')
        return

    if ffmpeg_command:
        try:
            subprocess.run(ffmpeg_command, check=True)
            logging.info(f'Compression successful: {output_path}')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error during compression: {e}')


if __name__ == '__main__':
    try:
        # Change the working directory to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        print("Parsing arguments")
        # Parse the command line argument for the target file path
        parser = argparse.ArgumentParser(
            description="Compress the specified file")
        parser.add_argument("path", help="The file to compress")
        args = parser.parse_args()
        target_file = args.path.replace('\\', '/').strip()
        print(f"Target file: {target_file}")

        # Compress the file
        print("Starting compression")
        compress_file(target_file)
        print("Done")

    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
