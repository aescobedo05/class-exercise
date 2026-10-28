#main.py

import io
import logging

from fastapi import File, HTTPException, UploadFile, FastAPI, Query
from pathlib import Path

import pandas as pd

from src import (
    DataStorage,
    MovieInput,
    MovieResponse,
    CSVInfo
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}

app = FastAPI(title="Movie API")

storage = DataStorage()

@app.get("/health")
def health_check():
    return {"status": "ok"}

#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}

#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record

@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    results = list(movies.values())[:limit]
    logger.info("Returning %s movie(s)", limit)
    return results


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    movie_id = len(movies) + 1

    record = movie.model_dump()
    record["id"] = movie_id

    movies[movie_id] = record

    logger.info("Added movie with ID %s", movie_id)

    return record


@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}



@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    contents = await file.read()

    data_dir = Path(file.filename)
    if data_dir.suffix != '.csv':
        logger.warning("Extension not .csv")
        raise HTTPException(status_code=400, detail="Extension not .csv")

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
        logger.warning("Cannot read CSV: %s", error)
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")

    dataset = storage.save_data(df, file.filename)
    logger.info("Stored dataset: id=%s, filename=%s", dataset, file.filename)


    return CSVInfo(
        filename=file.filename,
        rows=len(df),
        columns=len(df.columns),
        column_names=df.columns.tolist(),
        dataset_id=dataset
    )

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    dataset = storage.get_data(dataset_id)

    if dataset is None:
        logger.warning("Dataset not found: %s", dataset_id)
        raise HTTPException( status_code=404, detail="Dataset not found")

    logger.info("Dataset successfully retrieved: %s", dataset_id)

    return {"dataset_id": dataset_id, "rows": len(dataset), "columns": len(dataset.columns)}
