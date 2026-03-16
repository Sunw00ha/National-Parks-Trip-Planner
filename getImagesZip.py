# /parkimages
# Names: Irene Ha, Ejean Kuo, Henron Ruan

import json
import requests
import zipfile
import zlib
import uuid
from botocore.client import Config
import boto3
import io
import pymysql
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# open connection to database
def get_dbConn():
    try:
        endpoint = str(os.environ.get("DB_ENDPOINT"))
        portnum = int(os.environ.get("DB_PORT_NUMBER"))
        username = str(os.environ.get("DB_USERNAME"))
        pwd = str(os.environ.get("DB_PASSWORD"))
        dbname = str(os.environ.get("DB_NAME"))

        dbConn = pymysql.connect(host=endpoint, 
                                 port=portnum, 
                                 user=username, 
                                 passwd=pwd, 
                                 database=dbname, 
                                 client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)

        return dbConn

    except Exception as err:
        print(str(err))
        raise

# get bucketkey using park code if valid to use for downloading
# image, assuming the bucketkey already existed
@retry(stop = stop_after_attempt(3), 
        wait = wait_exponential(multiplier=1, min=2, max=30), 
        reraise = True
)
def get_bucketkey(park):
    try: 
        # open mySQL connection to execute relevant query
        dbConn = get_dbConn()
        dbCursor = dbConn.cursor()

        sql = """
            SELECT bucketkey
            FROM parks
            WHERE park = %s;
            """
        
        dbCursor.execute(sql, [park])

        row = dbCursor.fetchone()
        
        return row

    except Exception as err:
        print(str(err))
        raise

    # close cursor and connections if necessary
    finally:
        try:
            dbCursor.close()
        except:
            pass

        try:
            dbConn.close()
        except:
            pass

# insert a park:bucketkey entry into the database
@retry(stop = stop_after_attempt(3), 
        wait = wait_exponential(multiplier=1, min=2, max=30), 
        reraise = True
)
def insert_park(park, bucketkey):
    try:
        # open mySQL connection to execute relevant query
        dbConn = get_dbConn()
        dbCursor = dbConn.cursor()

        # use a transaction because we are inserting into the database
        dbConn.begin()

        print("**Executing insert...")

        sql = """
              INSERT INTO parks(park, bucketkey) VALUES (%s, %s);
              """

        dbCursor.execute(sql, [park, bucketkey])

        dbConn.commit()

        print("Insert complete!")

    except Exception as err:
        dbConn.rollback()
        print(str(err))
        raise

    # close cursor and connections if necessary
    finally:
        try:
            dbCursor.close()
        except:
            pass

        try:
            dbConn.close()
        except:
            pass

def lambda_handler(event, context):
    try: 
        print("** Getting images...")

        if "pathParameters" not in event:
            raise ValueError("request has no path parameters")
        
        pathParams = event["pathParameters"]

        if "park" not in pathParams:
            raise ValueError("request has no key park")

        park = pathParams["park"]

        print(f"park code is {park}")

        # check if we have done this park already
        row = get_bucketkey(park)

        # if the park is not in the database, then we have to call the 
        # park service API for the data
        if row == None or row == ():

            print("**Calling National Park Service API...")

            # the number of images is an environmental variable
            limit = int(os.environ.get("LIMIT"))

            # api url
            url = f"https://developer.nps.gov/api/v1/multimedia/galleries?parkCode={park}&limit={limit}"

            # API key is stored in an environmental variable
            API_KEY = str(os.environ.get("API_KEY"))

            response = requests.get(url, headers={"X-Api-Key": API_KEY})

            # remove the API_KEY from memory
            API_KEY = ""

            print("Response obtained")

            if response.status_code == 400:
                raise ValueError("park error")

            body = response.json()

            if "data" not in body:
                raise Exception("no galleries available")

            galleries = body["data"]

            if len(galleries) == 0:
                raise Exception("no galleries available")

            num = 1

            # use memory buffer for zipe file
            zip_file = io.BytesIO()
            
            # extract images into zip file 
            with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as myzip:
                for gallery in galleries:
                    if "images" not in gallery or not len(gallery["images"]):
                            continue
                    for image in gallery["images"]:
                        myzip.writestr(f"{image["title"]}.jpg".replace(" ", "_"), requests.get(image["url"]).content)
                        print(f"image {num} compressed")
                        num += 1

            # generate bucket key for zip file
            bucketkey = f"parks/{park}/{uuid.uuid1()}"  
            
            # upload zip file to s3
            bucketname = str(os.environ.get("BUCKET_NAME"))
            regionname = str(os.environ.get("REGION_NAME"))

            s3 = boto3.resource(
                's3',
                region_name=regionname,
                config = Config(
                    retries = {
                        'max_attempts': 3,
                        'mode': 'standard'
                    }
                )
            )

            bucket = s3.Bucket(bucketname)

            print("**Uploading file...")

            # upload zip file to s3
            zip_file.seek(0)
            bucket.upload_fileobj(zip_file, bucketkey)

            print("**Upload complete!")

            insert_park(park, bucketkey)

        # otherwise our bucket key already existed
        else:
            bucketkey = row[0]

        print("**Getting URL...")

        client = boto3.client("s3", config=Config(
            retries = {
                'max_attempts': 3,
                'mode': 'standard'
            }, 
            signature_version="s3v4"
        ))

        # declare a proper filename so that when the download procs, it will 
        # be provided in the proper file format
        filename = park + ".zip" 

        # get download url for zip file
        link = client.generate_presigned_url("get_object",
                                              Params={
                                                "Bucket": str(os.environ.get("BUCKET_NAME")), 
                                                "Key": bucketkey,
                                                "ResponseContentDisposition": f"attachment; filename = {filename}"
                                              }, 
                                              ExpiresIn=int(os.environ.get("EXPIRATION")))

        print(link)

        body = {
            'message': "success",
            'download_link': link
        }

        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }
                                                        
    except Exception as err:
        print("**Exception")
        print("**Message: ", str(err))

        status_code = 500

        if ValueError:
            status_code = 400

        body = {
            'message': str(err),
            'download_link': ""
        }

        return {
            'statusCode': status_code,
            'body': json.dumps(body)
        }

