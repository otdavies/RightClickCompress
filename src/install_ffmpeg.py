import os
import sys
import zipfile
import urllib.request
import subprocess
import ctypes

# FFMpeg mirror URL, adjust to your preferred FFmpeg mirror link
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def download_ffmpeg():
    local_filename = "ffmpeg.zip"
    with urllib.request.urlopen(FFMPEG_URL) as response, open(local_filename, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    return local_filename


def extract_ffmpeg(zip_filepath):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(".")
    # Get the name of the folder extracted, the first folder with an ffmpeg.exe file
    ffmpeg_dir = next((folder for folder in os.listdir(
        os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), folder, "bin", "ffmpeg.exe"))), None)
    # Add bin to the path
    folder_name = os.path.join(ffmpeg_dir, "bin")
    # Return the full path to the bin folder
    return os.path.join(os.getcwd(), folder_name)


def add_to_path(directory):
    # Get the current PATH
    path = os.environ.get("PATH", "")
    # Check if the directory is already in the PATH
    if directory not in path:
        # Add the directory to the PATH
        print("Adding to PATH: " + f'{path};{directory}')
        subprocess.run(['setx', 'PATH', f'{path};{directory}'], check=True)


def main():
    # Check if FFmpeg is already installed
    ffmpeg_installed = subprocess.run(
        ["where", "ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    if not ffmpeg_installed:
        if not is_admin():
            print("Didn't find FFmpeg, we need admin rights to install it.")
            print("Requesting admin rights, this is just to install FFmpeg to your PATH.")
            run_as_admin()
            return

        print("FFmpeg not found, we are going to attempt to install FFMpeg for you. God help us.")
        print(f"Downloading around ~100mb... this will take a moment.")
        zip_filepath = download_ffmpeg()
        print("Download complete, extracting to " + os.getcwd() + zip_filepath)
        ffmpeg_dir = extract_ffmpeg(zip_filepath)
        print("Extraction complete, adding to PATH...")
        add_to_path(ffmpeg_dir)
        print("FFMpeg is now installed, hopefully. No promises lol.")
        # Delete .zip file
        os.remove(zip_filepath)
    else:
        print("FFmpeg is already installed, that was easy.")


if __name__ == "__main__":
    main()
    input("Press enter to exit...")
