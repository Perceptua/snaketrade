"""Helper classes for snaketrade."""
from datetime import datetime as dt


class SnakeTradeUtils:
    """Utility functions for snaketrade."""

    def check_date_format(date_string, format_string, raise_error=True):
        """
        Verify date string matches specified format.

        Parameters
        ----------
        date_string : str
            Date string to check.
        format_string : str
            Expected format of date string.
        raise_error : bool, optional
            If True, raise any errors encountered during execution. The default
            is True.

        Raises
        ------
        error
            Any error encountered during execution.

        Returns
        -------
        matches_format : bool
            True if date string matches expected format. If date string does
            not match expected format & raise_error is False, returns False.

        """
        matches_format = False

        try:
            dt.strptime(date_string, format_string)
            matches_format = True
        except Exception as error:
            if raise_error:
                raise error

        return matches_format
