# =====================================================
# IntelliICU Frontend - Production Dockerfile
# =====================================================

# =====================================================
# Stage 1: Build React + Vite Application
# =====================================================

FROM node:20-bookworm-slim AS build

WORKDIR /app

# Copy package manifest first.
# package-lock.json is intentionally not used for the Docker
# dependency installation because it may have been generated
# on Windows and omit Linux-specific optional native packages.
COPY package.json ./

# Install dependencies directly inside the Linux environment.
# This allows npm to resolve all required Linux-native optional
# dependencies for Vite, Rolldown, LightningCSS, etc.
RUN npm install \
    --include=optional \
    --no-audit \
    --no-fund

# Copy the complete frontend application.
COPY . .

# Build production Vite application.
RUN npm run build


# =====================================================
# Stage 2: Production Nginx Server
# =====================================================

FROM nginx:alpine AS production

# Remove default Nginx static content.
RUN rm -rf /usr/share/nginx/html/*

# Copy compiled Vite application.
COPY --from=build /app/dist /usr/share/nginx/html

# Create SPA-compatible Nginx configuration.
# This ensures React Router routes such as:
# /dashboard
# /patients/ICU-10264
# /telemetry
# work correctly when opened/refreshed directly.
RUN printf 'server {\n\
    listen 80;\n\
    server_name _;\n\
\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
\n\
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf)$ {\n\
        expires 1y;\n\
        add_header Cache-Control "public, immutable";\n\
        try_files $uri =404;\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]