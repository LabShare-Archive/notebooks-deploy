FROM python:3.9
RUN pip wheel easybuild-easyconfigs==4.5.3

FROM labshare/polyglot-notebook:0.9.3

USER root
RUN wget https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 -O /usr/bin/jq
RUN chmod +x /usr/bin/jq

USER $NB_UID

COPY --from=0 /easybuild* .

# Install easybuild
ENV EASYBUILD_PREFIX=/opt/modules \
    EASYBUILD_BUILDPATH=/tmp/easybuild
RUN pip install easybuild_easyconfigs-4.5.3-py3-none-any.whl easybuild==4.5.3