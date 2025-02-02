FROM node:20.15.1 AS frontend-builder

ARG API_URL
ENV VITE_API_URL=$API_URL

WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:1.26
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d
