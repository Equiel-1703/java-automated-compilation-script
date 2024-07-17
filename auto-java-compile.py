import os
import sys
import subprocess

from exceptions import *
from compilation_options import CompilationOptions
from terminal_colors import TerminalColors

def show_menu(src_folder) -> str:
	"""
	Shows a menu with the available options to the user and the path of the informed source folder.

	Args:
		src_folder (str): The absolute path of the source folder.
	
	Returns:
		str: The user's choice.
	"""
	print(f"{TerminalColors.HEADER} - Automated Java Compilation Script by Equiel_1703 - {TerminalColors.ENDC}")
	print()
	print(f"{TerminalColors.OKBLUE}Source Folder (absolute path): {src_folder}{TerminalColors.ENDC}")
	print()
	print("Choose an option:")
	print("1. Compile all Java files in the source folder")
	print("2. Compile specific Java files in the source folder")
	print("3. Clear build")
	print("4. Compile and run a specific Java file")
	print("5. Compile and run the entire program")
	print("6. Setup compilation options")
	print("0. Exit")

	choice = input().strip()
	return choice

def posorder_traversal(folder, condition) -> list[str]:
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
			list_of_files.extend(posorder_traversal(file, condition))
		elif condition(file):
			# If "file" is a file, we must add it to the list - only if it satisfies the condition
			list_of_files.append(file)
	
	# Return the list of files
	return list_of_files

def compile_file(path_to_file: str, compilation_options: CompilationOptions) -> None:
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

def compile_all_files(compilation_options: CompilationOptions) -> None:
	"""
	Compiles all Java files in the source folder.

	Args:
		compilation_options (CompilationOptions): The compilation options to use when compiling the files.
	"""
	# Get the list of files that will be compiled
	files_to_compile = posorder_traversal(compilation_options.src_folder, lambda file: file.endswith(".java"))

	# Print the list of files
	print("Files to compile:")
	for file in files_to_compile:
		print("+ " + file)

	try:
		# Now we can compile the files in the list
		for file in files_to_compile:
			print(f"\n{TerminalColors.OKCYAN}Compiling file: {file}{TerminalColors.ENDC}")
			compile_file(file, compilation_options)
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
	files_available = posorder_traversal(compilation_options.src_folder, lambda file: file.endswith(".java"))

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
			compile_file(file, compilation_options)
	except CompilationError:
		print(f"\n{TerminalColors.FAIL}Error> Could not compile all files!{TerminalColors.ENDC}", file=sys.stderr)
		return
	
	print(f"\n{TerminalColors.OKGREEN}Compilation finished!{TerminalColors.ENDC}")
	print(f"Total of {len(files_to_compile)} files compiled.")

def clear_build(src_folder) -> None:
	"""
	Removes all .class files from the source folder.

	Args:
		src_folder (str): The absolute path of the source folder.
	"""
	files_to_delete = posorder_traversal(src_folder, lambda file: file.endswith(".class"))

	# Print to the user
	print(f"{TerminalColors.OKCYAN}Cleaning build...{TerminalColors.ENDC}")
	print()

	for file in files_to_delete:
		os.remove(file)
		print(f"{TerminalColors.WARNING}Deleted: {file}{TerminalColors.ENDC}")
	
	print(f"\n{TerminalColors.OKGREEN}Build cleaned!{TerminalColors.ENDC}")

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

	# Check if the user provided too many arguments
	if len(sys.argv) > 3:
		print(f"{TerminalColors.FAIL}Error> Too many arguments provided!{TerminalColors.ENDC}", file=sys.stderr)
		print(f"Usage: python {sys.argv[0]} [source_folder] [class_path]", file=sys.stderr)
		exit(1)

	if len(sys.argv) == 1:
		# If no arguments were provided, we must ask the user for the source folder
		src_folder = input("Folder containing the source code: ").strip()
	elif len(sys.argv) == 2:
		# If the user provided a single argument, we must use it as the source folder
		src_folder = sys.argv[1]

	if len(sys.argv) == 3:
		# If the user provided a class path (two arguments), we must use it as the class path
		class_path = sys.argv[2]
		compilation_options = CompilationOptions(src_folder, class_path)
	else:
		# Create Compiler Options object without class path
		compilation_options = CompilationOptions(src_folder)

	# Program loop
	while True:
		choice = show_menu(src_folder)

		if choice == "1":
			# Compile all Java files in the source folder
			os.system(clear_command)
			compile_all_files(src_folder)
		elif choice == "2":
			# Compile specific Java files in the source folder
			os.system(clear_command)
			compile_specific_files(src_folder)
		elif choice == "3":
			# Clear build
			os.system(clear_command)
			clear_build(src_folder)
		elif choice == "0":
			# Exit the program
			print(f"{TerminalColors.OKCYAN}Exiting the program...{TerminalColors.ENDC}")
			exit(0)
		else:
			print(f"{TerminalColors.FAIL}Error> Invalid option!{TerminalColors.ENDC}", file=sys.stderr)
			continue

		input("\nPress Enter to continue...")
		os.system(clear_command)