sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx/nginx.conf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/gunicornconf.py /etc/gunicorn.d/hello.py
sudo /etc/init.d/nginx restart
#sudo /etc/init.d/gunicorn restart
sudo gunicorn -c /etc/gunicorn.d/hello.py
sudo service mysql start
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS qaapp DEFAULT CHARACTER SET='utf8';"
sudo python ask/manage.py makemigrations qa
sudo python ask/manage.py migrate
curl -vv http://10.42.9.128/question/3141592/
