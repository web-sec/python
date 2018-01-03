#coding=utf8
import os
def getScanDirFiles():
    files = []
    try:
        with open('/Users/wf/Desktop/config/scan_dir') as f:
            all_the_text = f.read()
            all_the_text = all_the_text.strip()
            all_the_text = all_the_text.split('\n')
            for x in all_the_text:
                if not x:
                    all_the_text.remove(x)

            for x in all_the_text:
                fl = os.listdir(x)
                files+=fl
    except Exception as e:
        print(e)
    finally:
        return files

# paths = getScanDirFiles()
# print(paths)
