from storages.backends.s3 import S3Storage


class SupabaseStorage(S3Storage):

    def url(self, name):
        return (
            "https://xmjjupcbhkxgzgybvlif.supabase.co"
            "/storage/v1/object/public/"
            f"{self.bucket_name}/{name}"
        )