# Right Click Compress
![explorer_JJ2bMnfl24](https://github.com/otdavies/RightClickCompress/assets/3145170/7a55ed7d-e930-414d-9b7b-0acab83c6520)
-----

https://github.com/otdavies/RightClickCompress/assets/3145170/75359f65-21fe-4447-a973-295419db7f1f


This project adds right-click context menu options in Windows for compressing images and videos without significant loss in visual quality. 

Note: In some cases (especially with .png) the image may not reduce in size if it has already been compressed.

## Features

- Adds context menu options for compressing images and videos.
- Supports a variety of file formats including `.jpg`, `.jpeg`, `.png`, `.mp4`, `.mov`, `.wav`, `.avi`, and `.webp`.
- Utilizes FFmpeg for compression.

## Requirements

- Python 3.x
- Windows OS
- FFmpeg

## Installation

1. Clone or download the repository to your local machine.
2. Ensure [FFmpeg](FFMPEG.md) is installed and added to your system PATH.
3. Run `install.bat` to add the context menu options.
   - This will create registry entries for the context menu options.
4. (Optional) Run `uninstall.bat` as an administrator to remove the context menu options if needed.

## Usage

1. Right-click on a supported file.
2. Select 'Compress' from the context menu to compress the file.
   - Compressed images will retain their original file format.
   - Compressed videos will be output as `.mp4` files.

## File Structure

- `src/`
  - `install.py`: Script for installing the context menu options.
  - `uninstall.py`: Script for uninstalling the context menu options.
  - `compress.py`: Script for handling compression tasks.
  - `run.bat`: Batch file for executing `compress.py` from the context menu.
- `README.md`: Project documentation.
- `install.bat`: A batch file to make running install.py easier.
- `uninstall.bat`: A batch file to make running uninstall.py easier.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or create issues for bugs and feature requests.


MIT License - see the [LICENSE](LICENSE) file for details.
