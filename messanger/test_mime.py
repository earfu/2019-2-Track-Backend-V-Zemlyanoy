import boto3
import magic

MCS_ACCESS_KEY = 'tHwmMmsEpYjEpxBRQ3FefU'
MCS_SECRET_KEY = 'gE8MpxyfXway76BfY2iwhrkbgwziwcjqF2PAn5612PGL'

def attach(filename):

    mime = open(filename, mode='rb')
   # magic.from_buffer(mime.read(), mime=True)
 #   if (not mime):
  #      print('Not true')
  #      return


    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url='http://hb.bizmrg.com',
        aws_access_key_id=MCS_ACCESS_KEY,
        aws_secret_access_key=MCS_SECRET_KEY,
        )
  #  print(mime, mime.name, hash(mime.name))
    byts = mime.read()
   # print(byts)
    return s3_client.put_object(Bucket='messanger_zemlyanoy', Key=(str(hash(mime.name)) + mime.name), Body=byts )
