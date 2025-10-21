eval "$(ssh-agent -s)"
docker build --ssh default . -t notes_de_cours
