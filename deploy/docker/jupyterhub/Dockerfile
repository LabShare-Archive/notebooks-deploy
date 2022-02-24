FROM frolvlad/alpine-miniconda3:python3.7@sha256:bf5c88b66776e27b6745a7489104263d4ec05748eb447e7a292a0c4b5ed6c074
LABEL maintainer="Labshare <konstantin.taletskiy@labshare.org>"

# Track semantic versioning
COPY VERSION /

# Copy cull-idle script
COPY cull-idle-servers.py /srv/jupyterhub/config/cull-idle-servers.py

RUN conda install --yes -c conda-forge \
      git \
      sqlalchemy \
      tornado \
      jinja2 \
      traitlets \
      requests \
      pycurl \
      nodejs=12 \
      configurable-http-proxy \
      escapism=1.0.1 \
      jupyterhub=2.1.1 \
      python-kubernetes=22.6.0 \
      jupyterhub-kubespawner=2.0.1 && \
    pip install \
      psycopg2-binary==2.9.1  \
      oauthenticator==14.2.0

RUN mkdir -p /srv/jupyterhub/
COPY config-wrapper.py /srv/jupyterhub/config-wrapper.py
WORKDIR /srv/jupyterhub/
EXPOSE 8000

LABEL org.jupyter.service="jupyterhub"

CMD ["python", "/srv/jupyterhub/config-wrapper.py"]