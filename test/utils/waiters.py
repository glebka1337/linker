import docker
import time
def _check_is_container_ready(
    client: docker.DockerClient,
    container_name: str
) -> bool:
    
    try:
        container = client.containers.get(
            container_id=container_name
        )
        container.reload()
        return container.stats == 'running'
    except:
        return False

def _wait_container_for_start(
    docker_client: docker.DockerClient,
    container_name: str
) -> None:
    for _ in range(10):
        if _check_is_container_ready(
            client=docker_client,
            container_name=container_name
        ):
            break
        
        time.sleep(0.5)