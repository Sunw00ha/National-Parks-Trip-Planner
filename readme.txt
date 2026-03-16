README setup file
Names: Irene Ha, Ejean Kuo, Henron Ruan


S3 Policies
    - Go to IAM.
    - On the left, look for policies.
    - Create a policy.
    - Copy this JSON into the JSON editor: 
        task 2: 
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": ["s3:PutObject"],
              "Resource": "arn:aws:s3:::nationalparkapp/*"
            }
          ]
        }

        task 3:
         {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject",
                        "s3:GetObject"
                    ],
                    "Resource": [
                        "arn:aws:s3:::nationalparkapp/*"
                    ]
                }
            ]
        }
    - Click the format json button to make it look nicer.
    - Save the policy.
    - enable S3 object permissions for Task 2
    - Go to S3 bucket, click permissions, add this bucket policy to allow the chart image to be opened upon clicking the generated URL
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadObjects",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::national-park-task2/*"
                }
            ]
        }

Database Setup
    - Assuming you have a database instance in AWS RDS setup, run the schema.sql file included to set up the database. Switch out the user name and password for however you see fit.
p
Lambda Configuration
    - Make a Lambda function by going to the Lambda section of the AWS console and pasting the code into a new lambda function. 
        - Task 1: parkboundaries
        - Task 2: activity-chart
        - Task 3: parkImages
    - Task 1
        - Go to the Lambda function tab. 
        - Go to the Configuration tab. 
        - In “general configuration,” change the time limit to 10 minutes
        - Go to “Permissions”.
        - Go to the Configuration tab for the lambda function. 
        - Add environmental variables
            - Variable 1:
            - Key: NPS_API_KEY
            - Value: cJiyEdJza5KbUti3SiPV74zO90xvYnKjU2FeqSy5
    - Task 2
        - Go to the Lambda function tab. 
        - Go to the Configuration tab. 
        - In “general configuration,” change the time limit to 10 minutes
        - Go to “Permissions”.
        - Go to the Configuration tab for the lambda function. 
        - Add environmental variables
            - Variable 1:
                Key: NPS_API_KEY
                Value: cJiyEdJza5KbUti3SiPV74zO90xvYnKjU2FeqSy5
            - Variable 2:
                Key: CHART_BUCKET
                Value: [name of s3 bucket]
    - Task 3
        - Go to the Lambda function tab. 
        - Go to the Configuration tab. 
        - In “general configuration,” change the time limit to 10 minutes and the max memory to 5000 MB (so we can use a memory buffer to hold the .zip file)
        - Go to “Permissions”.
        - Click the link in “Role Name”.
        - Click “Add Permissions” and attach the S3 policy we made earlier.
        - Now go back to the Configuration tab for the lambda function. 
        - Go to environment variables.
        - Add the following environment variables
            - API_KEY: <whatever your API key is for calling the NPS API>
            - BUCKET_NAME: <whatever your bucket name is>
            - DB_ENDPOINT: <whatever DB link you want to use>
            - DB_NAME: <whatever database name you want to use>
            - DB_PORT_NUMBER: 3306
            - DB_USERNAME: <whatever username you need to access DB_NAME before>
            - DB_PASSWORD: <whatever password you need to access DB_NAME>
            - EXPIRATION: 400 (this is just the time it takes for the link to expire, we have set it default to be 10 minutes = 600 seconds)
            - LIMIT: 500 (the maximum number of images we are compressing)
            - REGION_NAME: us-east-2

Lambda Layer Setup (assuming the lambda functions are already set up)
    - At the very top of the screen, in the menu bar with the settings and the search symbol, click on the Cloudshell icon. 
    - Once in the shell, run the following commands in this order
        rm -rf python
        mkdir python
        cd python
        # this command changes depending on the task you are setting up
            - task 1: pip3 install requests typing_extensions==4.14.1 -t .
            - task 2: pip3 install requests boto3 typing_extensions==4.14.1 -t .
            - task 3: pip3 install requests boto3 pymysql tenacity typing_extensions==4.14.1 -t .
        cd ..
        zip -r <layer>.zip python
        aws s3 cp parkImages-layer.zip s3://<whatever bucket name the layer should go in>
    - scroll down to layers and click “edit,” then “add a layer,” then “custom layers,” then look for the one that we just made; you might have to click the refresh button on the right if you don’t see it
    - configure the layer for x86 and Python 3.14 runtime	

Setting Up Gateway
    - First, create an API called “NationalParkAPI”
    - Task 1: 
        - Create resource called “parkboundaries”
        - Within that resource, create another resource called {sitecode}. Create a method for this /{sitecode} resource using a “GET” method and enabling lambda proxy integration, attach the “parkboundaries” lambda function.
    - Task 2: 
        - Create a Resource called “activitiestchart” under resource path “/”
        - Click on the path /activity-chart and create a “POST” method with integration type Lambda Function, Lambda proxy integration turned on, and the “activitychart” lambda function selected.
    - Task 3: 
        - Add a new resource, call it “parkimages” under resource path “/”
        - Within that resource, create another resource called {park} that utilizes the “GET” method and connects to the lambda function for this task “imagedownload”; make sure to enable “proxy integration,” otherwise we will not be able to access the event structure of the lambda function.

To run the client.py file, type “python3 client.py” on the command line and follow the instructions provided. 
