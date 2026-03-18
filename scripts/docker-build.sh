#!/bin/bash
set -e

echo "=== Docker 构建和发布脚本 ==="

# 配置
IMAGE_NAME="fastapi-practice"
VERSION="0.1.0"
REGISTRY="${DOCKER_REGISTRY:-docker.io}"
DOCKERFILE="${DOCKERFILE:-Dockerfile}"

# 构建镜像
build() {
    echo "构建 Docker 镜像..."
    docker build -t "${IMAGE_NAME}:${VERSION}" -t "${IMAGE_NAME}:latest" -f "${DOCKERFILE}" .
    echo "构建完成：${IMAGE_NAME}:${VERSION}"
}

# 本地运行测试
run() {
    echo "本地运行容器..."
    docker run -d --rm -p 8000:8000 --name "${IMAGE_NAME}" "${IMAGE_NAME}:${VERSION}"
    echo "容器已启动：http://localhost:8000"
    echo "停止命令：docker stop ${IMAGE_NAME}"
}

# 推送到仓库
push() {
    if [ -z "$1" ]; then
        echo "错误：请指定镜像标签"
        echo "用法：$0 push <tag>"
        exit 1
    fi
    TAG=$1
    echo "推送镜像到 ${REGISTRY}/${IMAGE_NAME}:${TAG}..."
    docker tag "${IMAGE_NAME}:${VERSION}" "${REGISTRY}/${IMAGE_NAME}:${TAG}"
    docker push "${REGISTRY}/${IMAGE_NAME}:${TAG}"
    echo "推送完成"
}

# 清理
clean() {
    echo "清理 Docker 资源..."
    docker stop "${IMAGE_NAME}" 2>/dev/null || true
    docker rm "${IMAGE_NAME}" 2>/dev/null || true
    echo "清理完成"
}

# 主逻辑
case "${1:-build}" in
    build)
        build
        ;;
    run)
        run
        ;;
    push)
        push "$2"
        ;;
    clean)
        clean
        ;;
    all)
        build
        run
        ;;
    *)
        echo "用法：$0 {build|run|push|clean|all}"
        echo ""
        echo "命令说明:"
        echo "  build   - 构建 Docker 镜像"
        echo "  run     - 本地运行容器"
        echo "  push    - 推送到仓库 (需指定标签)"
        echo "  clean   - 停止并删除容器"
        echo "  all     - 构建并运行"
        exit 1
        ;;
esac
