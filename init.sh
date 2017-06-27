sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx/nginx.conf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/gunicornconf.py /etc/gunicorn.d/hello.py
sudo /etc/init.d/nginx restart
sudo /etc/init.d/gunicorn restart
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS qaapp DEFAULT CHARACTER SET='utf8';"
