# Data Modeling with Postgres
### Udacity - Data Engineering with Azure - Project 1

This project demonstrates an ETL pipeline which transforms extracted JSON files from a third party application (An imaginary music streaming service Sparklify) and loads them to a Postgres database. Song metadata and log data of song plays are ingested into a star schema which consists of songplays (fact table) and songs, users, artists, time (dimension tables).

Upsert operations have been defined for the following tables in favor of keeping new entries; *users*, *songs*, and *artists*. In the event of conflicting primary keys, the features will replace the existing ones, however conflicts in the foreign key fields will throw an error. As a potential improvement of the project, these operations could be tracked using a trigger to a history table. Meanwhile, upsert operations are defined for *time* table in favor of existing entries, using the command "DO NOTHING". There is no need to update datetime-related fields in the event of receiving a duplicate timestamp, as these properties are quite material.


## Files
- **run_db.sh**: A shell script containing the code for creating a Docker container for the database and a remove script if the container with the same name already exists.
- **requirements.txt**: Required python packages for the project.
- **sql_queries.py**: Helper SQL queries which are referred in other scripts, create_tables.py and etl.py.
- **create_tables.py**: Defines the procedure to create a database and create tables with the correct field types and constraints
- **etl.py**: The main script of the project. Defines the ETL procedure.
- **etl.ipynb**: Jupyter Notebook explaining all the processes step by step and also running requirements.txt, run_db.sh, create_tables.py, and etl.py
- **etl.ipynb**: Jupyter Notebook containing the results of sanity checks after the ETL pipeline is run.


## How to Run
You can easily run the program with all the explanations using etl.ipynb.

For standalone processing, please use the code snippet below to install requirements to your virtual environment, initialize the Docker container for the database, create tables and schema, and run the etl.py script.

```
pip install -r requirements.txt
bash run_db.sh
python create_tables.py
python etl.py
```
