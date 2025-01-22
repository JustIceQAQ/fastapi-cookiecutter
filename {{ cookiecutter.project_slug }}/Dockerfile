ARG PYTHON_VERSION=3.11.11-slim-bookworm

FROM python:${PYTHON_VERSION} AS python
FROM python AS python-build-stage
ARG BUILD_ENVIRONMENT=production
WORKDIR /app
COPY ./requirements .
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt


FROM python AS python-run-stage
ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app
WORKDIR ${APP_HOME}
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/
COPY . ${APP_HOME}
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
