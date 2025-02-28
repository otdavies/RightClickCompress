import logging
import os
import argparse
import subprocess
from pathlib import Path


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logging.error(
            "FFmpeg not found. Please install FFmpeg to compress video files.")
        # Let's actually check the path for ffmpeg.exe
        # I probably don't have an env var, I'll need to iterate
        # over the PATH variable
        pathsChecked = 0
        for path in os.environ['PATH'].split(os.pathsep):
            ffmpeg_path = Path(path) / 'ffmpeg.exe'
            pathsChecked += 1
            if ffmpeg_path.exists():
                logging.info(f"Found FFmpeg at: {ffmpeg_path}")
                return True

        print(
            f"Checked all {pathsChecked} available path strings and couldn't find ffmpeg.exe")
        return False


def setup_pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        logging.info("Installing Pillow...")
        try:
            subprocess.run(['pip', 'install', 'Pillow'], check=True)
            from PIL import Image
            return Image
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install Pillow: {e}")
            return None


def compress_file(file_path: Path):
    if not file_path.exists():
        logging.error(f"File not found: {file_path}")
        return False

    file_ext = file_path.suffix.lower()[1:]
    output_path = file_path.parent / \
        f"{file_path.stem}_compressed{file_path.suffix}"

    if file_ext in ['jpg', 'jpeg', 'png']:
        Image = setup_pillow()
        if not Image:
            return False

        try:
            with Image.open(file_path) as img:
                if file_ext == 'png' and img.mode == 'RGBA':
                    img = img.convert('RGBA', colors=256)
                elif file_ext == 'png':
                    img = img.convert('RGB', colors=256)

                save_kwargs = {
                    'optimize': True,
                    'quality': 60 if file_ext in ['jpg', 'jpeg'] else None
                }
                img.save(
                    output_path, **{k: v for k, v in save_kwargs.items() if v is not None})
                logging.info(f"Image compressed successfully: {output_path}")
                return True

        except Exception as e:
            logging.error(f"Error compressing image: {e}")
            return False

    elif file_ext in ['mp4', 'mov', 'wav', 'avi', 'webp']:
        if not check_ffmpeg():
            return False

        output_path = file_path.parent / f"{file_path.stem}_compressed.mp4"
        ffmpeg_command = [
            'ffmpeg',
            '-i', str(file_path),
            '-vcodec', 'libx264',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            str(output_path)
        ]

        try:
            subprocess.run(ffmpeg_command, check=True, capture_output=True)
            logging.info(f"Video compressed successfully: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Error compressing video: {e.stderr.decode() if e.stderr else str(e)}")
            return False

    else:
        logging.error(f"Unsupported file type: {file_ext}")
        return False


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Compress the specified file")
    parser.add_argument("path", help="The file to compress")
    args = parser.parse_args()

    try:
        file_path = Path(args.path).resolve()
        logging.info(f"Processing file: {file_path}")
        compress_file(file_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        input("Press Enter to exit...")


if __name__ == '__main__':
    main()
