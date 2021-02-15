FROM mysql:5
COPY nnuh.sql /docker-entrypoint-initdb.d/

 # install python modules
ADD mysqld_charset.cnf /etc/mysql/conf.d/
RUN chmod 0444 /etc/mysql/conf.d/mysqld_charset.cnf
