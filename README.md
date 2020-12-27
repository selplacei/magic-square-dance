# magic-square-dance

This program is a visual representation of the "Magic Square Dance" algorithm used to construct all tilings of an Aztec Diamond board, as described in this Mathologer video: https://www.youtube.com/watch?v=Yy7Q8IWNfHM

I'm not a mathematician, just thought this would be a fun program to make.

## How to run this program

Install Python (make sure it's Python 3.8 or later)  
Download this repository  
Open a terminal (command prompt on Windows)  
Go to the downloaded repository's directory (e.g. `cd ~/Downloads/magic-square-dance`)  
Run `pip install -r requirements.txt` (if you'd like to use a venv etc. you already know what you're doing)  
Launch `main.py` (if this opens a text editor, specify Python as the application)

## Usage

Assuming you've watched the video, it should be pretty straightforward - this program has a minimal feature set.  
Note that because QWidget doesn't utilize the GPU, the program can lag when drawing new boards of big enough sizes. I'm currently looking into using OpenGL instead, which should fix the performance issues.

## License

Copyright (c) 2020 Illia Boiko (selplacei)

All files in this repository are licensed under the Apache 2.0 License. The terms and conditions can be found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0.txt.
