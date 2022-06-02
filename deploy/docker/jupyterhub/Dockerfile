FROM continuumio/miniconda3:4.10.3p0-alpine@sha256:dc976a37da75088ab3d458ab266910b0b5afa2c9d971b01ae0cdcd4cc3a97247
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
      jupyterhub=2.3.0 \
      jupyterhub-kubespawner=4.1.0 \
      psycopg2-binary==2.9.1 && \
    pip install \
      oauthenticator==14.2.0 \
      jupyterhub-idle-culler==1.2.1

RUN mkdir -p /srv/jupyterhub/
COPY config-wrapper.py /srv/jupyterhub/config-wrapper.py
WORKDIR /srv/jupyterhub/
EXPOSE 8000

LABEL org.jupyter.service="jupyterhub"

CMD ["python", "/srv/jupyterhub/config-wrapper.py"]