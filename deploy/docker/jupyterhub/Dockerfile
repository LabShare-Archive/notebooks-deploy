FROM frolvlad/alpine-miniconda3:python3.7@sha256:ca48cb5d359d6de5311d909754f39bbe34227f583158b7a4eec9089d4686aa01
LABEL maintainer="Labshare <konstantin.taletskiy@labshare.org>"

# Track semantic versioning
COPY VERSION /

# Copy cull-idle script
COPY cull-idle-servers.py /srv/jupyterhub/config/cull-idle-servers.py

# Copy ModularSpawner
COPY modularspawner /modularspawner

RUN conda install --yes -c conda-forge \
      git \
      sqlalchemy \
      tornado \
      jinja2 \
      traitlets \
      requests \
      pycurl \
      nodejs=12 \
      configurable-http-proxy && \
    pip install \
      git+https://github.com/jupyterhub/jupyterhub.git@3800ceaf9edf33a0171922b93ea3d94f87aa8d91#egg=jupyterhub \
      oauthenticator==14.0.0 \
      jupyterhub-kubespawner==1.0.0 \
      /modularspawner && \
    npm install -g polus-railyard && \
    rm -rf ~/.cache ~/.npm /modularspawner

RUN mkdir -p /srv/jupyterhub/
WORKDIR /srv/jupyterhub/
EXPOSE 8000

LABEL org.jupyter.service="jupyterhub"

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]