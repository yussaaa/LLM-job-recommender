import os
import json
import boto3


def save_file_to_s3(file_name, bucket_name="job-recommender-bucket-yusa"):
    """Save file to S3 bucket

    Args:
        file_name (str): file name
        bucket_name (str): bucket name
    """
    try:
        s3 = boto3.client("s3")  # Boto3 will automatically search for credentials
        s3.upload_file(file_name, bucket_name, file_name)
    except Exception as e:
        print(e)


# # Make sure the data folder exists
# data_folder = "data"
# if not os.path.exists(data_folder):
#     os.makedirs(data_folder)

# FILE_NAME = "data/output.json"
# # Save the JSON data to a file
# with open(FILE_NAME, "w") as file:
#     json.dump(data, file)
