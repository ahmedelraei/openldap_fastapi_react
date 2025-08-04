FROM node:22-alpine

# Enable corepack to use pnpm
RUN corepack enable

WORKDIR /app

# Copy package files
COPY package*.json pnpm-lock.yaml* ./

 
RUN pnpm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start the application in development mode
CMD ["pnpm", "run", "dev"]
