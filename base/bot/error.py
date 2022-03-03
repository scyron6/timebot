class InvalidFilesError(Exception):
    """Error with input or output files"""
    def __init__(self, message="Error with input or output files"):
        self.message = message
        super().__init__(self.message)