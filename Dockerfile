# syntax=docker/dockerfile:1.4

# Use a base Ubuntu image
FROM ubuntu:rolling

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    python3 \
    python3-pip \
    python3-venv \
    git \
    openssh-client \
    nano \
    nginx \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment for Python (optional)
RUN python3 -m venv /opt/mkdocs-venv
ENV PATH="/opt/mkdocs-venv/bin:$PATH"

# Install MkDocs
RUN pip3 install mkdocs-material \ 
                 markdown-include \ 
                 openpyxl \
                 pyyaml \
                 mkdocs-video \
                 mkdocs-table-reader-plugin

# Create a non-root user for SSH access
RUN useradd -m -s /bin/bash mkdocsuser

# Set a password for the new user (replace 'your_password' with a strong password)
RUN echo 'mkdocsuser:Xy_XHR=H$#BvDFTuVtL9MM' | chpasswd

# Create the SSH directory for the new user
RUN mkdir /home/mkdocsuser/.ssh && \
    chown mkdocsuser:mkdocsuser /home/mkdocsuser/.ssh

RUN echo PATH=\"/opt/mkdocs-venv/bin:\$PATH\" >> /home/mkdocsuser/.profile
RUN echo PATH=\"/opt/mkdocs-venv/bin:\$PATH\" >> /home/mkdocsuser/.bashrc
RUN echo eval \"\$\(ssh-agent -s\)\" >> /home/mkdocsuser/.profile
RUN echo eval \"\$\(ssh-agent -s\)\" >> /home/mkdocsuser/.bashrc
RUN echo ssh-add /home/mkdocsuser/.ssh/id_ed25519 >> /home/mkdocsuser/.profile
RUN echo ssh-add /home/mkdocsuser/.ssh/id_ed25519 >> /home/mkdocsuser/.bashrc

# Add GitHub's public key to known_hosts to avoid interactive prompts
RUN ssh-keyscan github.com >> /home/mkdocsuser/.ssh/known_hosts \
    && chown mkdocsuser:mkdocsuser /home/mkdocsuser/.ssh/known_hosts

# Add GitHub's public key to known_hosts to avoid interactive prompts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts 

# Clone a private repository using the forwarded SSH agent
# The key itself is never copied into the container
RUN mkdir /notes_de_cours && \
    chown mkdocsuser:mkdocsuser /notes_de_cours
RUN --mount=type=ssh git clone git@github.com:jaixan/bm.git /notes_de_cours/bm && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/bm
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/developpementweb3.git /notes_de_cours/developpementweb3 && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/developpementweb3
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/piratage.git /notes_de_cours/piratage && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/piratage
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/techno.git /notes_de_cours/techno && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/techno
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/techinfo.git /notes_de_cours/techinfo && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/techinfo
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/support.git /notes_de_cours/support && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/support
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/bd1.git /notes_de_cours/bd1 && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/bd1
RUN --mount=type=ssh git clone git@github.com:cegepvictoetienne/bd2.git /notes_de_cours/bd2 && \
    chown -R mkdocsuser:mkdocsuser /notes_de_cours/bd2

# Remove the default Nginx configuration file
RUN rm /etc/nginx/nginx.conf

# Copy your custom nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Copy index.html to nginx html directory
COPY index.html /usr/share/nginx/html/index.html

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Allow password-based authentication (for simplicity, consider key-based auth for production)
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
# Allow root login (optional, but can be useful for debugging)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config
# Expose the SSH port
EXPOSE 22
# Expose the HTTP port 
EXPOSE 80

# Start supervisor which in turn starts nginx and sshd
CMD ["/usr/bin/supervisord"]