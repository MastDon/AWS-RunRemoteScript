### Import required python libraries
import os
import time
import shutil
#import boto
#import s3fs

#from boto.s3.connection import S3Connection
#from boto.s3.key import Key
# s3://dp-s3-education/backup_test/  S3://bucket-name



#S3_BUCKET = 'dp-s3-education/backup_test'

### Create Connection to S3 ###

# aws_conn = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
# bucket_name = aws_conn.get_bucket(S3_BUCKET)


### MySQL database details to which backup to be done.

DB_HOST = 'localhost' # Can be RDS/localhost
DB_USER = 'backup'
DB_USER_PASSWD = 'password'
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

#### upload to the S3 Bucket Section

#s3_file = s3fs.S3FileSystem()
#local_path = BACKUP_PATH
#s3_path = S3_BUCKET
#s3_file.put(local_path, s3_path, recursive=True)

### Get the complete path of the file that we want to upload

# for root, dirs, files in os.walk(BACKUP_PATH):
#     for File_Name in files:
#         local_file_path = os.path.join(root, File_Name)
#         k = Key(bucket_name)
#         file_name_to_use_in_s3 = os.path.basename(local_file_path)
#         k.key = file_name_to_use_in_s3
#         k.set_contents_from_filename(local_file_path)
        ### Delete the Compressed Files from local backup directory
        # os.unlink(local_file_path)


### Delete the files from S3 Bucket, that are older than specified days
# for key in bucket_name.list():
#     last_modified_time = time.mktime(time.strptime(key.last_modified.split(".")[0], "%Y-%m-%dT%H:%M:%S"))
#     time_now = time.time()
#     if last_modified_time > (time_now - DeleteOlderThan):
#         continue
#     else:
#         print (key.name)
#         key.delete()
