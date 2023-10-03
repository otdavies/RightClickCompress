# FFmpeg Installation Guide (Windows)

This guide walks through the steps to install FFmpeg on a Windows machine.

# Automatic Installation

 1. Run `attempt_ffmpeg_install.bat` once you've downloaded the repo.
 2. Pray. If it works, great! If not, continue to the manual installation steps below.


# Manual Installation

## 1. Download FFmpeg

- Download the FFmpeg executable from the official website:
  [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)

## 2. Extract the Zip File

- After the download completes, extract the zip file to a location of your choice, e.g., `C:\ffmpeg`.

## 3. Update System Path

- Right-click on 'This PC' or 'My Computer' on your desktop or in File Explorer, and select 'Properties'.
- Click on 'Advanced system settings'.
- Click on 'Environment Variables'.
- In the 'System variables' section, scroll down and select the 'Path' variable, then click on 'Edit'.
- Click on 'New' and add the path to the `bin` directory inside the extracted FFmpeg folder, e.g., `C:\ffmpeg\bin`.
- Click 'OK' to close each window.

## 4. Verify Installation

- Open a command prompt and type `ffmpeg -version` to verify the installation.

---

Now, FFmpeg should be installed and accessible from the command line.
