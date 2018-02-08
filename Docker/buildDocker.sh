NODE_BASE_IMAGE_NAME=anirbandas/kafkaspark_edge
NODE_BASE_VERSION="0.0.1"

function buildImage() {
    #VERSIONED_IMAGE="$NODE_BASE_IMAGE_NAME:$NODE_BASE_VERSION"
    #docker build -t $VERSIONED_IMAGE -f Dockerfile . 
    docker build -t $NODE_BASE_IMAGE_NAME -f dockerfile .
    docker tag $NODE_BASE_IMAGE_NAME $NODE_BASE_IMAGE_NAME:latest 
    echo "Tagged image...Pushing to Dockerhub"
    docker push $NODE_BASE_IMAGE_NAME:latest
}

echo "Building docker image..."
buildImage
echo "Build Done...Push Complete..."

