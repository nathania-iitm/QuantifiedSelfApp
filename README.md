# Local Setup
- Clone the project
- Run `pip install -r requirements.txt` to install all dependencies

# Local Development Run
- `python3 app.py` It will start the flask app in `development`. Suited for local development. 

# Replit run
- Go to shell and run `python3 app.py`
- The web app will be availabe at https://final-project.nathania-fernandes.repl.co/

# Folder Structure
- `tracker.sqlite3` is the sqlite database
- `static` - default `static` files folder. It serves at '/static' path.
- `templates` - Default flask templates folder containing html files


```
Final Project/
├── app.py
├── tracker.sqlite3
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── static/
│   ├── myplot.png
│   └── style.css
├── templates/
│   ├── addlog.html
│   ├── create.html
│   ├── dash.html
│   ├── edit_l.html
│   ├── edit_t.html
│   ├── home.html
│   └──viewlog.html
└── 
```