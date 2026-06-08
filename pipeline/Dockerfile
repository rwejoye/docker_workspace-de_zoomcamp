#start with slim python 3.13 (the image)
FROM python:3.13.13-slim 

#copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

#set working directory
WORKDIR /app 

#Add virtual environment to path so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH" 

#copy dependency files from lock file 
COPY "pyproject.toml" "uv.lock" ".python-version" ./

#Install dependencies from locked file (to ensure reproducibility)
RUN uv sync --locked 

#Copy application code 
COPY pipeline.py pipeline.py 

#Set entry point 
# ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
ENTRYPOINT ["python", "pipeline.py"]