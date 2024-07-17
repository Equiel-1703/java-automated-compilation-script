class CompilationError(Exception):
	"""Exception raised for errors during compilation.

	Attributes:
		message -- explanation of the error
	"""

	def __init__(self, message="Compilation failed"):
		self.message = message
		super().__init__(self.message)