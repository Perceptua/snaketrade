"""Helper classes for snaketrade."""
from datetime import datetime, timedelta, timezone
import json
import pandas as pd


class SnakeTradeUtils:
    """Utility functions for snaketrade."""

    def parse_response_json(response):
        """
        Deserialize response JSON into dictionary.

        Requires a response with status code 200. If status code is not
        200, ValueError is raised.

        Parameters
        ----------
        response : requests.Response
            An HTTP response object.

        Raises
        ------
        ValueError
            If response status code is not 200, raise ValueError.

        Returns
        -------
        data : dict or list
            Parsed response JSON.

        """
        data = {}

        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            error_message = f'{response.status_code}: {response.reason}'
            raise ValueError(error_message)

        return data

    def dict_to_dataframe(data, flatten=True):
        """
        Parse dictionary data into a single-row dataframe.

        If the optional flatten parameter is set to true, nested dictionaries
        will be parsed & resulting dataframes will be concatenated with parent
        dictionaries along axis 1 (columns). Note that values of type list will
        not be parsed.

        Parameters
        ----------
        data : dict
            Dictionary to be parsed into dataframe.
        flatten : bool, optional
            If true, parse nested dictionaries & concatenate resulting
            dataframes to the parent dictionary along axis 1 (columns).
            The default is True.

        Returns
        -------
        dataframe : pandas.DataFrame
            Single-row dataframe of dictionary data.

        """
        formatted = {}
        subframes = []

        for key, value in data.items():
            if flatten and type(value) == dict:
                subframes += [
                    SnakeTradeUtils.dict_to_dataframe(value, flatten)
                ]
            else:
                formatted[key] = [value]

        subframes += [pd.DataFrame(data=formatted)]
        dataframe = pd.concat(subframes, axis=1)

        return dataframe

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
            datetime.strptime(date_string, format_string)
            matches_format = True
        except Exception as error:
            if raise_error:
                raise error

        return matches_format

    def utc_from_milliseconds(milliseconds):
        """
        Convert milliseconds since epoch to datetime object with UTC timezone.

        Parameters
        ----------
        milliseconds : str or int
            Milliseconds since epoch (1970-01-01 00:00:000.000).

        Returns
        -------
        utc_timestamp : datetime.datetime
            Datetime object representing seconds from epoch in UTC timezone.

        """
        milliseconds = int(milliseconds)

        utc_timestamp = datetime(
            year=1970, month=1, day=1, tzinfo=timezone.utc
        ) + timedelta(
            milliseconds=milliseconds
        )

        return utc_timestamp
