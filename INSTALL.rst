sudo apt-get update && sudo apt-get upgrade

#sudo locale-gen en_US.UTF-8
#sudo locale-gen uk_UA.UTF-8

sudo apt-get install python-virtualenv python-pip libpq-dev python-dev postgresql-contrib git
sudo apt-get install postgresql

git clone https://github.com/gromoleg/k-server.git

virtualenv env

. ./env/bin/activate

pip install -r k-server/requirements.txt

deactivate

sudo su - postgres

createdb kdb

psql

CREATE USER oledbg WITH password 'pLcwkHpNXs8Jhktx';

GRANT ALL PRIVILEGES ON DATABASE kdb TO oledbg;

\q
logout

. ./env/bin/activate

cd k-server

./manage.py migrate

./manage.py runserver 0.0.0.0:8000
