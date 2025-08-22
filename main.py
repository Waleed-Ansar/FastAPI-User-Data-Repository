from fastapi import FastAPI, HTTPException
from typing import List
from typing import Annotated
from pydantic import BaseModel, Field
import motor.motor_asyncio 

# || APP CREATION ||
app = FastAPI()
# || APP CREATION ||

# || DATABASE CONNECTION ||
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Waleed-Ansar:<password>@fastapi-cluster.0yfuiu4.mongodb.net/?retryWrites=true&w=majority&appName=FastAPI-Cluster")
db = client['User_Database']
Credentials = db['User_Data']
# || DATABASE CONNECTION ||

# || SCHEMA AND MODEL ||
PhoneNumber = Annotated[str, Field(pattern=r'^\+923\d{9}$')]
class Credential(BaseModel):
    id: int = Field(..., gt=0, description='User ID Must Be Unique!')
    name: str
    contact_no: PhoneNumber = Field(..., description="Phone number must start with +923 and contain 12 digits total")
    
    class config:
        populate_by_name = True

class Update_Credential(BaseModel):
    name: str
    contact_no: PhoneNumber = Field(..., description="Phone number must start with +923 and contain 12 digits total")
# || SCHEMA AND MODEL ||

# || MAIN CODE ||
@app.get("/", response_model=List[Credential])
async def display_all():
    users = Credentials.find({}, {"_id":0})
    creds = await users.to_list(length=None)
    return creds

@app.post("/add_user/", response_model=Credential)
async def add_user(user: Credential):
    existing = await Credentials.find_one({"id": user.id})
    if existing:
        raise HTTPException(status_code=404, detail='User ID already Exists.')
    await Credentials.insert_one(user.model_dump())
    return user

@app.get("/get_by_id/{user_id}", response_model=Credential)
async def get_user_by_id(user_id: int):
    user = await Credentials.find_one({"id": user_id})
    if user:
        return user
    raise HTTPException(status_code=404, detail='User not Found.')

@app.put("/modify_creds/", response_model=Credential)
async def modify_user_credentials(user_id: int, creds: Update_Credential):
    updated = await Credentials.find_one_and_update({"id": user_id}, {"$set": dict(creds)})
    if updated:
        return updated
    raise HTTPException(status_code=404, detail='User not Found.')

@app.delete("/delete_user/{user_id}" ,response_model=Credential)
async def  delete_user(user_id: int):
    deleted = await Credentials.find_one_and_delete({"id": user_id})
    if deleted:
        return deleted
    raise HTTPException(status_code=404, detail='ID not Found.')
# || MAIN CODE ||


# uvicorn main:app --reload
