import os
import sys
import subprocess

from jacs_modules.exceptions import *
from jacs_modules.compilation_options import CompilationOptions
from jacs_modules.terminal_colors import TerminalColors

def show_menu(compilation_options: CompilationOptions) -> str:
	"""
	Shows a menu with the available options to the user and the path of the informed source folder.

	Args:
		compilation_options (CompilationOptions): The compilation options to use when compiling the files.
	
	Returns:
		str: The choice made by the user.
	"""
	print(f"{TerminalColors.HEADER} - Automated Java Compilation Script by Equiel_1703 - {TerminalColors.ENDC}")
	print(f"{TerminalColors.OKCYAN}")
	print(f"\t+ Source Folder (absolute path): {compilation_options.src_folder}")
	print(f"\t+ Class Path (absolute path): {compilation_options.class_path}")
	print(f"\t+ Main Class Path: {compilation_options.main_class_path}")
	print(f"{TerminalColors.ENDC}")
	print("Choose an option:")
	print("1. Compile all Java files in the source folder")
	print("2. Compile specific Java files in the source folder")
	print("3. Clear build")
	print("4. Compile and run project")
	print("5. Setup compilation options")
	print("0. Exit")

	choice = input().strip()
	return choice

def _posorder_traversal(folder, condition) -> list[str]:
	"""
	Recursively traverses a folder and its subfolders in postorder,
	returning a list of absolute paths of files that satisfy the condition function.

	Args:
		folder (str): The absolute path of the folder to traverse.
		condition (function): A function that receives a file path and returns a boolean value.

	Returns:
		list[str]: A list of absolute paths of the files that satisfy the condition function
	"""
	list_of_files = []
	# Get list of files and folders in the received folder
	files = os.listdir(folder)

	for file in files:
		# Join the folder path with the file/folder
		file = os.path.join(folder, file)

		if os.path.isdir(file):
			# If the file is a folder, recursively traverse it and add the files to the list
			list_of_files.extend(_posorder_traversal(file, condition))
		elif condition(file):
			# If "file" is a file, we must add it to the list - only if it satisfies the condition
			list_of_files.append(file)
	
	# Return the list of files
	return list_of_files

def _compile_file(path_to_file: str, compilation_options: CompilationOptions) -> None:
	"""
	Compiles a Java file.

	Args:
		path_to_file (str): The absolute path of the file to compile.
		compilation_options (CompilationOptions): The compilation options to use when compiling the file.
	"""
	# Elaboring command to compile the files
	command = [compilation_options.compiler, "-cp", compilation_options.class_path, "-encoding", compilation_options.encoding]

	if compilation_options.verbose:
		command.append("-verbose")

	# Compile the file
	result = subprocess.run(command + [path_to_file], capture_output=True, text=True)

	if compilation_options.class_path == compilation_options.src_folder:
		print(f"{TerminalColors.WARNING}NOTE> the -cp provided to the Java compiler was the Source Folder path. If you want a different one, change the compilation options.{TerminalColors.ENDC}")

	if result.returncode != 0:
		print(f"{TerminalColors.FAIL}Error> Could not compile the file \"{path_to_file}\"!", file=sys.stderr)
		print(f"Compilation aborted.{TerminalColors.ENDC}", file=sys.stderr)
		print("\n" + result.stderr, file=sys.stderr)

		raise CompilationError(f"Could not compile the file \"{path_to_file}\".")

def _process_args() -> CompilationOptions:
	"""
	Processes the arguments provided by the user and returns the compilation options based on them.

	Returns:
		CompilationOptions: The compilation options based on the arguments provided by the user
	"""

	# Check if the user provided too many arguments
	if len(sys.argv) > 4:
		print(f"{TerminalColors.FAIL}Error> Too many arguments provided!{TerminalColors.ENDC}", file=sys.stderr)
		print(f"Usage: python {sys.argv[0]} [source_folder] [class_path]", file=sys.stderr)
		exit(1)

	if len(sys.argv) == 1:
		# If no arguments were provided, we must ask the user for the source folder and the main class path
		src_folder = input("Folder containing the source code: ").strip()
		main_path = input("Main class path: ").strip()
	elif len(sys.argv) == 2:
		# If the user provided a single argument, we must use it as the source folder and ask for the main class path
		src_folder = sys.argv[1]
		main_path = input("Main class path: ").strip()
	elif len(sys.argv) == 3:
		# If the user provided two arguments, we must use them as the source folder and the main class path
		src_folder = sys.argv[1]
		main_path = sys.argv[2]
	
	if len(sys.argv) == 4:
		# If the user provided three arguments, we must use them as the source folder, the main class path, and the class path
		src_folder = sys.argv[1]
		main_path = sys.argv[2]
		class_path = sys.argv[3]

		# Create compilation options
		compilation_options = CompilationOptions(src_folder, main_path, class_path)
	else:
		# Check if user want to define the class path
		class_path = input("Class path (leave empty to use the source folder as the class path): ").strip()
		
		if class_path == "":
			class_path = src_folder
		
		# Create compilation
		compilation_options = CompilationOptions(src_folder, main_path, class_path)
	
	return compilation_options

def compile_all_files(compilation_options: CompilationOptions) -> None:
	"""
	Compiles all Java files in the source folder.

	Args:
		compilation_options (CompilationOptions): The compilation options to use when compiling the files.
	"""
	# Get the list of files that will be compiled
	files_to_compile = _posorder_traversal(compilation_options.src_folder, lambda file: file.endswith(".java"))

	# Print the list of files
	print("Files to compile:")
	for file in files_to_compile:
		print("+ " + file)

	try:
		# Now we can compile the files in the list
		for file in files_to_compile:
			print(f"\n{TerminalColors.OKCYAN}Compiling file: {file}{TerminalColors.ENDC}")
			_compile_file(file, compilation_options)
	except CompilationError:
		print(f"\n{TerminalColors.FAIL}Error> Could not compile all files!{TerminalColors.ENDC}", file=sys.stderr)
		return

	print(f"\n{TerminalColors.OKGREEN}Compilation finished!{TerminalColors.ENDC}")
	print(f"Total of {len(files_to_compile)} files compiled.")

def compile_specific_files(compilation_options: CompilationOptions) -> None:
	"""
	Compiles specific Java files in the source folder.

	Args:
		compilation_options (CompilationOptions): The compilation options to use when compiling.
	"""
	files_available = _posorder_traversal(compilation_options.src_folder, lambda file: file.endswith(".java"))

	# Print the list of files to the user
	print("Files available to compile:")
	for i, file in enumerate(files_available):
		print(f"{i + 1}. {file.removeprefix(compilation_options.src_folder + os.sep)}")
	
	# Ask the user which files they want to compile
	files_to_compile = input("\nChoose the files to compile (separated by commas): ").split(",")
	files_to_compile = map(str.strip, files_to_compile)
	files_to_compile = [*filter(lambda file_index: file_index.isdigit() and 1 <= int(file_index) <= len(files_available), files_to_compile)]

	if len(files_to_compile) == 0:
		print(f"{TerminalColors.FAIL}Error> No files were selected!{TerminalColors.ENDC}", file=sys.stderr)
		return
	
	# Get the files paths
	files_to_compile = list(map(lambda file_index: files_available[int(file_index) - 1], files_to_compile))

	try:
		for file in files_to_compile:
			print(f"\n{TerminalColors.OKCYAN}Compiling file: {file}{TerminalColors.ENDC}")
			_compile_file(file, compilation_options)
	except CompilationError:
		print(f"\n{TerminalColors.FAIL}Error> Could not compile all files!{TerminalColors.ENDC}", file=sys.stderr)
		return
	
	print(f"\n{TerminalColors.OKGREEN}Compilation finished!{TerminalColors.ENDC}")
	print(f"Total of {len(files_to_compile)} files compiled.")

def clear_build(compilation_options) -> None:
	"""
	Removes all .class files from the source folder.

	Args:
		compilation_options (CompilationOptions): The compilation options to use when removing the files.
	"""
	files_to_delete = _posorder_traversal(compilation_options.src_folder, lambda file: file.endswith(".class"))

	# Print to the user
	print(f"{TerminalColors.OKCYAN}Cleaning build...{TerminalColors.ENDC}")
	print()

	for file in files_to_delete:
		os.remove(file)
		print(f"{TerminalColors.WARNING}Deleted: {file}{TerminalColors.ENDC}")
	
	print(f"\n{TerminalColors.OKGREEN}Build cleaned!{TerminalColors.ENDC}")

def compile_and_run_project(compilation_options: CompilationOptions):
	"""
	Compiles and runs the project.

	Args:
		compilation_options (CompilationOptions): The compilation options to use when compiling and running the project.
	"""
	# Get path of the main file
	main_file = os.path.join(compilation_options.src_folder, compilation_options.main_class_path.replace(".", os.sep) + ".java")
	
	# Compile the main file
	_compile_file(main_file, compilation_options)

	# Run the project
	command = ["java", "-cp", compilation_options.class_path, compilation_options.main_class_path]
	result = subprocess.run(command, capture_output=True, text=True)

	if result.returncode != 0:
		print(f"{TerminalColors.FAIL}Error> Could not run the project!{TerminalColors.ENDC}", file=sys.stderr)
		print("\n" + result.stderr, file=sys.stderr)
		return

	print("\n" + result.stdout)

def setup_compilation_options(compilation_options: CompilationOptions):
	"""
	Setup the compilation options for the program.

	Args:
		compilation_options (CompilationOptions): The compilation options to setup.
	"""
	while True:
		# Print current compilation options
		print(f"{TerminalColors.OKBLUE}Current compilation options:\n{compilation_options}{TerminalColors.ENDC}")

		# Ask the user what they want to change
		print("\nChoose the option to change:")
		print("1. Source folder")
		print("2. Main class path")
		print("3. Class path")
		print("4. Verbose")
		print("5. Encoding")
		print("6. Compiler")
		print("0. Return")

		choice = input().strip()

		if choice == "1":
			# Change the source folder
			src_folder = input("New source folder: ").strip()
			compilation_options.set_src_folder(src_folder)
		elif choice == "2":
			# Change the main class path
			main_class_path = input("New main class path: ").strip()
			compilation_options.set_main_class_path(main_class_path)
		elif choice == "3":
			# Change the class path
			class_path = input("New class path: ").strip()
			compilation_options.set_class_path(class_path)
		elif choice == "4":
			# Change the verbose option
			verbose = input("Verbose (y/n): ").strip().lower()
			if verbose == "y":
				compilation_options.set_verbose(True)
			else:
				compilation_options.set_verbose(False)
		elif choice == "5":
			# Change the encoding
			encoding = input("New encoding: ").strip()
			compilation_options.set_encoding(encoding)
		elif choice == "6":
			# Change the compiler
			compiler = input("New compiler: ").strip()
			compilation_options.set_compiler(compiler)
		elif choice == "0":
			break
		else:
			print(f"{TerminalColors.FAIL}Error> Invalid choice! Try again.{TerminalColors.ENDC}", file=sys.stderr)
			os.system(clear_command)
			continue
	
	compilation_options.create_compilation_options_file()
	print(f"{TerminalColors.OKGREEN}Compilation options updated!{TerminalColors.ENDC}")

# Main program
if __name__ == "__main__":
	# Check if the user is using Windows or not
	if os.name == "nt":
		# If the OS is Windows, we must enable colors in the terminal
		os.system("color")
		# Also, we must use the "cls" command to clear the terminal
		clear_command = "cls"
	else:
		# If the OS is not Windows, we must use the "clear" command
		clear_command = "clear"

	# Check if the compilation options file exists
	if CompilationOptions.check_if_compilation_options_file_exists():
		# If the file exists, we must load the compilation options from it
		compilation_options = CompilationOptions.load_compilation_options_file()
	else:
		# If the file does not exist, we must process the arguments provided by the user
		compilation_options = _process_args()
		# And create the compilation options file
		compilation_options.create_compilation_options_file()

	# Program loop
	while True:
		choice = show_menu(compilation_options)

		if choice == "1":
			# Compile all Java files in the source folder
			os.system(clear_command)
			compile_all_files(compilation_options)
		elif choice == "2":
			# Compile specific Java files in the source folder
			os.system(clear_command)
			compile_specific_files(compilation_options)
		elif choice == "3":
			# Clear build
			os.system(clear_command)
			clear_build(compilation_options)
		elif choice == "4":
			# Compile and run project
			os.system(clear_command)
			compile_and_run_project(compilation_options)
		elif choice == "5":
			# Setup compilation options
			os.system(clear_command)
			setup_compilation_options(compilation_options)
		elif choice == "0":
			# Exit the program
			print(f"{TerminalColors.OKCYAN}Exiting the program...{TerminalColors.ENDC}")
			exit(0)
		else:
			print(f"{TerminalColors.FAIL}Error> Invalid option!{TerminalColors.ENDC}", file=sys.stderr)
			continue

		input("\nPress Enter to continue...")
		os.system(clear_command)