sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx/nginx.conf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/gunicornconfig.py /etc/gunicorn.d/hello.py
sudo /etc/init.d/nginx restart
sudo /etc/init.d/gunicorn restart
gunicorn -c /etc/gunicorn.d/hello.py hello:app
