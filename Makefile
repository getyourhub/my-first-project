.PHONY: build run test clean

# 构建Docker镜像
build:
	docker build -t subtitles .

# 运行测试
test:
	python test_subtitles.py

# 运行程序（示例）
run:
	python main.py samples/example.srt --translator google --target-lang zh-cn

# 清理
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/

# 安装依赖
install:
	pip install -r requirements.txt

# 显示帮助
help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker image"
	@echo "  make test     - Run tests"
	@echo "  make run      - Run example translation"
	@echo "  make clean    - Clean Python cache files"
	@echo "  make install  - Install Python dependencies"