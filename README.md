# Linux Server Configuration

------
## Descriptions
Configurate a Linux server and host my web applications.
Flask + Apache2 + mod_wsgi + sqlalchemy + postgreSQL

## Login with ssh
```$ ssh grader@119.29.111.231 -p 2200 -i location_of_privatekey```

## Web application URL
http://119.29.111.231/

## Software Installed
Some software installed with apt:
    finger, apache2, postgresql, python-pip, libapache2-mod-wsgi
Some packages install with pip:
click, Flask, httplib2, itsdangerous, Jinja2, MarkupSafe, pip, psycopg2, setuptools, six, SQLAlchemy, SQLAlchemy-Utils, Werkzeug, wheel,

## Configuration

> * All packages are updated.
    PS: check with command```$ sudo apt-get update```
> * Uncomplicated Firewall (UFW) is configured.
  (Only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123))
    PS: check with command```$ sudo ufw status```
> * A new user account named 'grader' with the permission to sudo is created.
    PS: check with command```$ finger grader```
> * PasswordAuthentication is forbidden and remote login of the root user disabled
PS: check with command```$ sudo vim /etc/ssh/sshd_config```
> * Local timezone is set to UTC
    PS: check with command```$ date```
> * wsgi and Apache config file are created
PS:
wsgi config file ： ```/home/grader/Udacity-FSND-catalog/catalog.wsgi```
    Apache config file  : ```/etc/apache2/sites-enabled/000-default.conf```
> * A new database user named 'catalog' is created.
PS: check with command
```
$ sudo su - postgres
$ psql
$ \du
```
> *  PostgreSQL configuration.
```$ vim /etc/postgresql/9.5/main/postgresql.conf```

## Location of the public SSH key
```/home/grader/.ssh/authorized_keys```