from typing import List

from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from backend.db import get_database
from backend.models import users2_table, datasets_table
from backend.schemas import User2, User2Create, User2Update, User2Delete

users2_router = APIRouter()


@users2_router.get("/users2", response_model=List[User2])
async def read_users2(database: Database = Depends(get_database)):
    query = users2_table.select()
    results = await database.fetch_all(query)
    return results

@users2_router.get("/users2/{user_id}", response_model=List[User2])
async def get_users2(user_id: int, database: Database = Depends(get_database)):
    query = users2_table.select().\
        where (users2_table.c.id == user_id)
    results = await database.fetch_all(query)
    return results


@users2_router.post("/users2", response_model=List[User2])
async def add_user2(
    user2: User2Create, database: Database = Depends(get_database)
    ):
    id = user2.dict().get("dataset_id")
    query = datasets_table.select().\
        where (datasets_table.c.id == user2.dict().get("dataset_id"))
    results = await database.fetch_all(query)
    if user2.dict().get("dataset_id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Dataset Not Found", headers={"X-Error": "DataSet ID not found in DB"},)
        return results

    name = user2.dict().get("name")
    query = users2_table.select().\
        where (users2_table.c.name == user2.dict().get("name"))
    results = await database.fetch_all(query)
    if name in [item[1] for item in results]:
        raise HTTPException(status_code=400, detail="Duplicate Entry", headers={"X-Error": "The Name already exists in DB"},)
        return results
    else:
        insert_query = users2_table.insert().values(**user2.dict())
        last_record_id = await database.execute(insert_query)
        select_query = users2_table.select().where(text("id = {}".format(last_record_id)))
        results = await database.fetch_all(select_query)
        return results


@users2_router.put("/users2", response_model=List[User2])
async def update_user(
    user2: User2Update, database: Database = Depends(get_database)
):
    name = user2.dict().get("name")
    query = users2_table.select().\
        where (users2_table.c.name == user2.dict().get("name"))
    results = await database.fetch_all(query)
    if name in [item[1] for item in results]:
        raise HTTPException(status_code=400, detail="Duplicate Entry", headers={"X-Error": "The Name already exists in DB"},)
        return results

    query = users2_table.select().\
        where (users2_table.c.id == user2.dict().get("id"))
    results = await database.fetch_all(query)
    if user2.dict().get("id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Not Found", headers={"X-Error": "ID not found in DB"},)
        return results
    else:
        update_query = users2_table.update().\
            where(users2_table.c.id == user.dict().get("id")).\
            values(
            name = user2.dict().get("name"),
            surname = user2.dict().get("surname")
        )
        last_record_id = await database.execute(update_query)
        update_query = users2_table.select().where(text("id = id".format(last_record_id)))
        results = await database.fetch_all(update_query)
        return results

@users2_router.delete("/users2")
async def delete_user2(
    user2: User2Delete, database: Database = Depends(get_database)
):

    query = users2_table.select().\
        where (users2_table.c.id == user2.dict().get("id"))
    results = await database.fetch_all(query)
    if user2.dict().get("id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Not Found", headers={"X-Error": "ID not found in DB"},)
        return results
    delete_query = users2_table.delete().\
        where (users2_table.c.id == user2.dict().get("id"))
    results = await database.execute(delete_query)
    return results
    # return {
    #     "status" : True,
    #     "message": "Successfully deleted"
    # }
