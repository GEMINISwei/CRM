FROM node:20.15.1

ARG API_URL
ARG IDLE_TIME

ENV VITE_API_URL=${API_URL}
ENV VITE_IDLE_TIME=${IDLE_TIME}

WORKDIR /app
COPY . .
RUN npm install && npm run build
