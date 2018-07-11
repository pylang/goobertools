#!python3
import random
import logging
import pathlib

from flask import Flask, render_template, request

from . import models
from . import select_random_


app = Flask(__name__)

mio = models.IO()


@app.route("/", methods=["GET", "POST"])
def selector():
    result = None
    if request.method == "GET":                            # refresh page
        # Default data
        models.write_temporary_files()

    if request.method == "POST":                           # press button
        # Load data
        input_url = request.form["input_url"]

        if input_url:
            models.write_temporary_files(url=input_url)
        
        # Select random item
        data = mio.read_shuffled_from_file()
        header = next(data)
        try:
            song = next(data)
            #print(song)
        except StopIteration:
            app.logger.info(" End of songs.  Restarting...")
            print(" End of songs.  Restarting...")
            songs = mio.read_songs_from_file()
            mio.write_shuffled_to_file(songs)              # reset shuffled file
            result = "done"
        else:
            mio.remove_from_shuffled_file()
            result = dict(zip(header, song))
            #print(result)
    return render_template("selector.html", result=result)


if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True                                 # keep from restarting the server
    app.jinja_env.auto_reload = True
    app.run()