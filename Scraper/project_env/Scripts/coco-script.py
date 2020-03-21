#!c:\users\kwant\documents\github\covid-19-response-index\scraper\project_env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'country-converter==0.6.7','console_scripts','coco'
__requires__ = 'country-converter==0.6.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('country-converter==0.6.7', 'console_scripts', 'coco')()
    )
