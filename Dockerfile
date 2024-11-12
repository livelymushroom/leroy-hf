# syntax=docker/dockerfile:1.0.0-experimental
FROM ghcr.io/cinnamon/kotaemon:main-full as base_image

RUN useradd -m -u 1000 user
RUN --mount=type=ssh chown -R user:user /app
RUN --mount=type=ssh chown -R user:user /usr/local/lib/python3.10
USER user
WORKDIR /app

COPY app.py /app

ENV GRADIO_SERVER_NAME=0.0.0.0
ENV KH_FEATURE_USER_MANAGEMENT=true

ENTRYPOINT ["python", "app.py"]
EXPOSE 7860