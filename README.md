# Flask Server Test

Experimenting with using Flask as a back-end

Trying out [Flask](https://flask.palletsprojects.com) with HTMX and Sqlite as a simple back-end stack, with a view to using it in my classes (replacing PHP / MySQL). Using [Railway.app](https://railway.app/) for deployment.

## My Requirements

In order to replace the tech. stack I've used for years, I'll need...

- A simple way to serve up basic HTML pages
- A simple routing system
- A simple templating system for pages
- A simple component system for data-linked page components, etc.
- To be able to add simple SPA functionality using HTMX
- An easy-to-use relational DB

Ideally I'll be able to work with the students in VS Code (or possibly PyCharm)

## Setting up a Virtual Environment for Python

Create the virtual environment...

Windows:
```PowerShell
python -m venv venv
.\venv\Scripts\activate
pip install -r .\requirements.txt
```

Linux:
```Bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Launching the Server

If the 
```Bash
flask run
```

Or... Run via the IDE, checking that the IDE is using the virtual environment

