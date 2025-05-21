#!/bin/sh

# Set timezone
if [ -n "$TZ" ]; then
    echo "Setting timezone to $TZ"
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone
else
    echo "Timezone not set, defaulting to UTC"
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" >/etc/timezone
fi

# Load environment variables from .env file
sed -i "s|__VITE_API_KEY__|${VITE_API_KEY}|g" /usr/share/nginx/html/index.html

# Execute the main process
exec "$@"
