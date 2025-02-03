FROM node:20.15.1

ARG API_URL
ENV VITE_API_URL=$API_URL

WORKDIR /app
COPY . .
RUN npm install && npm run build
