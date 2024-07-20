from os import path as path
import os
import sys
import shutil

PROG_NAME = "Jacs"

BAT_FILE = "jacs.bat"
PROG_FILE = "jacs.py"
MODULES_FOLDER = "jacs_modules"

SRC_PATH = path.join(path.dirname(path.abspath(__file__)), "src")
BAT_PATH = path.join(SRC_PATH, "bat", BAT_FILE)
PROG_PATH = path.join(SRC_PATH, PROG_FILE)
MODULES_PATH = path.join(SRC_PATH, MODULES_FOLDER)

if __name__ == "__main__":
	path_to_install = input(f"Where you want to install {PROG_NAME}? ").strip()

	if not path.exists(path_to_install) or not path.isdir(path_to_install):
		print(f"ERROR> Path '{path_to_install}' does not exist or is not a folder.", file=sys.stderr)
		exit(1)
	else:
		path_to_install = path.abspath(path_to_install)
	
	# Create a folder inside the path to install
	folder_name = PROG_NAME.lower()
	path_to_install_folder = path.join(path_to_install, folder_name)

	if not path.exists(path_to_install_folder):
		os.mkdir(path_to_install_folder)

	# Copy the program files
	try:
		shutil.copy(BAT_PATH, path_to_install)
		shutil.copy(PROG_PATH, path_to_install_folder)
		shutil.copytree(MODULES_PATH, path.join(path_to_install_folder, MODULES_FOLDER), dirs_exist_ok=True)
	except Exception as e:
		print(f"ERROR> {e}", file=sys.stderr)
		exit(1)
	
	print(f"{PROG_NAME} installed successfully in '{path_to_install_folder}'!")
	exit(0)
	
