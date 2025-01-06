# Makefile for infrastructure setup

all:	infra-up
	@echo "初始化样例数据"
	python3 ./data_init.py
	@echo "初始化完成"

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


clean:	infra-down
	@echo "清除创建的容器"
	make infra-down