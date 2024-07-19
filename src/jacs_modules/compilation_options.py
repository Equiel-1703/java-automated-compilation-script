import json
import os
import sys

from jacs_modules.terminal_colors import TerminalColors

class CompilationOptions:
	_name_of_file = "compilation_options.json"
	_directory_path = os.path.abspath(os.path.join(os.path.pardir, "config"))

	src_folder: str
	main_class_path: str
	class_path: str
	verbose: bool
	encoding: str
	compiler: str

	def __init__(self, *args) -> None:
		self.verbose = False
		self.encoding = "UTF-8"
		self.compiler = "javac"

		if len(args) == 2:
			self.set_src_folder(args[0])
			self.main_class_path = args[1]
			
			# If the class path is not specified, we will use the source folder as the class path
			self.class_path = self.src_folder
		elif len(args) == 3:
			self.set_src_folder(args[0])
			self.main_class_path = args[1]
			self.set_class_path(args[2])
		else:
			self.src_folder = ""
			self.main_class_path = ""
			self.class_path = ""
	
	def __str__(self) -> str:
		return f"+ Source folder: {self.src_folder}\n+ Main class path: {self.main_class_path}\n+ Class path: {self.class_path}\n+ Verbose: {self.verbose}\n+ Encoding: {self.encoding}\n+ Compiler: {self.compiler}"

	def _validate_folder(self, folder_path) -> str:
		"""
		Validates the received folder. If the folder does not exist or it is not a path, the program will exit with an error message.

		If it's a valid folder, the absolute path of the folder will be returned.

		Args:
			folder_path (str): The path of the folder to validate.
		
		Returns:
			str: The absolute path of the folder.
		"""
		# Get the absolute path of the folder
		absolute_path = os.path.abspath(folder_path)

		# Check if the folder exists and is a folder in fact
		if not os.path.exists(absolute_path) or not os.path.isdir(absolute_path):
			print(f"{TerminalColors.FAIL}Error> The folder \"{os.path.basename(absolute_path)}\" does not exist!{TerminalColors.ENDC}", file=sys.stderr)
			exit(1)
		
		return absolute_path
	
	def set_verbose(self, verbose: bool) -> None:
		"""
		Sets the verbose option.

		Args:
			verbose (bool): The value to set.
		"""
		self.verbose = verbose
	
	def set_encoding(self, encoding: str) -> None:
		"""
		Sets the encoding option.

		Args:
			encoding (str): The value to set.
		"""
		self.encoding = encoding
	
	def set_compiler(self, compiler: str) -> None:
		"""
		Sets the compiler option.

		Args:
			compiler (str): The value to set.
		"""
		self.compiler = compiler

	def set_src_folder(self, src_folder: str) -> None:
		"""
		Sets the source folder option.

		Args:
			src_folder (str): The value to set.
		"""
		self.src_folder = self._validate_folder(src_folder)

	def set_main_class_path(self, main_class_path: str) -> None:
		"""
		Sets the main class path option.

		Args:
			main_class_path (str): The value to set.
		"""
		self.main_class_path = main_class_path

	def set_class_path(self, class_path: str) -> None:
		"""
		Sets the class path option.

		Args:
			class_path (str): The value to set.
		"""
		self.class_path = self._validate_folder(class_path)

	@staticmethod
	def check_if_compilation_options_file_exists() -> bool:
		"""
		Checks if the compilation options file exists in its default directory.

		Returns:
			bool: True if the file exists, False otherwise.
		"""
		return os.path.exists(os.path.join(CompilationOptions._directory_path, CompilationOptions._name_of_file))
	
	@staticmethod
	def load_compilation_options_file() -> "CompilationOptions":
		"""
		Loads the compilation options from the path specified. The name of the file must be %s.

		Returns:
			CompilationOptions: The CompilationOptions object with the loaded options.
		""".format(CompilationOptions._name_of_file)

		path = os.path.join(CompilationOptions._directory_path, CompilationOptions._name_of_file)

		# Load the dictionary from the file
		with open(path, "r") as file:
			compilation_options = json.load(file)
		
		# Create a new CompilationOptions object with the loaded options
		compilation_options_obj = CompilationOptions()

		# It is a good idea to define later a JSON Schema to validate the file

		compilation_options_obj.set_src_folder(compilation_options["src_folder"])
		compilation_options_obj.set_main_class_path(compilation_options["main_class_path"])
		compilation_options_obj.set_class_path(compilation_options["class_path"])
		compilation_options_obj.set_verbose(compilation_options["verbose"])
		compilation_options_obj.set_encoding(compilation_options["encoding"])
		compilation_options_obj.set_compiler(compilation_options["compiler"])

		return compilation_options_obj
	
	def create_compilation_options_file(self) -> None:
		"""
		Creates a compilation options file with the name %s in the specified path.

		The options saved are the current ones of this object.
		
		Args:
			path (str): The path to create the file in.
		""".format(self._name_of_file)

		# Create the dictionary with the compilation options
		compilation_options = {
			"src_folder": self.src_folder,
			"main_class_path": self.main_class_path,
			"class_path": self.class_path,
			"verbose": self.verbose,
			"encoding": self.encoding,
			"compiler": self.compiler
		}

		path = os.path.join(self._directory_path, self._name_of_file)

		# Write the dictionary to the file
		with open(path, "w") as file:
			json.dump(compilation_options, file, indent=4)