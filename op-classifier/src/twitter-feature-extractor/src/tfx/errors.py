class ExtractionError(Exception):
    pass


class ConfFileError(ExtractionError):
    pass


# Come up with some meaningful error names (try to group them)
class MissingDataError(ExtractionError):
    pass


class InvalidDataError(ExtractionError):
    pass


class FileExistsError(ExtractionError):
    pass


class ResultFileError(ExtractionError):
    pass


# Things that are not actually "errors", just exceptions that are caught
class UserNotNeeded(Exception):
    def __init__(self, user_id, label):
        self.user_id = user_id
        self.label = label
