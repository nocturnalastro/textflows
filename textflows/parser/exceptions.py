class InvalidEntrypoint(Exception):
    pass


class MissingConditions(Exception):
    @classmethod
    def __iter__(cls):
        raise cls("Conditions are missing")

    @classmethod
    def __next__(cls):
        raise cls("Conditions are missing")


class MissingSubflows(Exception):
    @classmethod
    def __iter__(cls):
        raise cls("Subflows are missing")

    @classmethod
    def __next__(cls):
        raise cls("Subflows are missing")


class ParseFailed(Exception):
    pass
