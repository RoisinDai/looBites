# Loo-Bites

## Overview

Loo-Bites is a full-stack web application that provides a platform for Waterloo students to find nearby restaurants. This app will allow users to rate restaurants, search restaurants by name and by relevant meal type. 

[images of the project]

## Technologies used:

- HTML/CSS
- Javascript
- Python
- Flask
- MySQL

## Setup and Running

### Setup Virtual Env
#### Generate requirements.txt (Does not need to be set up again)
```
pip install pipreqs
pipreqs /path/to/project --force
```
#### To setup your virtualenv (Run it in the root folder of this project):
For MacOS and Linus:
```
# https://docs.python.org/3/library/venv.html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
\
For Windows:
```
# https://docs.python.org/3/library/venv.html
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### To deactivate your virtualenv:
```python
deactivate
```
#### To reactivate your virtualenv:
```python
source venv/bin/activate
```

### Connecting to MySQL
#### Making the Connection
(Optional) The virtual environment should have mysql-connector-python installed, but if not, install the library by:
```
pip install mysql-connector-python
python3 -m pip install mysql-connector
```
- Connection configuration is located in the `gcp_sql_config.py` file. More information can be found [HERE](https://towardsdatascience.com/sql-on-the-cloud-with-python-c08a30807661)

### Running Flask backend local server
Make sure you're in the `root directory` and run:
```
python run.py
```
The local host and port will show up in the terminal
 ```
 * Running on http://127.0.0.1:5000
 ````
 ### AWESOME pictures of the website
![Register](https://user-images.githubusercontent.com/125154836/225560324-386d34ef-52ed-4b21-b6e2-d6b7868dc825.PNG)
![Login](https://user-images.githubusercontent.com/125154836/225560434-deccfcc7-9600-42f1-9254-41b17c30958f.PNG)
![Add or Search Restaurants](https://user-images.githubusercontent.com/125154836/225560551-cce61080-5dae-4e4b-817c-2483f86916ff.PNG)
![Relevant Bites](https://user-images.githubusercontent.com/125154836/225560643-260c2ff3-945e-47a0-ac89-4a76ec51b21d.PNG)

