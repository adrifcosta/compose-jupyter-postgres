# Simple docker compose for DS

Welcome! This folder contains a Docker application with two services: postgres and jupyter notebook.

`notebooks/load_data.py` loads the csv file into postgres instance. 

`notebooks/Read Data.ipynb` reads the data from postgres and uses *pandas* to analyse the data.

Run `docker-compose up` to launch the app.