# =====================================================
# IntelliICU Frontend - Production Dockerfile
# =====================================================

# -----------------------------
# Stage 1: Build Vite frontend
# -----------------------------
FROM node:20-slim AS build

WORKDIR /app

# Copy dependency manifests
COPY package.json package-lock.json ./

# Install locked dependencies
RUN npm ci

# Explicitly install Rolldown Linux GNU native binding.
# Required for Vite 8 production builds in Linux containers.
RUN npm install --no-save @rolldown/binding-linux-x64-gnu

# Copy frontend source
COPY . .

# Build production frontend
RUN npm run build


# -----------------------------
# Stage 2: Serve with Nginx
# -----------------------------
FROM nginx:alpine

# Copy Vite production build
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]