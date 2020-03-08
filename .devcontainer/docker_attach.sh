docker container run \
    -it \
    --rm \
    --name image-share-container \
    --user vscode \
    --mount type=bind,source=/home/ubuntu/Projects/image-share,target=/workspace/image-share \
    --workdir /workspace/image-share \
    --publish 3034:3034 \
    e3cd678e04eb /bin/bash && pip3 install -r requirements.txt
