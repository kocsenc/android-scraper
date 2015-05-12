# android-scraper
Tools and program to scrape through android apps and determine information about them

## License
BSD 2-Clause [Simplified] license.

## Usage
Note: In order to use this application, you will need a path to the uncompressed android app directory using our [Android Decompiler](https://github.com/kocsenc/android-scraper/tree/master/tools/apk-decompiler/).

There are two main ways to run this:
- Single mode
- Batch mode

### Single Run Mode

So you may use it directly from command line
```
python Driver.py path/to/uncompressedapk
```

Or you can use it as a python module
```python
import Driver

analyze_app("/path/to/uncompressedapk")
```

### Batch Mode
Batch mode allows you to run the analyses on a large body of apps. Used for mass information gathering.

```
python BatchRun.py /path/to/apks /path/to/file/with/apknames.txt /path/to/decompiler.sh [SKIP_VAL]
```
Parameter Explanations:
- `/path/to/apks`: is the directory path to where all the apks are located
- `/path/to/file/with/apknames.txt`: is a path to a file which has each name of app to analyze per line
- `/path/to/decompiler`: this is the path to the [decomipler we provide](https://github.com/kocsenc/android-scraper/tree/master/tools/apk-decompiler/).
- `SKIP_VAL`: (Optional) a number of number of apps to skip when going through them. (i.e. SKIP_VAL = 5 would ignore the first 5 apks and continue analyzing on the 6th one).


## Dependencies
- MySQL Connector for Python. ([Useful installation guide](https://geert.vanderkelen.org/installing-coy-using-pip/))


## Tools Available
### [Android Decompiler](https://github.com/kocsenc/android-scraper/tree/master/tools/apk-decompiler/)
An all in one solution to turning an APK file into readable XML and uncompiled code.
Uses dex2jar, procyon decompiler and apktools.
Find it [here](https://github.com/kocsenc/android-scraper/tree/master/tools)

