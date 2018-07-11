"""Data module."""
import csv
import random
import logging
import pathlib 

from . import select_random_


ALLOWED_EXTENSIONS = set(".txt .csv".split())
WORKING_DIRPATH = pathlib.Path(__file__).parent


def load_songs_from_url(url=None, df=False):
    """Return dict rows or a DataFrame; load data from a url."""
    if url is None:
        config_filepath = WORKING_DIRPATH / "__config.json"
        url = select_random_.load_google_sheet_url(config_filepath)
    
    if not df:
        data = select_random_.read_google_sheets_to_dictrows(url)
    else:
        data = df = select_random_.read_google_sheets(url)
    return data


def write_temporary_files(url=None, df=True):
    """Write remote items to disk and shuffled items to disk."""
    songs = load_songs_from_url(url=url, df=df)
    IO().write_songs_to_file(songs)
    IO().write_shuffled_to_file(songs)


class IO:
    """A class to handle psuedo-database io."""
    
    def __init__(self):
        self._dirpath = pathlib.Path(__file__).absolute().parent
        self._filepath_songs = self._dirpath / "_db_songs.csv"
        self._filepath_shuffled = self._dirpath / "_db_shuffled.csv"
    
    def write_songs_to_file(self, songs):
        """Write items to a csv file."""
        self._write_csv(self._filepath_songs, songs)
        
    def write_shuffled_to_file(self, songs):
        """Write shuffled items to a csv file."""
        try:
            data = songs.sample(frac=1)
        except AttributeError:
            songs = list(songs)
            head, data = songs[0], songs[1:]
            random.shuffle(data)
        else:
            head = None
        self._write_csv(self._filepath_shuffled, data, header=head)
        
    def read_songs_from_file(self):
        """Read items from a csv file."""
        yield from self._read_csv(self._filepath_songs)

    def read_shuffled_from_file(self):
        """Read shuffled items from a csv file."""
        yield from self._read_csv(self._filepath_shuffled)
                
    def remove_from_shuffled_file(self):
        """Delete the first row from the file of shuffled items."""
        data = self.read_shuffled_from_file()
        header = next(data)
        next(data)
        tail = data
        self._write_csv(self._filepath_shuffled, tail, header=header)


    @staticmethod
    def _read_csv(filepath):
        """Read data from a csv."""
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                yield row

    @staticmethod
    def _write_csv(filepath, data, header=None):
        """Write data (DataFrame or plain text) to a csv file."""
        try:
            data.to_csv(filepath, index=False)
        except AttributeError:
            logging.info(" No DataFrame detected.  Writing file to csv ...")
            print(" INFO: No DataFrame detected.  Writing file to csv ...")
            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

    @staticmethod
    def _allowed_file(filename: pathlib.Path):
        """Return True if the file has the proper extension."""
        dot = "." in filename
        ext = filename.suffix in ALLOWED_EXTENSIONS
        return  dot and ext
