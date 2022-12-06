# slack_history_refresh
Transforming slack exports into history imports

Requirements:
- You have python 3.8 with installed packages: os, datetime, json, time, pprint

Instructions:
1. Download slack export zip file
2. Unzip into a directory named './slack_archive' (changeable in code)
3. Execute the program:  python process_archive.py
4. Create new zip file for slack import:
   - cd ./slack_archive
   - zip -r ../slack_archive_new.zip *
   - cd ..
5. Import the new archive into slack

