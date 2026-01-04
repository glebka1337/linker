"""Client will be used as fixture"""
import pytest
import docker

@pytest.fixture(scope='session')
def docker_client():
    docker_cl = docker.from_env()
    yield docker_cl
    docker_cl.close()
