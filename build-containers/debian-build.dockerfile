FROM debian:bullseye-slim

# Use a volume for external file access
RUN mkdir -p /result

# Install Dependencies
RUN apt-get update
RUN apt-get install -y gcc patchelf git vim wget bash scons musl musl-dev make \
  zlib1g-dev build-essential libffi-dev libssl-dev libsqlite3-dev \
  libc6-dev libbz2-dev

WORKDIR /python
RUN wget https://www.python.org/ftp/python/3.11.10/Python-3.11.10.tgz && \
  tar xzf Python-3.11.10.tgz && \
  cd Python-3.11.10 && \
  ./configure \
    --enable-shared \
    --enable-optimizations \
    --prefix=/usr/local \
    LDFLAGS="-Wl,--rpath=/usr/local/lib" \
    && \
  make -j 1 && \
  make altinstall && \
  mv python /usr/local/bin

WORKDIR /poetry
RUN python -m ensurepip --upgrade
# ADD build-containers/install_poetry.py install_poetry.py
# RUN chmod +x install_poetry.py && ./install_poetry.py

# RUN python3 -m pip install --user pipx && \
#   python3 -m pipx ensurepath

RUN python -m pip install poetry

ADD . /tfdocs
WORKDIR /tfdocs
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# # Install Python dependencies via Poetry
RUN python -m poetry install

# # Set required environment variables for MUSL and ZLIB paths
# ENV MUSL_PATH=/lib/ld-musl-x86_64.so.1
# ENV ZLIB_PATH=/lib/libz.so.1

# # Run PyInstaller to package the app
RUN python -m poetry run pyinstaller \
  --noconfirm \
  tfdocs.spec

# # Bundle Binary into Static Binary using StaticX
# RUN poetry run staticx dist/tfdocs tfdocs
# due to certain python libraries requiring C-libs, this can't be used currently :/

# Copy out the build artefact
# CMD ["sh", "-c", "set -e; cp dist/tfdocs /result && ls -sh1 /result"]
CMD ["bash"]
