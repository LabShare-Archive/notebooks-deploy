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
      escapism==1.0.1 \
      psycopg2-binary==2.9.1 \
      git+https://github.com/jupyterhub/jupyterhub.git@17ba49117c79628b475f161d33debbf03c35fd94#egg=jupyterhub \
      oauthenticator==14.2.0 \
      jupyterhub-kubespawner==1.1.0 \
      /modularspawner && \
    npm install -g polus-railyard && \
    rm -rf ~/.cache ~/.npm /modularspawner

RUN mkdir -p /srv/jupyterhub/
COPY config-wrapper.py /srv/jupyterhub/config-wrapper.py
WORKDIR /srv/jupyterhub/
EXPOSE 8000

LABEL org.jupyter.service="jupyterhub"

CMD ["python", "/srv/jupyterhub/config-wrapper.py"]