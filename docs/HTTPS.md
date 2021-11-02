# Domains and HTTPS with NGINX & certbot
Embedded iframes are easy if your site only uses HTTP. But if your site uses HTTPS, then you can likely see your donation button at `http://YOUR_SERVER_IP:8000/` but not in the embeded iframe due to HTTPS security policies. It is best that we create a new subdomain like `xmrsale.yoursite.com` from which we can serve payments. Install NGINX, and create a new file `/etc/nginx/sites-enabled/xmrsale`:
```
server {
    listen 80;
    server_name xmrsale.YOURWEBSITE.com;

    location / {
        proxy_pass http://localhost:8000;
	proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```
Check with `nginx -t` and then `systemctl restart nginx`.

Now point your domain `xmrsale.YOURWEBSITE.com` DNS to your server IP. Then create HTTPS certificates by runnining the `certbot` command (or whatever else you use).

You could also try provide Gunicorn with your website's HTTPS certificate directly by using the flags `--certfile=cert.pem --keyfile=key.key`. If you use certbot for SSL, your keys are probably in `/etc/letsencrypt/live/`.
