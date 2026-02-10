# Multi-stage Dockerfile for Crypto Retirement Web App

# Stage 1: Build frontend assets
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/ ./

# Install dependencies
RUN npm ci --silent

# Build static assets
RUN npm run build || true

# Stage 2: Production web server
FROM nginx:alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend build artifacts
COPY --from=frontend-builder /app/frontend/dist/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Use non-root user
RUN adduser -D -u 1000 nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d

RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid && \
    chmod -R 770 /var/run/nginx.pid

USER nginx

CMD ["nginx", "-g", "daemon off;"]