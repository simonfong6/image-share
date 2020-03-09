docker container run \
    -it \
    --rm \
    --name image-share-container \
    --user vscode \
    --mount type=bind,source=/home/ubuntu/Projects/image-share,target=/workspace/image-share \
    --workdir /workspace/image-share \
    --publish 1343:1343 \
    image-share.mothakes.com.image:latest /bin/bash && pip3 install -r requirements.txt
