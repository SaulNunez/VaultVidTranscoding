import sys
import pika
import os
from s3_storage.bucket_abstraction import ObjectStorageBucket
from s3_storage.minio_storage_bucket import MinioStorageBucket
from s3_storage.models import S3StorageAccessInformation
from minio import Minio

from transcoding.transcoding import start_transcoding_process

def get_message_queue_connection_information() -> str:
    return os.getenv("MESSAGE_QUEUE_HOST", "localhost")

def get_s3_bucket_storage_information() -> S3StorageAccessInformation:
    url = os.getenv("OBJECT_STORE_URL")
    access_key = os.getenv("OBJECT_STORE_ACCESS_KEY")
    secret_key = os.getenv("OBJECT_STORE_SECRET_KEY")

    if access_key is None:
        raise Exception("OBJECT_STORE_ACCESS_KEY environment variable not defined. " \
                        "Please set this variable with the access key to your S3 compatible storage.")
    
    if secret_key is None:
        raise Exception("OBJECT_STORE_SECRET_KEY environment variable not defined. " \
                        "Please set this variable with the password to access you S3 compatible storage.")

    return {url, access_key, secret_key}

def create_s3_instance(params: S3StorageAccessInformation) -> ObjectStorageBucket:
    client = Minio(
        params.url,
        access_key=params.access_key, 
        secret_key=params.secret_key,
        )
    return MinioStorageBucket(client)

def main():
    object_storage = create_s3_instance(get_s3_bucket_storage_information())
    def callback(ch, method, properties, body):
        bucket = body['bucket']
        object_location = ['object']
        location_in_local_cache = object_storage.download(bucket, object_location)
        start_transcoding_process(location_in_local_cache)
        if os.path.exists(location_in_local_cache):
            os.remove(location_in_local_cache)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    VIDEO_TRANSCODING_QUEUE = "vault_vid_new_video_transcoding"

    message_queue_host = get_message_queue_connection_information()

    connection = pika.BlockingConnection(pika.ConnectionParameters(message_queue_host))
    channel = connection.channel()

    channel.queue_declare(queue=VIDEO_TRANSCODING_QUEUE, durable=True)

    channel.basic_consume(queue=VIDEO_TRANSCODING_QUEUE,
                        on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)