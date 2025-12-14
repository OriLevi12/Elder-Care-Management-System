FROM node:18-alpine

# Install tini for proper signal handling
RUN apk add --no-cache tini

WORKDIR /react-frontend

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the port React runs on
EXPOSE 3000

# Use tini to handle signals properly for graceful shutdown
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["npm", "start"]
