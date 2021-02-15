class Reporter(object):
    """
    Super class of all reporters in ApprovalTests.Python

    The only necessary function to implement for a
    reporter is 'report', which takes the absolute
    paths of the received- and approved files, and
    returns a truthy value on success.
    """

    def report(self, received_path, approved_path):
        """
        Apply the reporter to pair of files given
        as absolute paths parameters.

        A truthy return value from report means that it succeeded,
        such as because any command existed.

        A falsy return value from report means that its operation
        failed in some way.

        Note: At the time of writing, not all implementations of
        Reporter return this value correctly.
        """
        raise Exception("Interface member not implemented")
