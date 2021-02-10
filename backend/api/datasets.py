from typing import List

from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from backend.db import get_database
from backend.models import datasets_table
from backend.schemas import Dataset, DatasetCreate, DatasetUpdate, DatasetDelete

datasets_router = APIRouter()

#getting all entries in dataset
@datasets_router.get("/datasets", response_model=List[Dataset])
async def read_datasets(database: Database = Depends(get_database)):
    query = datasets_table.select()
    results = await database.fetch_all(query)
    return results

#getting dataset related to specific ID
@datasets_router.get("/datasets/{dataset_id}", response_model=List[Dataset])
async def get_datasets(dataset_id: int, database: Database = Depends(get_database)):
    query = datasets_table.select().\
        where (datasets_table.c.id == dataset_id)
    results = await database.fetch_all(query)
    return results


@datasets_router.post("/datasets", response_model=List[Dataset])
async def add_dataset(
    dataset: DatasetCreate, database: Database = Depends(get_database)
):
    #checking if the name already exists in DB
    name = dataset.dict().get("name")
    query = datasets_table.select().\
        where (datasets_table.c.name == dataset.dict().get("name"))
    results = await database.fetch_all(query)
    #if the name exists throw error (Duplicates not allowed)
    if name in [item[1] for item in results]:
        raise HTTPException(status_code=400, detail="Duplicate Entry", headers={"X-Error": "The Name already exists in DB"},)
        return results
    else:
        insert_query = datasets_table.insert().values(**dataset.dict())
        last_record_id = await database.execute(insert_query)
        select_query = datasets_table.select().where(text("id = {}".format(last_record_id)))
        results = await database.fetch_all(select_query)
        return results

#Updating the entry
@datasets_router.put("/datasets", response_model=List[Dataset])
async def update_dataset(
    dataset: DatasetUpdate, database: Database = Depends(get_database)
):
#if the name exists throw error (Duplicates not allowed)
    name = dataset.dict().get("name")
    query = datasets_table.select().\
        where (datasets_table.c.name == dataset.dict().get("name"))
    results = await database.fetch_all(query)
    if name in [item[1] for item in results]:
        raise HTTPException(status_code=400, detail="Duplicate Entry", headers={"X-Error": "The Name already exists in DB"},)
        return results
#Checking for ID. If ID not exists in DB then throw error
    query = datasets_table.select().\
        where (datasets_table.c.id == dataset.dict().get("id"))
    results = await database.fetch_all(query)
    if dataset.dict().get("id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Not Found", headers={"X-Error": "ID not found in DB"},)
        return results
    else:
        update_query = datasets_table.update().\
            where(datasets_table.c.id == dataset.dict().get("id")).\
            values(
            name = dataset.dict().get("name"),
            description = dataset.dict().get("description")
        )
        last_record_id = await database.execute(update_query)
        update_query = datasets_table.select().where(text("id = id".format(last_record_id)))
        results = await database.fetch_all(update_query)
        return results
#deleting dataset
@datasets_router.delete("/datasets")
async def delete_dataset(
    dataset: DatasetDelete, database: Database = Depends(get_database)
):

    query = datasets_table.select().\
        where (datasets_table.c.id == dataset.dict().get("id"))
    results = await database.fetch_all(query)
    if dataset.dict().get("id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Not Found", headers={"X-Error": "ID not found in DB"},)
        return results
    delete_query = datasets_table.delete().\
        where (datasets_table.c.id == dataset.dict().get("id"))
    results = await database.execute(delete_query)
    return results
    # return {
    #     "status" : True,
    #     "message": "Successfully deleted"
    # }