$ docker exec chayuan-postgres psql -U chayuan_user -d chayuan_db -t -c "SHOW hba_file;"
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
        LANGUAGE = (unset),
        LC_ALL = "en_SG.utf8",
        LC_CTYPE = (unset),
        LC_NUMERIC = (unset),
        LC_COLLATE = (unset),
        LC_TIME = (unset),
        LC_MESSAGES = (unset),
        LC_MONETARY = (unset),
        LC_ADDRESS = (unset),
        LC_IDENTIFICATION = (unset),
        LC_MEASUREMENT = (unset),
        LC_PAPER = (unset),
        LC_TELEPHONE = (unset),
        LC_NAME = (unset),
        LANG = "en_SG.utf8"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
 /var/lib/postgresql/data/pgdata/pg_hba.conf

$ docker exec -u root chayuan-postgres sh -c 'echo "host chayuan_db chayuan_user 172.27.0.0/16 trust" >> /var/lib/postgresql/data/pgdata/pg_hba.conf'

$ psql -h localhost -U chayuan_user -d chayuan_db -c "\dt content.*"
psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  no pg_hba.conf entry for host "172.27.0.1", user "chayuan_user", database "chayuan_db", no encryption

$ docker exec chayuan-postgres psql -U chayuan_user -d chayuan_db -c "SELECT pg_reload_conf();"
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
        LANGUAGE = (unset),
        LC_ALL = "en_SG.utf8",
        LC_CTYPE = (unset),
        LC_NUMERIC = (unset),
        LC_COLLATE = (unset),
        LC_TIME = (unset),
        LC_MESSAGES = (unset),
        LC_MONETARY = (unset),
        LC_ADDRESS = (unset),
        LC_IDENTIFICATION = (unset),
        LC_MEASUREMENT = (unset),
        LC_PAPER = (unset),
        LC_TELEPHONE = (unset),
        LC_NAME = (unset),
        LANG = "en_SG.utf8"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
 pg_reload_conf 
----------------
 t
(1 row)

$ psql -h localhost -U chayuan_user -d chayuan_db -c "\dt content.*"
Did not find any relation named "content.*".

$ psql -h localhost -U chayuan_user -d chayuan_db -c "\dt *.*"

$ psql -h localhost -U chayuan_user -d chayuan_db -c "\dn"
      List of schemas
  Name  |       Owner       
--------+-------------------
 public | pg_database_owner
(1 row)

PGPASSWORD=chayuan_dev_password psql -h localhost -U chayuan_user -d chayuan_db -c "\dt"

