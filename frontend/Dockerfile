FROM node:22-alpine

WORKDIR /app

# Copiar package files
COPY package.json ./

# Instalar dependencias
RUN npm install

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 5173

# Comando de desarrollo
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
