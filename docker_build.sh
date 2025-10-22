eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
DOCKER_BUILDKIT=1 docker build --ssh default . -t notes_de_cours
