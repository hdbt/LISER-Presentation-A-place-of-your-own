# Build for linux/amd64. Version tags are fixed; see README for digest caveat.
FROM node:22.14.0-bookworm-slim AS node_runtime
FROM python:3.12.9-bookworm
ARG QUARTO_VERSION=1.7.32
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=UTC LANG=C.UTF-8
COPY --from=node_runtime /usr/local/bin/node /usr/local/bin/node
RUN curl --fail --location --retry 3 \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz" \
    -o /tmp/quarto.tar.gz \
    && mkdir -p /opt/quarto \
    && tar -xzf /tmp/quarto.tar.gz -C /opt/quarto --strip-components=1 \
    && ln -s /opt/quarto/bin/quarto /usr/local/bin/quarto \
    && rm /tmp/quarto.tar.gz \
    && quarto --version
WORKDIR /project
COPY requirements.txt requirements.lock ./
COPY vendor/ vendor/
RUN python -m pip install --no-index --find-links=vendor --require-hashes -r requirements.lock
COPY . .
# Rebuild during image creation, so missing inputs or failing checks fail the build.
RUN python build.py
ENTRYPOINT ["python", "build.py"]
CMD ["--output-dir", "/output"]
