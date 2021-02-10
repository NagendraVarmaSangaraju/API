from pydantic import BaseModel


class Dataset(BaseModel):
    id: int
    name: str
    description: str


class DatasetCreate(BaseModel):
    name: str
    description: str

class DatasetUpdate(BaseModel):
    id:int
    name: str
    description: str

    
class DatasetDelete(BaseModel):
    id:int
    # name: str
    # description: str


class User(BaseModel):
    id: int
    name: str
    surname: str




class UserCreate(BaseModel):
    name: str
    surname: str


class UserUpdate(BaseModel):
    id:int
    name: str
    surname: str

    
class UserDelete(BaseModel):
    id:int
    # name: str
    # description: str



class User2(BaseModel):
    id: int
    name: str
    surname: str
    dataset_id: int


class User2Create(BaseModel):
    name: str
    surname: str
    dataset_id: int

class User2Update(BaseModel):
    id:int
    name: str
    surname: str

    
class User2Delete(BaseModel):
    id:int
    # name: str
    # description: str

