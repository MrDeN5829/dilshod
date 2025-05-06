Final Project: Full Web Application Deployment on AWS

Overview

This project demonstrates how to deploy a full-stack web application using:

Amazon EC2 – Hosting a Flask backend

Amazon RDS (PostgreSQL) – Hosting the database

Amazon S3 – Hosting the static frontend

Features

Display data from PostgreSQL RDS

Add and delete sample data

Fully deployed and accessible via the internet

Phase 1: Database Setup (RDS – PostgreSQL)

Step 1: Choose a Dataset

Visit Kaggle Datasets

Download a CSV dataset of your choice

Step 2: Launch RDS PostgreSQL Instance

Go to RDS → Databases → Create database

Choose Standard Create

Engine: PostgreSQL, version 15 or higher

DB Instance Identifier: db_<first_name>

Master username: postgres, Password: your password

DB instance class: db.t3.micro (free tier)

Enable public access

Use default VPC and subnet group

(Optional) Uncheck "Enable Storage Auto Scaling"

Step 3: Configure RDS Security Group

Go to EC2 → Security Groups

Edit inbound rules for your RDS security group:

Type: PostgreSQL

Port: 5432

Source: your EC2 instance’s security group or 0.0.0.0/0 (testing only)

Step 4: Import Dataset to RDS

Use DBeaver or psql CLI to:

Connect to your RDS PostgreSQL instance

Create a table: tbl_<first_name>_data

Import your CSV into the table

Phase 2: Static Website Hosting (S3)

Step 5: Create S3 Bucket

Go to S3 → Create bucket

Name it (e.g., webapp-<first_name>)

Uncheck "Block all public access"

Step 6: Upload Frontend Files

Upload index_<first_name>.html, CSS, and JS files

Step 7: Make Files Public

Apply the following Bucket Policy:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}

Step 8: Enable Static Website Hosting

Go to Properties → Static website hosting

Index document: index_<first_name>.html

Copy the Endpoint URL

Phase 3: EC2 Deployment

Step 9: Launch EC2 Instance

Go to EC2 → Launch Instance

Choose Ubuntu Server 22.04 LTS

Instance type: t2.micro (free tier)

Enable auto-assign Public IP

Create/select key pair (e.g., webapp_<first_name>.pem)

Configure Security Group with these rules:

Inbound Rules

| Type        | Protocol | Port Range | Source     |
|-------------|----------|------------|------------|
| SSH         | TCP      | 22         | 0.0.0.0/0  |
| HTTP        | TCP      | 80         | 0.0.0.0/0  |
| HTTPS       | TCP      | 443        | 0.0.0.0/0  |
| All TCP     | TCP      | 0–65535    | 0.0.0.0/0  |
| All traffic | All      | All        | 0.0.0.0/0  |

Outbound Rules

| Type        | Protocol | Port Range | Destination |
|-------------|----------|------------|-------------|
| HTTPS       | TCP      | 443        | 0.0.0.0/0   |
| SSH         | TCP      | 22         | 0.0.0.0/0   |
| HTTP        | TCP      | 80         | 0.0.0.0/0   |
| All traffic | All      | All        | 0.0.0.0/0   |

Step 10: Connect & Set Up Flask Backend

ssh -i webapp_<first_name>.pem ubuntu@<EC2_PUBLIC_IP>

# Update system and install tools
sudo apt update
sudo apt install python3-pip python3-venv postgresql-client

# Create project directory
mkdir webapp_<first_name>
cd webapp_<first_name>

# Create virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install flask psycopg2-binary flask-cors python-dotenv

# Create Flask app
nano app.py

Paste your Flask code into app.py and save.

Step 11: Run the Flask App

python app.py

Visit your API:

http://<EC2_PUBLIC_IP>:5000/data

Phase 4: Connect Frontend with API

Step 12: Update Frontend JavaScript

In index_<first_name>.html, set:

const API_BASE = 'http://<EC2_PUBLIC_IP>:5000';

Useful Links

EC2 API Endpoint: http://<EC2_PUBLIC_IP>:5000

S3 Static Site: http://your-bucket-name.s3-website-region.amazonaws.com/index_<first_name>.html

RDS Endpoint: <your_rds_endpoint>

Notes

Make sure EC2, RDS, and S3 are in the same AWS region

Use the correct ports and IP ranges in security groups

Do not use hardcoded credentials in production environments

License

This project is for educational use only.

