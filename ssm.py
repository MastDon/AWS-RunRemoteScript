### Import required python libraries
import os
import time
import shutil
#import boto
#import s3fs




### MySQL database details to which backup to be done.

DB_HOST = 'localhost' # Can be RDS/localhost
DB_USER = 'backup'
DB_USER_PASSWD = 'password1'
BACKUP_PATH = '/tmp/hell' # location on local host to save dump before uploading to S3
DeleteOlderThan = 10 # Delete the dumps older then mentioned days

### Convert the Time into Seconds

DeleteOlderThan = int(DeleteOlderThan) * 86400

### Getting current datetime like "Sunday-16.11.2014" to create separate directory for backup.

DATETIME = time.strftime('%A-%d.%m.%Y')


### Checking that the the backup directory already exists, if not then it will create it.

### Creating backup folder

if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)

os.chdir(BACKUP_PATH)

### Get the list of databases

GET_DB_LIST = "mysql -u %s -p%s -h %s --silent -N -e 'show databases'" % (DB_USER, DB_USER_PASSWD, DB_HOST)

for DB_NAME in os.popen(GET_DB_LIST).readlines():
    DB_NAME = DB_NAME.strip()
    if DB_NAME == 'information_schema':
        continue
    if DB_NAME == 'performance_schema':
        continue
    if DB_NAME == 'mysql':
        os.popen("mysqldump -u %s  --events --ignore-table=mysql.event -p%s -h %s -e --opt -c %s | gzip -c > %s.gz" % (DB_USER,DB_USER_PASSWD,DB_HOST,DB_NAME,DB_NAME+"_"+DATETIME))
    else:
        os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz" % (DB_USER,DB_USER_PASSWD,DB_HOST,DB_NAME,DB_NAME+"_"+DATETIME))

os.popen('aws s3 cp /tmp/hell s3://dp-s3-education/backup_test/ --recursive')
