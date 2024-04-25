# IMPORTANT
This version of the program is the deprecated Python version, this repo will remain available for archival purposes, but will no longer be updated. For the new version of this program, written in Rust, go [here](https://github.com/sykesgabri/AutoTCLog-RS).

# AutoTCLog
Writing timecode logs manually is tedious and time consuming. AutoTCLog gets the worst of it done fast so you only have to fill in the easy parts.

## Dependencies
* Python 3
* Pandas (install with `pip install pandas`)
* OpenPyXL (install with `pip install openpyxl`)
* Colorama (install with `pip install colorama`)
* FFmpeg

## Installing Python 3
AutoTCLog is programmed in Python 3. Python 3 must be installed on your computer for the program to work. Here's how to install Python 3 on Windows, MacOS, or Linux:

Windows:
* Go to https://www.python.org/downloads/windows/ and click the link that says "Latest Python 3 Release", choose "Windows installer (64-bit)" under files at the bottom of the page.
* Open the installer, make sure that "Use admin privileges when installing py.exe" and "Add python.exe to PATH" are checked, click "Customize installation", make sure all optional features are checked, check "Install for all users" under advanced options, do not customize install location, click "Install".
* When the install is finished, click "Disable PATH length limit."
* Restart your PC.

MacOS:
* Install Homebrew from https://brew.sh/
* Open a terminal and run the following command: `brew install python3`

Linux:
* Use your distro's package manager to install the `python` or `python3` package

## Installing FFmpeg
AutoTCLog uses FFmpeg to extract video metadata. FFmpeg must be installed on your computer for the program to work. Here's how to install FFmpeg on Windows, MacOS, or Linux:

Windows:
* Download the FFmpeg Windows binary from https://ffmpeg.org/download.html#build-windows
* Extract the downloaded archive to a folder of your choice
* Add the FFmpeg executable to your system's PATH environment variable

MacOS:
* Install Homebrew from https://brew.sh/
* Open a terminal and run the following command: `brew install ffmpeg`

Linux:
* Use your distro's package manager to install the `ffmpeg` package

## Using AutoTCLog
1. Clone this repository to your computer by opening a terminal and typing `git clone https://github.com/sykesgabri/AutoTCLog`. Alternatively, you can click the green "Code" button on this repository, click "Download ZIP", then extract the ZIP file
2. Open a terminal and navigate to the AutoTCLog folder
3. Type the command `python3 autotclog.py`
4. Follow the instructions provided to you by the program

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
