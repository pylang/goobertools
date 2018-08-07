"""Tests for validating links."""

import os
import urllib
import pathlib
import functools as ft
import collections as ct

import pandas as pd
import nose.tools as nt
from testfixtures import TempDirectory

from ..utils import tools as ut
from ..utils import select_random as sr
from .test_fixtures import test_fixture_select_random as fixture


def test_to_str_dictvalues():
    """Verify a dict of values is joins values as comma-delimited strings."""
    gen = sr.to_str_dictvalues
    data = [dict(x="a", y="b", z="c"), dict(x="1", y="2", z="3")]
    nt.eq_(list(gen(data)), ["a, b, c", "1, 2, 3"])


class TestShufflePicks:
    """A suite of tests for shuffle_picks."""

    def __init__(self):
        self.data = "a b c x y z".split()
        self.picks = sr.shuffle_picks(iter(self.data), seed=123)

    def test_shuffle_picks_item(self):
        """Verify PickResult items."""
        actual = [p.item for p in self.picks]
        expected = "x y b z c a".split()
        nt.eq_(actual, expected)

    def test_shuffle_picks_total(self):
        """Verify PickResult total."""
        actual = [p.total for p in self.picks]
        expected = [len(self.data)] * len(self.data)
        nt.eq_(actual, expected)

    def test_shuffle_picks_remaining(self):
        """Verify PickResult remaining."""
        actual = [p.remaining for p in self.picks]
        expected = list(reversed(range(1, 7)))
        nt.eq_(actual, expected)


# Requires mock url to a Google Sheets or mock csv
def test_read_google_sheets():
    """Verify reading sheets-like data."""
    d = {
        "": "A B C".split(),
        "col1": "a b c".split(),
        "col2": "x y z".split(),
        "col3": "1 2 3".split(),
        # "col3": [1, 2, 3],
    }
    resource = fixture.get_buffer_google_sheet()
    expected = pd.DataFrame(d)
    actual = sr.read_google_sheets(resource)
    ut.assertFrameEqual(expected, actual)


def test_read_google_sheets_to_dictrows():
    """Verify a dictrow is next yielded."""
    resource = fixture.get_buffer_google_sheet()
    result = sr.read_google_sheets_to_dictrows(resource)
    expected = {"": "A", "col1": "a", "col2": "x", "col3": "1"}
    actual = next(result)    
    nt.eq_(expected, actual)


def test_get_data_values_w_pandas():
    """Verify head-less str row is returned via pandas."""
    resource = fixture.get_buffer_google_sheet()
    result = sr.get_data_values_w_pandas(resource)
    expected = "A, a, x, 1"
    actual = next(result)
    nt.eq_(expected, actual)
    

def test_get_data_values_w_pandas_csv():
    """Verify fallback to get data pandas from a csv."""
    resource = fixture.get_buffer_csv()
    result = sr.get_data_values_w_pandas(resource)
    expected = "A, a, x, 1"
    actual = next(result)
    nt.eq_(expected, actual)


def test_get_data_values_no_pandas_csv():
    """Verify get data from a .csv file without pandas."""
    with TempDirectory() as d:
        expected = "A, a, x, 1"
        filename = "test.csv"
        filepath = pathlib.Path(d.path) / filename
        csv_content = fixture.get_buffer_csv()
        csv_content_bytes = csv_content.getvalue().encode()
        d.write(filename, csv_content_bytes)
        actual = list(sr.get_data_values_no_pandas(filepath))[0]
        nt.eq_(expected, actual)


def test_get_data_values_no_pandas_txt():
    """Verify get data from a .txt file without pandas."""
    with TempDirectory() as d:
        expected = "item1"
        filename = "test.txt"
        filepath = pathlib.Path(d.path) / filename
        content = fixture.get_buffer_txt()
        content_bytes = content.getvalue().encode()
        d.write(filename, content_bytes)
        actual = list(sr.get_data_values_no_pandas(filepath))[0]
        nt.eq_(expected, actual)


# FIX: test is long ---------------------------------------
def test_read_txt():
    """Verify text file context is equal."""
    with TempDirectory() as d:
        expected = [
            "item1",
            "item2",
            "item3",
        ]

        filename = "test.txt"
        filepath = pathlib.Path(d.path) / filename
        content = fixture.get_buffer_txt()
        content_bytes = content.getvalue().encode()
        d.write(filename, content_bytes)
        actual = list(sr.read_txt(filepath))
        nt.eq_(expected, actual)


def test_read_csv():
    """Verify reading a csv file."""
    with TempDirectory() as d:
        expected = [
            {"": "A", "col1": "a", "col2": "x", "col3": "1"},
            {"": "B", "col1": "b", "col2": "y", "col3": "2"},
            {"": "C", "col1": "c", "col2": "z", "col3": "3"},
        ]

        filename = "test.csv"
        filepath = pathlib.Path(d.path) / filename
        content = fixture.get_buffer_csv()
        content_bytes = content.getvalue().encode()
        d.write(filename, content_bytes)
        actual = list(sr.read_csv(filepath))
        nt.eq_(expected, actual)


@nt.raises(FileNotFoundError)
def test_load_google_sheet_url():
    """Verify error is raised for filepath."""
    fpath = pathlib.Path("./bad_filepath/foo.py")
    result = sr.load_google_sheet_url(fpath)
    next(result)


@nt.raises(urllib.error.URLError)
def test_read_google_sheets_to_dictrows_error():
    """Verify an error is raised from a bad url."""
    result = sr.read_google_sheets_to_dictrows("https://bad_url.com")
    next(result)


@nt.raises(TypeError)
def test_get_data_values_no_pandas_error_type():
    """Verify raise error if resource is not a filepath."""
    resource = None
    result = sr.get_data_values_no_pandas(resource)
    next(result)


@nt.raises(TypeError)
def test_get_data_values_no_pandas_error_ext():
    """Verify raise error if resource is not a .txt or .csv file."""
    resource = pathlib.Path("foo.bar")
    result = sr.get_data_values_no_pandas(resource)
    next(result)
