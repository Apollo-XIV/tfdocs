FROM debian:bullseye-slim

# Use a volume for external file access
RUN mkdir -p /result

# Install Dependencies
RUN apt-get update
RUN apt-get install -y gcc patchelf git vim wget bash scons musl musl-dev \
    python3 python3-pip python3-venv python3-poetry

ADD . /tfdocs
WORKDIR /tfdocs
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install Python dependencies via Poetry
RUN poetry install

# Set required environment variables for MUSL and ZLIB paths
ENV MUSL_PATH=/lib/ld-musl-x86_64.so.1
ENV ZLIB_PATH=/lib/libz.so.1

# Run PyInstaller to package the app
RUN poetry run pyinstaller \
  --noconfirm \
  tfdocs.spec

# # Bundle Binary into Static Binary using StaticX
# RUN poetry run staticx dist/tfdocs tfdocs
# due to certain python libraries requiring C-libs, this can't be used currently :/

# Copy out the build artefact
# CMD ["sh", "-c", "set -e; cp dist/tfdocs /result && ls -sh1 /result"]
CMD ["bash"]
