# /generateactivitychart
# Names: Irene Ha, Ejean Kuo, Henron Ruan

import os
import json
import boto3
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime

s3 = boto3.client("s3")

NPS_API_KEY = os.environ.get("NPS_API_KEY")
CHART_BUCKET = os.environ.get("CHART_BUCKET")
NPS_BASE_URL = os.environ.get("NPS_BASE_URL", "https://developer.nps.gov/api/v1")


def lambda_handler(event, context):
    try:
        # 1. Read and validate input
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Missing request body"
                })
            }

        body = json.loads(event["body"])

        if "parkCodes" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Missing parkCodes in request body"
                })
            }

        park_codes = body["parkCodes"]

        if not isinstance(park_codes, list) or len(park_codes) == 0:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "parkCodes must be a non-empty list"
                })
            }

        park_codes = [str(code).strip().lower() for code in park_codes if str(code).strip()]

        if not park_codes:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "No valid park codes provided"
                })
            }

        if not NPS_API_KEY:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": "Missing NPS_API_KEY environment variable"
                })
            }

        if not CHART_BUCKET:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": "Missing CHART_BUCKET environment variable"
                })
            }

        # 2. Call NPS /parks API one park code at a time
        park_data = []

        for code in park_codes:
            nps_params = {
                "parkCode": code,
                "limit": 1,
                "api_key": NPS_API_KEY
            }

            nps_url = f"{NPS_BASE_URL}/parks?{urllib.parse.urlencode(nps_params)}"
            print("Calling NPS URL:", nps_url)

            with urllib.request.urlopen(nps_url, timeout=20) as response:
                nps_bytes = response.read()
                nps_json = json.loads(nps_bytes.decode("utf-8"))

            if isinstance(nps_json, list):
                nps_json = nps_json[0]

            print(f"Response for {code}:", json.dumps(nps_json)[:1500])

            returned_data = nps_json.get("data", [])
            if returned_data:
                park = returned_data[0]
                park_data.append(park)
                print("Returned park:", park.get("parkCode"), park.get("fullName"))
            else:
                print("No park returned for code:", code)

        if not park_data:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "error": "No parks found for provided park codes"
                })
            }

        # 3. Extract labels and counts
        labels = []
        counts = []
        park_counts = {}

        for park in park_data:
            park_name = park.get("fullName", park.get("name", "Unknown Park"))
            activities = park.get("activities", [])
            activity_count = len(activities)

            labels.append(park_name)
            counts.append(activity_count)
            park_counts[park_name] = activity_count

        print("Labels:", labels)
        print("Counts:", counts)

        # 4. Build QuickChart config
        chart_config = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Number of Activity Categories",
                        "data": counts,
                        "backgroundColor": "rgba(54, 162, 235, 0.8)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 1
                    }
                ]
            },
            "options": {
                "plugins": {
                    "legend": {
                        "display": False
                    },
                    "title": {
                        "display": True,
                        "text": "Activity Categories by National Park"
                    }
                },
                "scales": {
                    "x": {
                        "title": {
                            "display": True,
                            "text": "National Parks",
                            "font": {
                                "size": 14,
                                "weight": "bold"
                            }
                        }
                    },
                    "y": {
                        "title": {
                            "display": True,
                            "text": "Number of Activity Categories",
                            "font": {
                                "size": 14,
                                "weight": "bold"
                            }
                        },
                        "beginAtZero": True
                    }
                }
            }
        }

        quickchart_payload = {
            "chart": chart_config,
            "format": "png",
            "width": 1000,
            "height": 500,
            "backgroundColor": "white",
            "version": "4"
        }

        quickchart_data = json.dumps(quickchart_payload).encode("utf-8")
        quickchart_request = urllib.request.Request(
            url="https://quickchart.io/chart",
            data=quickchart_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(quickchart_request, timeout=20) as response:
            image_bytes = response.read()
            content_type = response.headers.get("Content-Type", "")

        print("QuickChart content type:", content_type)
        print("Image byte length:", len(image_bytes))

        # 5. Upload PNG to S3
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        object_key = f"charts/activity-chart-{'-'.join(park_codes)}-{timestamp}.png"

        s3.put_object(
            Bucket=CHART_BUCKET,
            Key=object_key,
            Body=image_bytes,
            ContentType="image/png"
        )

        # 6. Return result
        file_url = f"https://{CHART_BUCKET}.s3.us-east-2.amazonaws.com/{object_key}"

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Chart generated and uploaded successfully",
                "bucket": CHART_BUCKET,
                "key": object_key,
                "fileUrl": file_url,
                "parkCounts": park_counts
            })
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print("HTTPError:", e.code, error_body)
        return {
            "statusCode": 502,
            "body": json.dumps({
                "error": f"External API HTTP error: {e.code}",
                "details": error_body
            })
        }

    except urllib.error.URLError as e:
        print("URLError:", str(e))
        return {
            "statusCode": 502,
            "body": json.dumps({
                "error": f"External API URL error: {str(e)}"
            })
        }

    except Exception as e:
        print("Unhandled exception:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"Internal server error: {str(e)}"
            })
        }
