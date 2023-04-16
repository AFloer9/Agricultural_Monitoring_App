
from fastapi.testclient import TestClient
import pytest
from dbsetup import get_db, engine 
from main import app #import app object
#import pydanticmodels
from sqlalchemy import create_engine, insert, Table, Column
from sqlalchemy.orm import sessionmaker, declarative_base
import pydanticmodels
import sqlalchmodels
from faker import Faker, providers
import random

#fake test SQL database:
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(  #new database factory
    # allow multithread interactions for a single request:
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
fake = Faker() #fake object for testing

# make database session class:
TestSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

@pytest.fixture(scope="module") #fixture  destroyed at end of tests
def dbsession():
    #before tests run:
    sqlalchmodels.Base.metadata.drop_all(engine) #tears down table
    sqlalchmodels.Base.metadata.create_all(engine) #sets up fresh table
    
    testdb = TestSessionLocal()  #session to send queries to endpoints--created upon a request, closed out after 
    try:
        yield testdb    #return new sessiom
        print("connection to test DB succeeded")  #DEBUG
    finally:
        testdb.close() #close connection to database
    
    #populate DB:
    i = 1
    while i < 100:
        i += 1
        testseed = sqlalchmodels.Seed(
            id = fake.unique.random_int(1, 300),
            seed_type = fake.word(),
            coll_loc = fake.city(), 
            coll_date = fake.date(), 
            num_coll = fake.random_int(1, 200)
        )  
        testdb.add_all([testseed])
        testdb.commit() 
    # end while
           
@pytest.fixture(scope="module")  
def client(dbsession):
    def override_get_db():  # dependency override, for testing only
        try:
            yield dbsession #return fresh database session
        finally:
            dbsession.close()
    app.dependency_overrides[get_db] = override_get_db   
    yield TestClient(app)   # return fresh TestClient for testing

   
#unit for black-box testing = class Seed

#integration test units: seedvault database table/HTTP requests for class Seed--incremental

#white-box testing: all API requests/possible status codes returned for class Seed--full coverage

#HTTP request tests:

#acceptance test
#test request for web app home page
def test_get_main_page(client: TestClient):
    response = client.get("/")
    print(response.json().get('data'))
    assert response.status_code == 200
    assert response.json() == {"Welcome to ": "the Agricultural Monitoring Project"}
    
#acceptance test
#test request for user's entire seed db table
def test_get_all_seeds(client: TestClient):
    response = client.get("/seedvault/")
    print(response)
    assert response.status_code == 200
   
    
#acceptance test
#test request for user's entire seed db table
def test_get_seeds_table_empty(client: TestClient):  
    response = client.get("/seedvault/")
    assert response.status_code == 200 
    assert response.json() == {'data': []}
    
#acceptance test
#test request for a single seed type from user's seed db table    
def test_get_seed(client: TestClient):
    response = client.get("/seedvault/99")
    if response.status_code == 200: #if specific seed is found in database
        assert response.json() != {'id': []}    #make sure it gets returned
    else:
        assert response.json() == {'id': []}
    
#acceptance test
#test deletion of one seed type (row) in db table
def test_delete_seed(client: TestClient):
    response = client.delete("/seedvault/5")
    if response.status_code == 200: #if seed is found in database
        assert response.json == ["seed deleted"]    #notify of deletion
    else:                                                   #or
        assert response.status_code == 404          #return not found

#acceptance test
#test creation of one seed type (row) in db table
def test_create_seed(client: TestClient):
    response = client.post("/seedvault/", json={"id": 22, "seed_type": "tomato", "coll_loc": "field"})
    new_seed = pydanticmodels.CreateSeed(**response.json())
    assert response.status_code == 201 #created
    
#acceptance test
#test edit of one seed type (row) in db table
def test_edit_one_seed(client: TestClient):
    response = client.put("/seedvault/44", json={"id": 44, "seed_type": "sage", "coll_loc": "backyard"})
    #edited_seed = pydanticmodels.EditSeed(**response.json())
    if response.status_code == 200:
        assert response.json() != {'data': []}
    else:
        assert response.status_code == 404
    
#acceptance test
#test deletion of non-existent seed type (row) in db table    
def test_delete_seed_DNE(client: TestClient): 
    response = client.delete("/seedvault/400")  #test index beyond auto-pop range
    assert response.status_code == 404  #not found
    
#acceptance test
#test edit of non-existent seed type (row) in db table
def test_edit_seed_DNE(client: TestClient):   
    response = client.post("/seedvault/500") #test index beyond auto-pop range
    assert response.status_code == 405  #method not allowed 

#acceptance test
#test request to create seed with no name
def test_create_seed_type_null(client: TestClient):   
    response = client.post("/seedvault/", json={"id": 54, "coll_loc": "field"})
    #new_seed = pydanticmodels.CreateSeed(**response.json())
    assert response.status_code == 422 
    assert response.json() == {"Please provide a seed type"}

def test_get_seeds_same_coll_loc(client: TestClient):
    response = client.get("/seedvault/coll_loc=backyard")
    assert response.request.read
    
def test_get_seeds_same_type(client: TestClient):
    response = client.get("/seedvault/seed_type=tomato")    
    assert response.request.read
