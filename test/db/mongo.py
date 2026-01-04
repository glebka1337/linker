import pytest_asyncio
from src.models.note import Note
from beanie import init_beanie
from docker.models.containers import Container
from motor.motor_asyncio import AsyncIOMotorClient
@pytest_asyncio.fixture
async def mongo_client(
    mongo_container
):
    client = AsyncIOMotorClient(
       'mongodb://test:test@localhost:27018/test?authSource=admin'
    )
    try:
        yield client
    finally:
        client.close()
        
@pytest_asyncio.fixture
async def mongo_test_collection(
    mongo_client: AsyncIOMotorClient
):
    test_db = mongo_client.test
    
    collection_name = 'test'
    
    collection = test_db[collection_name]
    
    yield collection
    
    print('Deleting mongo data...')
    await collection.delete_many({})
    await test_db.drop_collection(collection_name)
    
@pytest_asyncio.fixture
async def init_mongo_beanie(
    mongo_container: Container,
    mongo_client: AsyncIOMotorClient
):
    """
    Inits Beanie models with MongoDB
    """
    
    await init_beanie(
        database=mongo_client.test, # type: ignore
        document_models=[
            Note
        ]
    )
    
    yield mongo_client.test
    mongo_client.close()
