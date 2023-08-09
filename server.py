from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator
import logging
import uuid
import sqlite3

app = FastAPI()

logging.basicConfig(level=logging.INFO)

DATABASE = "xapi_statements.db"

# Initialize SQLite database
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS statements (
        id TEXT PRIMARY KEY,
        actor TEXT,
        verb TEXT,
        object TEXT,
        result TEXT,
        context TEXT,
        timestamp TEXT
    )
''')
conn.commit()

class Actor(BaseModel):
    mbox: EmailStr
    name: str
    objectType: str
    
    @validator("mbox", pre=True)
    def validate_mbox(cls, mbox):
        if mbox.startswith("mailto:"):
            return mbox.split("mailto:")[1]
        raise ValueError("Invalid mbox format. It should start with 'mailto:'.")

class Verb(BaseModel):
    id: str
    display: dict

class Object(BaseModel):
    id: str
    definition: dict
    objectType: str

class XAPIStatement(BaseModel):
    actor: Actor
    verb: Verb
    object: Object
    result: dict = None
    context: dict = None
    timestamp: str = None
    id: uuid.UUID = uuid.uuid4()

@app.post("/xapi/statements/")
async def create_xapi_statement(statement: XAPIStatement):
    logging.info(f"Received xAPI statement: {statement.id}")
    if statement.actor.objectType != "Agent":
        raise HTTPException(status_code=400, detail="Invalid actor objectType")
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO statements (id, actor, verb, object, result, context, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(statement.id), str(statement.actor), str(statement.verb), str(statement.object), str(statement.result), str(statement.context), statement.timestamp))
    
    return statement

@app.get("/xapi/statements/")
async def get_xapi_statements():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM statements")
        rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
