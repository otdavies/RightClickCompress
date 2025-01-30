import os
import sys
import zipfile
import urllib.request
import subprocess
import ctypes
from pathlib import Path

def ensure_tqdm():
    try:
        from tqdm import tqdm
        return tqdm
    except ImportError:
        print("Installing required dependency...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm", "--quiet"])
        from tqdm import tqdm
        return tqdm

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
    tqdm = ensure_tqdm()
    local_filename = "ffmpeg.zip"
    
    response = urllib.request.urlopen(FFMPEG_URL)
    total_size = int(response.headers.get('content-length', 0))
    
    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading FFmpeg") as pbar:
        with open(local_filename, 'wb') as out_file:
            while True:
                buffer = response.read(8192)
                if not buffer:
                    break
                out_file.write(buffer)
                pbar.update(len(buffer))
    
    return local_filename

def extract_ffmpeg(zip_filepath):
    tqdm = ensure_tqdm()
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        total_size = sum(file.file_size for file in zip_ref.filelist)
        extracted_size = 0
        
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Extracting FFmpeg") as pbar:
            for file in zip_ref.filelist:
                zip_ref.extract(file)
                extracted_size += file.file_size
                pbar.update(file.file_size)
    
    absolute_path = Path(os.getcwd()).resolve()
    ffmpeg_dir = next((folder for folder in os.listdir(absolute_path)
                      if os.path.isfile(os.path.join(absolute_path, folder, "bin", "ffmpeg.exe"))), None)
    
    if not ffmpeg_dir:
        raise FileNotFoundError("Could not find FFmpeg directory after extraction")
    
    bin_path = os.path.join(absolute_path, ffmpeg_dir, "bin")
    return str(Path(bin_path).resolve())

def add_to_path(directory):
    current_path = os.environ.get("PATH", "")
    paths = current_path.split(os.pathsep)
    
    if directory not in paths:
        new_path = os.pathsep.join([current_path, directory])
        print(f"Adding to PATH: {directory}")
        subprocess.run(['setx', 'PATH', new_path], check=True)
        os.environ["PATH"] = new_path

def main():
    ffmpeg_installed = subprocess.run(
        ["where", "ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        
    if not ffmpeg_installed:
        if not is_admin():
            print("Requesting admin rights to install FFmpeg.")
            run_as_admin()
            return

        print("Installing FFmpeg...")
        zip_filepath = download_ffmpeg()
        ffmpeg_dir = extract_ffmpeg(zip_filepath)
        print(f"Adding to PATH: {ffmpeg_dir}")
        add_to_path(ffmpeg_dir)
        print("FFmpeg installation complete.")
        os.remove(zip_filepath)
    else:
        print("FFmpeg is already installed.")

if __name__ == "__main__":
    main()
    input("Press enter to exit...")