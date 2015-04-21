# android-scraper
Tools and program to scrape through android apps and determine information about them

## License
BSD 2-Clause [Simplified] license.

## Usage
You will need a path to the uncompressed directory using our [Android Decompiler](https://github.com/kocsenc/android-scraper/tree/master/tools/apk-decompiler/)

So you may use it directly from command line
```
python Driver.py path/to/uncompressedapk
```

Or you can use it as a python module
```python
import Driver

analyze_app("/path/to/uncompressed apk)
```

## Dependencies
- MySQL Connector for python (ONLY if we want the apps to save to the DB)

## Install Instructions
TBD

## Tools Available
### [Android Decompiler](https://github.com/kocsenc/android-scraper/tree/master/tools/apk-decompiler/)
An all in one solution to turning an APK file into readable XML and uncompiled code.
Uses dex2jar, procyon decompiler and apktools.
Find it [here](https://github.com/kocsenc/android-scraper/tree/master/tools)

