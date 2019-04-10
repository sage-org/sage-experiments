FROM postgre:alpine

RUN mkdir -p /docker-entrypoint-initdb.d
RUN mkdir -p /opt/postgre_backup/

# copy init script
COPY restore_db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/restore_db.sh

# copy watdiv10Mn backup
COPY /home/ladda/watdiv10M_backup /opt/postgre_backup/watdiv10M

EXPOSE 5432
CMD ["postgres"]
