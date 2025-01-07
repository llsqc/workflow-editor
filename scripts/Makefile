all: infra-up check-containers data-init

# Target: infra-up
infra-up:
	@echo "创建应用依赖的容器"
	docker-compose --project-name workflow-editor -f ./docker-compose.yaml up --build -d
	@echo "创建完成"

# Target: check-containers
check-containers:
	@echo "检查容器是否全部启动"
	@RetVal=1; \
	while [ $$RetVal -ne 0 ]; do \
		sleep 2; \
		docker-compose --project-name workflow-editor -f ./docker-compose.yaml ps | grep -q "Up"; \
		RetVal=$$?; \
	done
	@echo "所有容器已启动"

# Target: data-init
data-init:
	@echo "初始化样例数据"
	python3 ./data_init.py
	@echo "初始化完成"
	@echo "首页: http://localhost:3000"

# Target: infra-down
infra-down:
	@echo "停止应用依赖的容器"
	docker-compose --project-name workflow-editor -f ./docker-compose.yaml down
	@echo "停止成功"

clean: infra-down
	@echo "清除创建的容器"
	make infra-down