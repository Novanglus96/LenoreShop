# develop stage
FROM node:lts-alpine AS develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# build stage
FROM develop-stage AS build-stage
RUN npm run build

# production stage
FROM nginx:stable-alpine AS production-stage
LABEL maintainer="John Adams"
LABEL version="1.6.23"

# Copy build artifacts
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Install tzdata for timezone data
RUN apk add -U tzdata

# Set timezone environment variable (default to UTC if not set)
ARG TZ=Etc/UTC
ENV TIMEZONE=${TZ}

# Link the timezone data
RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && echo $TIMEZONE >/etc/timezone

# Expose the port
EXPOSE 80

# Copy entrypoint script to set timezone
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Command to run the entrypoint script and start the development server
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
