###########
# Stage 1 #
# Frontend#
###########

FROM node:lts-alpine AS frontend-builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

##########
# Stage 2#
#  Final  #
##########

FROM python:3.11.4-slim-bookworm

LABEL maintainer="John Adams"
LABEL version="1.7.0-rc.10"

# Install system dependencies: nginx, supervisord, db clients, netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    netcat-openbsd \
    postgresql-client \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system --group app

# App directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/staticfiles $APP_HOME/mediafiles $APP_HOME/data
WORKDIR $APP_HOME

# Copy logos into staticfiles
COPY backend/logos/favicon.ico $APP_HOME/staticfiles/favicon.ico
COPY backend/logos/logov2.png $APP_HOME/staticfiles/logov2.png

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/dist /app/frontend/dist

# Copy nginx config
COPY nginx/nginx.conf /etc/nginx/sites-available/lenoreshop
RUN ln -sf /etc/nginx/sites-available/lenoreshop /etc/nginx/sites-enabled/lenoreshop \
    && rm -f /etc/nginx/sites-enabled/default

# Copy backend source
COPY backend/ $APP_HOME

# Copy and configure entrypoint
COPY backend/entrypoint.sh $APP_HOME/entrypoint.sh
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh \
    && chmod +x $APP_HOME/entrypoint.sh

# Own app files
RUN chown -R app:app $APP_HOME

EXPOSE 80

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
