def endswith(suffix):
    """
    Create a function that checks if the argument
    that is passed in ends with string
    :param str suffix: string to check the end for
    :return func endswith_function: a function that checks if the
    argument ends with the specified string
    """
    def string_ends_with(string):
        return str.endswith(string, suffix)
    return string_ends_with


def startswith(prefix):
    """
    Create a function that checks if the argument
    that is passed in starts with string
    :param str prefix: string to check the start for
    :return func startswith_function: a function that checks if the
    argument starts with the specified string
    """
    def string_starts_with(string):
        return str.startswith(string, prefix)
    return string_starts_with
