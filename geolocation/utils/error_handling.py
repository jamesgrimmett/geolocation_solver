class InsufficientDataError(Exception):
    def __init__(self, message="Insufficient data to proceed"):
        self.message = message
        super().__init__(self.message)

class UnknownCaseError(Exception):
    def __init__(self, message="Unknown problem setup"):
        self.message = message
        super().__init__(self.message)

class NotImplementedError(Exception):
    def __init__(self, message="Solution for this setup is not yet implemented"):
        self.message = message
        super().__init__(self.message)

class InvalidSolutionError(Exception):
    def __init__(self, message="The solution is not valid. Please check problem setup and raise an issue on the project github if necessary"):
        self.message = message
        super().__init__(self.message)
