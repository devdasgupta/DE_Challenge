FROM python:3.8.9-slim-buster

LABEL service="de-challenge" \
    schema.vcs-type="Git" \
    schema.vcs-url="https://github.com/devdasgupta/DE_Challenge"

ENV PATH=$PATH:/home/user/.local/bin \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_USER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    FLASK_SKIP_DOTENV=True \
    SHELL=/bin/sh \
    PAGER=cat \
    PIP_INSTALL_DEV='false'

RUN apt-get update && \
    apt-get install -y --no-install-recommends

# Avoid mixing $HOME and WORKDIR so important persistent files in $HOME such as
# ~/.local don't conflict with service runtime files.
WORKDIR /srv

# Run as a non-root user.
RUN useradd -ms $SHELL user \
 && chown -R user:user /srv
USER user

# Install the newest pip and setuptools.
RUN python -m pip install --upgrade --user pip setuptools

# Copy the entrypoint files for booting the application.
COPY --chown=user:user docker-entrypoint.sh setup.py setup.cfg /srv/

# Create a dummy service directory for the dependency installation.
# Install package with pip.
RUN mkdir -p /srv/de_challenge
RUN pip install /srv[dev,test]

# Copy the project director
COPY --chown=user:user de_challenge /srv/de_challenge

VOLUME /srv

# Use an entrypoint to run the application
ENTRYPOINT ["/docker-entrypoint.sh"]