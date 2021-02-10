from typing import List

from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from backend.db import get_database
from backend.models import users_table
from backend.schemas import User, UserCreate, UserUpdate, UserDelete

users_router = APIRouter()

#getting all entries in dataset
@users_router.get("/users", response_model=List[User])
async def read_users(database: Database = Depends(get_database)):
    query = users_table.select()
    results = await database.fetch_all(query)
    return results
#getting user related to specific ID
@users_router.get("/users/{user_id}", response_model=List[User])
async def get_users(user_id: int, database: Database = Depends(get_database)):
    query = users_table.select().\
        where (users_table.c.id == user_id)
    results = await database.fetch_all(query)
    return results


@users_router.post("/users", response_model=List[User])
async def add_user(
    user: UserCreate, database: Database = Depends(get_database)
    ):
    #checking if the name already exists in DB
    name = user.dict().get("name")
    query = users_table.select().\
        where (users_table.c.name == user.dict().get("name"))
    results = await database.fetch_all(query)
    #if the name exists throw error (Duplicates not allowed)
    if name in [item[1] for item in results]:
        raise HTTPException(status_code=400, detail="Duplicate Entry", headers={"X-Error": "The Name already exists in DB"},)
        return results
    else:
        insert_query = users_table.insert().values(**user.dict())
        last_record_id = await database.execute(insert_query)
        select_query = users_table.select().where(text("id = {}".format(last_record_id)))
        results = await database.fetch_all(select_query)
        return results

#Updating the entry
@users_router.put("/users", response_model=List[User])
async def update_user(
    user: UserUpdate, database: Database = Depends(get_database)
):
#if the name exists throw error (Duplicates not allowed)
    name = user.dict().get("name")
    query = users_table.select().\
        where (users_table.c.name == user.dict().get("name"))
    results = await database.fetch_all(query)
    if name in [item[1] for item in results]:
        raise HTTPException(status_code=400, detail="Duplicate Entry", headers={"X-Error": "The Name already exists in DB"},)
        return results
#Checking for ID. If ID not exists in DB then throw error
    query = users_table.select().\
        where (users_table.c.id == user.dict().get("id"))
    results = await database.fetch_all(query)
    if user.dict().get("id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Not Found", headers={"X-Error": "ID not found in DB"},)
        return results
    else:
        update_query = users_table.update().\
            where(users_table.c.id == user.dict().get("id")).\
            values(
            name = user.dict().get("name"),
            surname = user.dict().get("surname")
        )
        last_record_id = await database.execute(update_query)
        update_query = users_table.select().where(text("id = id".format(last_record_id)))
        results = await database.fetch_all(update_query)
        return results
#deleting user
@users_router.delete("/users")
async def delete_user(
    user: UserDelete, database: Database = Depends(get_database)
):

    query = users_table.select().\
        where (users_table.c.id == user.dict().get("id"))
    results = await database.fetch_all(query)
    if user.dict().get("id") not in [item[0] for item in results]:
        raise HTTPException(status_code=404, detail="Not Found", headers={"X-Error": "ID not found in DB"},)
        return results
    delete_query = users_table.delete().\
        where (users_table.c.id == user.dict().get("id"))
    results = await database.execute(delete_query)
    return results
    # return {
    #     "status" : True,
    #     "message": "Successfully deleted"
    # }
