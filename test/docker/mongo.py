import pytest
import docker
from src.models.note import Note
from test.utils.waiters import _wait_container_for_start

@pytest.fixture(scope='session')
def mongo_container(
    docker_client: docker.DockerClient
):
    container_name = "mongodb_linker_test"
    
    container = docker_client.containers.run(
        name=container_name,
        image='mongo:7.0',
        ports={
            '27017/tcp':27018
        },
        detach=True,
        remove=True,
        environment={
            'MONGO_INITDB_ROOT_USERNAME': 'test',
            'MONGO_INITDB_ROOT_PASSWORD': 'test',
            'MONGO_INITDB_DATABASE': 'test'
        }
    )
    try:
        
        _wait_container_for_start(
            docker_client,
            container_name
        )    
        yield container
        
    finally:
        container.stop()
        
