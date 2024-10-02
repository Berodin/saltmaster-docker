# Definiere Versionsargumente für Alpine und SaltStack
ARG ALPINE_VERSION=3.19

# Basis-Python-Image mit Alpine
FROM python:3.10-alpine${ALPINE_VERSION} AS saltmaster

ARG SALT_VERSION=3007.0

# Installiere notwendige Abhängigkeiten und Salt
RUN apk add --no-cache gcc g++ autoconf make libffi-dev openssl-dev libgit2-dev gettext cmake pkgconfig && \
    apk add --no-cache libgit2 dumb-init && \
    pip install --no-cache-dir 'cython<3' ruamel.yaml && \
    echo 'cython<3' > /tmp/constraint.txt && \
    PIP_CONSTRAINT=/tmp/constraint.txt USE_STATIC_REQUIREMENTS=1 \
    pip install --no-build-isolation --no-cache-dir --default-timeout=1000 \
        salt==${SALT_VERSION} pygit2==1.14.1 && \
    rm -rf /var/cache/apk/* /tmp/*

# Erstelle notwendige Verzeichnisse und setze Berechtigungen
RUN addgroup -g 450 -S salt && \
    adduser -s /bin/sh -SD -G salt salt && \
    mkdir -p /etc/salt /var/cache/salt /var/log/salt /srv/salt /run/salt && \
    chown -R salt:salt /etc/salt /var/cache/salt /var/log/salt /srv/salt /run/salt && \
    chmod -R 2775 /etc/salt /var/cache/salt /var/log/salt /var/run/salt

# Stelle sicher, dass die richtigen Berechtigungen für Salt-Binärdateien gesetzt sind
RUN chmod +x /usr/local/bin/salt-master /usr/local/bin/salt-minion

# Kopiere das EntryPoint-Skript
COPY entrypoint.py /entrypoint.py
RUN chmod +x /entrypoint.py

# Exponiere die notwendigen Ports für Salt
EXPOSE 4505 4506

# Setze EntryPoint
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint.py"]
