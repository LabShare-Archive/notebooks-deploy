FROM labshare/polyglot-notebook:0.9.0

USER root
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -O /usr/bin/jq
RUN chmod +x /usr/bin/jq

USER $NB_UID

USER root
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -O /usr/bin/jq
RUN chmod +x /usr/bin/jq

USER $NB_UID

# Install easybuild
ENV EASYBUILD_PREFIX=/opt/modules \
    EASYBUILD_BUILDPATH=/tmp/easybuild
RUN pip install --ignore-installed easybuild==4.5.1