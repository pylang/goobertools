"""Build test csv."""
import io
import pathlib

import nose.tools as nt


def get_buffer_txt():
    """Return a text buffer."""
    text = io.StringIO(
        "1. item1\n"
        "- item2\n"
        " item3\n"
    )
    return text


def get_buffer_csv():
    """Return a csv buffer."""
    csv = io.StringIO(
        ",col1,col2,col3\n"
        "A,a,x,1\n"
        "B,b,y,2\n"
        "C,c,z,3\n"
    )
    return csv


def get_buffer_google_sheet():
    """Return a sheet buffer."""
    google_sheet = io.StringIO(
        ",col1,col2,col3\n"
        "A,a,x,1\n"
        "B,b,y,2\n"
        "C,c,z,3\n"
    )
    return google_sheet