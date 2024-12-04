FROM alpine:3.20

# Use a volume for external file access
VOLUME /result

ENV PYTHON_VER=3.8.2

# Install Dependencies
RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.20/community" >> /etc/apk/repositories
RUN apk update && apk add --update gcc patchelf git vim wget bash scons musl-dev

RUN apk add --update poetry

ADD . /tfdocs
WORKDIR /tfdocs
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install

ENV MUSL_PATH=/lib/ld-musl-x86_64.so.1
ENV ZLIB_PATH=/lib/libz.so.1
RUN poetry run pyinstaller \
  --noconfirm \
  tfdocs.spec

# # Bundle Binary into Static Binary using StaticX
# RUN poetry run staticx dist/tfdocs tfdocs

# Copy out the build artefact
# CMD cp tfdocs /result && ls -sh1 /result
CMD ["bash"]

