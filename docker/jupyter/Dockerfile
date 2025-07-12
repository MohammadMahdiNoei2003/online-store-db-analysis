FROM jupyter/scipy-notebook

# Optional: install PostgreSQL client tools
USER root
RUN apt-get update && apt-get install -y libpq-dev

# Switch to default user and install python packages
USER jovyan
RUN pip install psycopg2-binary sqlalchemy plotly seaborn
