# Use an official Node.js runtime as a parent image
FROM node:latest
# Enable corepack for pnpm
RUN corepack enable
# Set working directory to /app
WORKDIR /app
# Copy package.json and pnpm-lock.yaml
COPY package*.json pnpm-lock.yaml ./
# Install dependencies
RUN pnpm install
# Copy the rest of the files
COPY . .
# Build the project
RUN pnpm run build
# Expose port 3000 for the application
EXPOSE 3000
# Set the command to start the application using pnpm run start
CMD ["pnpm", "run", "start"]