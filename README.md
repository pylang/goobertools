## History

This project attempts to build a suite of simple web apps.  

1. `selector` randomly selects songs from a Google Sheet.


## HowTo Run

Simply run in any cmd or cmder:

    > start_flask


##### Details 

The following commands are maintained in a not version-controlled   batch file `start_flask.bat`.

[Set environments][cli] and run the following in commandline:

    > cd l/_projects/<app_folder>
    > source activate lab

In Windows (cmd)

    > set FLASK_APP=app.py
    > flask run

or Linux (bash)

    > exp*rt FLASK_APP=app.py
    > FLASK_APP=app.py flask run

Use [`debug` mode][debug] in a development env to avoid restarting the server:

    > set FLASK_ENV=development


## Selector

This app has a few main ideas:

1. loading the page (`GET`) auto retrives data from a default url. It then locally writes two files: songs and shuffled dataset
1. optionally select a data to override the default dataset (read a url or file)
1. pushing the button (`POST`) selects from the shuffled data and removes the selection.  This file rebuilds a shuffled dataset when it is depleted.  The refresh button also rebuilds the shuffled dataset. 


#### Data Options

The `selector` app can read data from Google Sheets (given a url) or from a selected file (`.txt` or `.csv`).  Google Sheets must be [published][publish] and the url to the `.csv` file must be used.  If neither option is provided, a default Sheets url is used, which is saved in a private config file.

NOTE: although modifications to Google Sheets are saved instantaneously, changes are delayed to the `Published` url.  Wait about 5 minutes to see resulting modifications in the app.  For improved lag, modify and upload a local file.

DEPRECATED: the uploading files data option proved overly complex.  If uploading a file is needed, upload to Google Docs and use the url data option.


#### Notes

- data is only read as DataFrames from Google sheets; it is thereafter written and read locally as `.csv` files (e.g. `db_*` files).
- `db_*` files are temporary, psuedo-"databases"; they are written to preserve persisted data between page loads and button presses.


## `_viz/`

Something that is lacking from many web app tutorials are pictures - visual results of code.  This folder captures the progress of this project.

---

## Changelog

- `pre`:   cli tool, read from text/csv files and Google Sheets
- `0.1.0`: structure, selector tool
- `0.2.0`: visual update, navbar, make file
- `0.2.1`: jquery, collapsible divs
- `0.2.2`: refactor/symlink `random_select_`, dynamic table, startup script, reload data via refresh, `models.py`
- `0.3.0`: read as DataFrames, local csv persistent files (deprecate global variables), refresh to reshuffle data
- `0.3.1`: data options (url), deprecate upload data option
- `1.0.0`: from `workflowtools`, add dynamic refresh button
- `1.0.1`: published on GitHub, new versioning

## References

- Adapted from [PyBites 100 Days of Code][pybites]
- Adapted from [CS50's Web Dev with Python Course][cs50.1], [site][cs50.2]
- Visually cleaned and extended from [Traversy Media tutorial][trav]
- Visuals built on [Bootstrap CDN][cdn] and [starter template][template]
- Basic tutorial by [w3schools.com][w3]
- Flask docs on [uploading][upload]
- Post on [Refresh Button][refresh]
- Docs on [favicons][fav]
- Tutorial on [deployment with pythonanywhere][deploy]


  [cli]:        http://flask.pocoo.org/docs/1.0/cli/
  [debug]:      http://flask.pocoo.org/docs/1.0/quickstart/#debug-mode
  [pybites]:    https://github.com/pybites/100DaysOfCode/tree/master/056
  [cs50.1]:     https://www.youtube.com/watch?v=Q0TBOlIn4z8
  [cs50.2]:     https://cs50.github.io/web/lectures
  [trav]:       https://www.youtube.com/watch?v=zRwy8gtgJ1A&t
  [cdn]:        https://www.bootstrapcdn.com/ 
  [template]:   https://getbootstrap.com/docs/4.1/examples/starter-template/
  [w3]:         https://www.w3schools.com/bootstrap/bootstrap_get_started.asp
  [publish]:    https://www.google.com/search?q=how%20to%20publish%20google%20sheets
  [upload]:     http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
  [refresh]: https://stackoverflow.com/questions/28762188/how-to-create-a-refresh-button-in-flask
  [fav]:        http://flask.pocoo.org/docs/1.0/patterns/favicon/
  [deploy]:    https://medium.com/@rudder_/launching-a-flask-app-from-scratch-on-pythonanywhere-fef871171e18