# chromedriver-binary
Downloads and installs the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) binary version 88.0.4324.27 for automated testing of webapps. The installer supports Linux, MacOS and Windows operating systems.

Alternatively the package [proxied-chromedriver-binary-auto](https://pypi.org/project/proxied-chromedriver-binary-auto/) can be used to automatically detect the latest chromedriver version required for the installed Chrome/Chromium browser.

## Installation

### Latest and fixed versions

#### From PyPI
```
pip install proxied-chromedriver-binary
```

#### From GitHub
```
pip install git+https://github.com/imanazari70/proxied-chromedriver-binary-auto
```

### Automatically detected versions

Please make sure to install Chrome or Chromium first and add the browser to the binary search path.

#### From PyPI
```
pip install proxied-chromedriver-binary-auto
```

To redetect the required version and install the newest suitable chromedriver after the first installation simply reinstall the package using
```
pip install --upgrade --force-reinstall proxied-chromedriver-binary-auto
```

#### From GitHub
```
pip install git+https://github.com/imanazari70/proxied-chromedriver-binary-auto
```

## Usage
To use chromedriver just `import chromedriver_binary`. This will add the executable to your PATH so it will be found. You can also get the absolute filename of the binary with `chromedriver_binary.chromedriver_filename`.

### Example
```
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```

### Exporting chromedriver binary path
This package installs a small shell script `chromedriver-path` to easily set and export the PATH variable:
```
$ export PATH=$PATH:`chromedriver-path`
```
