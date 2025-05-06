
# Final Project: Full Web Application Deployment on AWS

## Overview

This project demonstrates how to deploy a full-stack web application using:

- **Amazon EC2** – Hosting a Flask backend
- **Amazon RDS (PostgreSQL)** – Hosting the database
- **Amazon S3** – Hosting the static frontend

### Features

- Display data from PostgreSQL RDS
- Add and delete sample data
- Fully deployed and accessible via the internet


## Phase 1: Database Setup (RDS – PostgreSQL)

### Step 1: Choose a Dataset

- Visit [Kaggle Datasets](https://www.kaggle.com/datasets)
- Download a CSV dataset of your choice

### Step 2: Launch RDS PostgreSQL Instance

1. Go to **RDS → Databases → Create database**
2. Choose **Standard Create**
3. Engine: **PostgreSQL**, version 15 or higher
4. DB Instance Identifier: `db_<first_name>`
5. Master username: `postgres`, Password: your password
6. DB instance class: `db.t3.micro` (free tier)
7. Enable public access
8. Use default VPC and subnet group
9. (Optional) Uncheck "Enable Storage Auto Scaling"

### Step 3: Configure RDS Security Group

- Go to **EC2 → Security Groups**
- Edit inbound rules for your RDS security group:
  - Type: PostgreSQL
  - Port: 5432
  - Source: your EC2 instance’s security group or `0.0.0.0/0` (testing only)

### Step 4: Import Dataset to RDS

- Use **DBeaver** or **psql CLI** to:
  1. Connect to your RDS PostgreSQL instance
  2. Create a table: `tbl_<first_name>_data`
  3. Import your CSV into the table


## Phase 2: Static Website Hosting (S3)

### Step 5: Create S3 Bucket

1. Go to **S3 → Create bucket**
2. Name it (e.g., `webapp-<first_name>`)
3. Uncheck "Block all public access"

### Step 6: Upload Frontend Files

- Upload `index_<first_name>.html`, CSS, and JS files

### Step 7: Make Files Public

Apply the following **Bucket Policy**:

```json
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
```
###Step 8: Enable Static Website Hosting

- Go to Properties → Static website hosting
- Index document: index_<first_name>.html
- Copy the Endpoint URL

## Phase 3: EC2 Instance Deployment

### Step 8: Enable Static Website Hosting

1. Go to **S3 → Properties → Static website hosting**
2. Enable Static website hosting
3. Set **Index document** to `index_<first_name>.html`
4. Note the **endpoint URL**

### Step 9: Launch EC2 Instance (Ubuntu)

1. Go to **EC2 → Launch Instance**
2. Choose **Ubuntu Server 22.04 LTS**
3. Instance type: **t2.micro** (free tier)
4. Enable auto-assign Public IP
5. Create or use a key pair (e.g., `webapp_<first_name>.pem`)
6. Configure **Security Group** as follows:

#### Inbound Rules

| Rule         | Protocol | Port       | Source    |
|--------------|----------|------------|-----------|
| SSH          | TCP      | 22         | 0.0.0.0/0 |
| HTTP         | TCP      | 80         | 0.0.0.0/0 |
| HTTPS        | TCP      | 443        | 0.0.0.0/0 |
| All TCP      | TCP      | 0 - 65535  | 0.0.0.0/0 |
| All traffic  | All      | All        | 0.0.0.0/0 |

#### Outbound Rules

| Rule         | Protocol | Port Range | Destination |
|--------------|----------|------------|-------------|
| HTTPS        | TCP      | 443        | 0.0.0.0/0   |
| SSH          | TCP      | 22         | 0.0.0.0/0   |
| HTTP         | TCP      | 80         | 0.0.0.0/0   |
| All traffic  | All      | All        | 0.0.0.0/0   |

### Step 10: Connect to EC2 and Set Up Backend

```bash
ssh -i webapp_<first_name>.pem ubuntu@<EC2_PUBLIC_IP>

# Update & install required packages
sudo apt update
sudo apt install python3-pip python3-venv postgresql-client

# Create project directory and navigate into it
mkdir webapp_<first_name>
cd webapp_<first_name>

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install flask psycopg2-binary flask-cors python-dotenv

# Create Flask application
nano app.py
```

Paste your Flask code into `app.py` and save.

### Step 11: Run the Application

```bash
python app.py
```

Access the API at:

```
http://<EC2_PUBLIC_IP>:5000/data
```

---

## Phase 4: Connect Frontend with Backend

### Step 12: Update Frontend JavaScript

Ensure your JavaScript connects to the correct API base:

```js
const API_BASE = 'http://<EC2_PUBLIC_IP>:5000';
```

---

## Deployed Resource Links

- **EC2 API Endpoint**: http://<EC2_PUBLIC_IP>:5000
- **S3 Static Site**: http://your-bucket-name.s3-website-region.amazonaws.com/index_<first_name>.html
- **RDS Endpoint**: <your_rds_endpoint>

---

## Application Features

- View data from PostgreSQL RDS
- Add a sample row
- Delete a sample row

---

## Notes

- Ensure all AWS services are in the same region
- Confirm inbound and outbound rules are properly set

---

## License

This project is for educational purposes only.
