# =====================================================
# IntelliICU Frontend - Production Dockerfile
# =====================================================

# Build stage
# Use Debian-based Node instead of Alpine because
# Vite 8 / Rolldown requires platform-specific native bindings.
FROM node:20-slim AS build

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install exact dependencies from lock file
RUN npm ci

# Copy frontend source
COPY . .

# Build Vite production application
RUN npm run build


# =====================================================
# Production stage
# =====================================================

FROM nginx:alpine

# Copy production build from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]