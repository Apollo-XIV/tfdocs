FROM fedora:latest

# Use a volume for external file access
RUN mkdir -p /result
# VOLUME /result


# Install Dependencies
RUN dnf -y update
RUN dnf -y install gcc patchelf git vim wget bash scons musl musl-devel \
  python3 python3-pip python3-virtualenv poetry dnf clean all

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
# due to certain python libraries requiring C-libs, this can't be used currently :/

# Copy out the build artefact
# CMD ["sh", "-c", "set -e; cp dist/tfdocs /result && ls -sh1 /result"]
CMD ["bash"]

