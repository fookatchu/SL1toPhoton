SL1toPhoton is a tool for converting PrusaSlicer's (previously Slic3r PE) SL1 files to Photon files for the Anycubic Photon 3D-Printer. Other cbddlp-files should also work (e.G. Elegoo Mars). It is largely based on [pyphotonfile](https://github.com/fookatchu/pyphotonfile), maintained by the same developer. The Photon S is currently not supported (see TODO). Anti-Aliasing with the new Firmware released in May 2019 is not supported. Please see the section about alternatives below if you need anti-aliasing support through chitubox.

Friendly Reminder
=================
   Use at your own risk. Please verify that what you are doing will not break your printer. This project also relies currently on beta software, so please be aware of future breaking changes.

PrusaSlicer Setup
=================
It is recommended to use PrusaSlicer 2.0.0-rc (previously Slic3rPE-1.42.0-beta2) or up, as this version added an option to disable anti-aliasing. Earlier versions will work, but the resulting Photon file will omit some pixels.

Steps:
 - Add a new SL1 Printer
 - Go to: Printer Settings -> General -> Corrections -> Printer gamma correction and set this to 0. This will disable anti-aliasing. This is currently recommended, since the Photon does not have support for this.

I would also recommend to increase the support thickness as the Photon does not have a tilting mechanism, which will increase pealing forces. I tried to copy the default settings from the AnyCubic Photon Slicer and came up with these values, which work ok:
 - Print Settings -> Supports -> Support head front diameter -> 0.8
 - Print Settings -> Supports -> Support pillar diameter -> 1.2

Further testing need to be done. I will add further recommendations, once they pop up. Please leave your test results and I will try to update this page with more informations.


Installation
========================================

Binarys
-------
Just get the latest release from the [releases](https://github.com/fookatchu/SL1toPhoton/releases) page and enjoy.


Source
------
Obviously clone or download the source first and change into the new folder.
```
git clone https://github.com/fookatchu/SL1toPhoton
cd SL1toPhoton
```

(Optional) I would recommend to create a new venv with and activate it:
```
python3 -m venv venv
source venv/bin/activate  # linux
venv\Scripts\activate     # win
```

For the full project:
```
pip install -r requirements.txt
```

If you don't want the GUI version with the PySide2 dependencys, just install

```
pip install pyphotonfile
```

If you want to build your own binarys:
```
pip install pyinstaller

# win
pyinstaller SL1_to_Photon.py --add-binary venv\Lib\site-packages\pyphotonfile\newfile.photon;pyphotonfile --onefile --clean
pyinstaller SL1_to_Photon_gui.py --add-binary venv\Lib\site-packages\pyphotonfile\newfile.photon;pyphotonfile --onefile --noconsole --clean

# mac (currently not working)
pyinstaller SL1_to_Photon.py --add-binary venv/lib/python3.7/site-packages/pyphotonfile/newfile.photon:pyphotonfile --onefile --clean
pyinstaller SL1_to_Photon_gui.py --add-binary venv/lib/python3.7/site-packages/pyphotonfile/newfile.photon:pyphotonfile --onefile --noconsole --clean
```
I am by no means fluent in pyinstaller, so if there is a way to remove the ugly binary import, please let me know.


Example Usage
========================================
The project currently hosts to seperate scripts: SL1_to_Photon.py which is the CLI version and the GUI version with the catchy name SL1_to_Photon_gui.py. The GUI is self-explanatory and the cli version looks like this:

```
python SL1_to_Photon.py --help
usage: SL1_to_Photon.py [-h] [-f] [-v] [-o OUTPUT] sl1_file

Convert an SL1 file to a Photon file.

positional arguments:
  sl1_file              SL1 file to convert.

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           overwrite existing files.
  -v, --verbose
  -o OUTPUT, --output OUTPUT
                        photon file output path.
```
Alternatives
========================================
PrusaSlicer now allows the export of STL's with supports as of PrusaSlicer 2.0.0-rc. You can export the prepared model and slice with another slicer which supports your printer directly.

TODO
====
- I would like to add support for the newer AnyCubic Photon S. I don't plan to buy that printer, so I am in need of external help. If you do have information about the file format, let me know.
- Remove binary dependency by creating a blank Photon file from scratch
