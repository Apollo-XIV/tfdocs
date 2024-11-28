ARG BASE_IMAGE=debian:latest
FROM ${BASE_IMAGE}
RUN useradd -m test-user
USER test-user:1000
WORKDIR /home/test-user
COPY . .
CMD ["bash"]
