from os import path
import uuid
from s3_storage.bucket_abstraction import ObjectStorageBucket


class MinioStorageBucket(ObjectStorageBucket):
    chunk_size = 4096

    def __init__(self, client: Minio):
        super().__init__()
        self.client = client


    def download(self, bucket: str, object: str, save_location: str = "/tmp"):
        response = None
        try:
            response = self.client.get_object(bucket_name=bucket, object_name=object)
            file_name = str(uuid.uuid4())
            file_path = path.join(save_location, file_name)
            with open(file_path, 'wb') as out:
                while True:
                    data = response.read(self.chunk_size)
                    if not data:
                        break
                    out.write(data)
            return file_path
        finally:
            response.close()
            response.release_conn()