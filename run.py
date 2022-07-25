from market import app
#because the market package has the __init__ file that runs initially, the variable 'app' is recognized.
#only recognizes from __init__.py, all packages have that __init__


#Checks if the run.py file has executed directly   and not imported
if __name__ == '__main__':
    app.run(debug=True)
