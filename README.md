SL1toPhoton is a tool for converting Slic3r PE's SL1 files to Photon files for the Anycubic Photon 3D-Printer. It is largely based on [pyphotonfile](https://github.com/fookatchu/pyphotonfile), maintained by the same developer.

Friendly Reminder
=================
   Use at your own risk. Please verify that what you are doing will not break your printer. This project also relies currently on beta software, so please be aware of future breaking changes.

Slic3r PE Setup
=================
It is recommended to use Slic3rPE-1.42.0-beta2 or up, as this version added an option to disable anti-aliasing. Earlier versions will work, but the resulting Photon file will omit some pixels.

Steps:
 - Add a new SL1 Printer
 - Go to: Printer Settings -> General -> Corrections -> Printer gamma correction and set this to 0. This will disable anti-aliasing for the Photon.

Installation (under construction)
========================================
Until I can provide a proper release with binarys, please follow these steps:

 - Clone repo with "git clone https://github.com/fookatchu/SL1toPhoton"
 - get a whl copy of pyphotonfile from https://github.com/fookatchu/pyphotonfile/releases
 - Inside the project folder run:
    - (Optional) create a virtual env with "python -m venv venv" and activate.
    - pip install path-to/pyphotonfile-0.1-py3-none-any.whl

Example Usage
========================================
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

TODO
========================================
- Add compiled binarys for easier usage