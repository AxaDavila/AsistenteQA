# frontend/Dockerfile
FROM node:20-alpine AS build

WORKDIR /app
# Copiamos los archivos de definición de dependencia
COPY package.json package-lock.json* ./
# Instalamos (omitimos el flag --silent para evitar errores de parseo)
RUN npm install --legacy-peer-deps
# Copiamos el resto de la app
COPY . .
# Compilamos la app
RUN npm run build

# Stage final (solo los artefactos)
FROM node:20-alpine
WORKDIR /app
COPY --from=build /app ./
EXPOSE 3000
CMD ["npm", "start"]
