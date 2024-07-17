import json
import os
import sys

from terminal_colors import TerminalColors

class CompilationOptions:
	_name_of_file = "compilation_options.json"

	def __init__(self, *args) -> None:
		self.verbose = False
		self.encoding = "UTF-8"
		self.compiler = "javac"

		if len(args) == 1:
			self.src_folder = self._validate_folder(args[0])
			# If the class path is not specified, we will use the source folder as the class path
			self.class_path = self.src_folder
		else:
			self.src_folder = self._validate_folder(args[0])
			self.class_path = self._validate_folder(args[1])

	def _validate_folder(self, folder_path) -> str:
		"""
		Validates the received folder. If the folder does not exist or it is not a path, the program will exit with an error message.

		This function returns the absolute path of the folder, if it valid.

		Args:
			folder_path (str): The path of the folder to validate.
		"""
		# Get the absolute path of the folder
		absolute_path = os.path.abspath(folder_path)

		# Check if the folder exists and is a folder in fact
		if not os.path.exists(absolute_path) or not os.path.isdir(absolute_path):
			print(f"{TerminalColors.FAIL}Error> The folder \"{os.path.basename(absolute_path)}\" does not exist!{TerminalColors.ENDC}", file=sys.stderr)
			exit(1)
		
		return absolute_path
	
	def check_if_compilation_options_file_exists(self, path: str) -> bool:
		"""
		Checks if the compilation options file exists in the specified path.

		Args:
			path (str): The path to check if the file exists.

		Returns:
			bool: True if the file exists, False otherwise.
		"""
		return os.path.exists(os.path.join(path, self._name_of_file))

	def create_compilation_options_file(self, path: str) -> None:
		"""
		Creates a compilation options file with the name %s in the specified path.

		The options saved are the current ones of this object.
		
		Args:
			path (str): The path of the file to create.
		""".format(self._name_of_file)

		# Create the dictionary with the compilation options
		compilation_options = {
			"verbose": self.verbose,
			"encoding": self.encoding,
			"compiler": self.compiler,
			"class_path": self.class_path,
			"src_folder": self.src_folder
		}

		# Write the dictionary to the file
		with open(path, "w") as file:
			json.dump(compilation_options, file, indent=4)
	
	def load_compilation_options_file(self, path: str) -> None:
		"""
		Loads the compilation options from the path specified. The name of the file must be %s.

		Args:
			path (str): The path of the file to load.
		""".format(self._name_of_file)

		path = os.path.join(path, self._name_of_file)

		# Load the dictionary from the file
		with open(path, "r") as file:
			compilation_options = json.load(file)
		
		# Set the compilation options
		self.verbose = compilation_options["verbose"]
		self.encoding = compilation_options["encoding"]
		self.compiler = compilation_options["compiler"]
		self.class_path = compilation_options["class_path"]
		self.src_folder = compilation_options["src_folder"]

			
		