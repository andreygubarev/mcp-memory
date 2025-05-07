.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

DOCKER_IMAGE := andreygubarev/mcp-remote-memory
DOCKER_TAG := $(shell git describe --always)

.PHONY: build
build: ## Build the Docker image
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

.PHONY: run
run: build ## Run Docker container
	docker run --rm -it $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: push
push: ## Push the Docker image to Docker Hub
	docker buildx build --push --platform linux/amd64,linux/arm64 -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
