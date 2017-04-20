sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
