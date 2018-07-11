:: set environment varibles (app and debug mode)
echo "Reminder: activate a virtural environment"
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
pause