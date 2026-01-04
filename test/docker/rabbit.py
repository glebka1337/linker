import pytest
import docker
from test.utils.waiters import _wait_container_for_start

RABBITMQ_CONTAINER_NAME = "rabbitmq_linker_test"
RABBITMQ_DEFAULT_USER = "guest"
RABBITMQ_DEFAULT_PASS = "pass"
@pytest.fixture
def rabbitmq_container(
    docker_client: docker.DockerClient
): 
    global RABBITMQ_CONTAINER_NAME
    
    container = docker_client.containers.run(
        name=RABBITMQ_CONTAINER_NAME,
        image="rabbitmq:3-management",
        ports={
            "15672/tcp":15673, # TODO: Change in real world scenario
        },
        detach=True,
        remove=True,
        environment={
            "RABBITMQ_DEFAULT_USER":RABBITMQ_DEFAULT_USER,
            "RABBITMQ_DEFAULT_PASS":RABBITMQ_DEFAULT_PASS,
        }
    )
    _wait_container_for_start(
        docker_client,
        RABBITMQ_CONTAINER_NAME
    )
    yield container
    container.stop()
