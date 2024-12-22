# Makefile for infrastructure setup

# Target: infra
# Target: infra
infra-up:
	@echo "初始化开发环境的基础设施"
	docker-compose --project-name workflow-editor -f ./docker-compose-dev.yaml up -d
	@echo "初始化完成"


# Target: infra-down
infra-down:
	@echo "Stopping development environment..."
	docker-compose --project-name workflow-editor -f ./docker-compose-dev.yaml down
	@echo "Development environment stopped successfully."