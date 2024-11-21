export DOCKER_BUILDKIT=0 && export COMPOSE_DOCKER_CLI_BUILD=0
docker build -f Dockerfile --no-cache -t llms/txt2img:2.0 .