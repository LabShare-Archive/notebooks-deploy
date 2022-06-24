FROM continuumio/miniconda3:4.12.0@sha256:58b1c7df8d69655ffec017ede784a075e3c2e9feff0fc50ef65300fc75aa45ae
LABEL maintainer="Labshare <konstantin.taletskiy@labshare.org>"

# Track semantic versioning
COPY VERSION /

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
      jupyterhub=2.3.1 \
      jupyterhub-kubespawner=4.1.0 \
      psycopg2-binary==2.9.3 \
      oauthenticator=15.0.1 \
      jupyterhub-idle-culler=1.2.1


RUN mkdir -p /srv/jupyterhub/
COPY config-wrapper.py /srv/jupyterhub/config-wrapper.py
WORKDIR /srv/jupyterhub/
EXPOSE 8000

LABEL org.jupyter.service="jupyterhub"

CMD ["python", "/srv/jupyterhub/config-wrapper.py"]