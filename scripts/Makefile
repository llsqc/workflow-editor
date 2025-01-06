# Makefile for infrastructure setup

# Target: infra
# Target: infra
infra-up:
	@echo "创建应用依赖的容器"
	docker-compose --project-name workflow-editor -f ./docker-compose.yaml up --build -d
	@echo "创建完成"


# Target: infra-down
infra-down:
	@echo "停止应用依赖的容器"
	docker-compose --project-name workflow-editor -f ./docker-compose.yaml down
	@echo "停止成功"

all:
	make infra-up

clean:
	@echo "清除创建的容器"
	make infra-down