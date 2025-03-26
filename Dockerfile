FROM condaforge/miniforge3


WORKDIR /django_app


COPY environment.yml .
RUN conda env create -f environment.yml && conda clean --all -y


ENV PATH /opt/conda/envs/django_env/bin:$PATH


COPY . .


ENV PYTHONUNBUFFERED=1


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
