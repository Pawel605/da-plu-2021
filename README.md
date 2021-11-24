## Purpose
The project was created and developed during the [Python Level Up Spring 2021 course](https://github.com/daftcode/daftacademy-python_levelup-spring2021).

It is a simple application that uses FastAPI and REST API with data from Northwind database.
## Deployment
The application is available on [Heroku](https://da-plu-2021-pf.herokuapp.com/).

API docs:

https://da-plu-2021-pf.herokuapp.com/docs

## Run app
### Installing Dependency
Here gives an example of configuring a conda virtual environment using [Anaconda](https://www.anaconda.com/). 
When creating the virtual environment, make sure the default python of the virtual environment is python 3.8

* Download Anaconda ([official site](https://www.anaconda.com/distribution/#download-section)) and install.

Then:
```bash
conda create --name env_example python=3.8
conda activate env_example
git clone https://github.com/Pawel605/da-plu-2021.git
cd da-plu-2021
pip install -r requirements.txt
```

* Finally, run application with Uvicorn:

`uvicorn views.main:app`

* or auto-reload:

`uvicorn views.main:app --reload`

## Used technologies
* Python 3.8
* FastAPI 
* pytest
* uvicorn
* PostgreSQL database 
* SLQAlchemy ORM
* docker-compose