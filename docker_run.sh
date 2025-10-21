docker stop notes_de_cours || true
docker rm notes_de_cours || true
docker run -d -p 2222:22 -v /root/ssh_notes_de_cours/:/home/mkdocsuser/.ssh --network n8n_local --name notes_de_cours notes_de_cours
docker exec notes_de_cours chown mkdocsuser:mkdocsuser /home/mkdocsuser/.ssh/authorized_keys
docker exec notes_de_cours chown mkdocsuser:mkdocsuser /home/mkdocsuser/.ssh
docker exec notes_de_cours chmod 700 /home/mkdocsuser/.ssh
docker exec notes_de_cours chmod 600 /home/mkdocsuser/.ssh/authorized_keys
