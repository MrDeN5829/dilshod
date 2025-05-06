
# Final Project: Full Web Application Deployment on AWS

## Overview

This repository demonstrates the deployment of a full-stack web application using:

- **Amazon EC2**: for hosting the Flask backend
- **Amazon RDS (PostgreSQL)**: as the database backend
- **Amazon S3**: for static website hosting of the frontend

The application consists of:

- A static HTML/JS frontend served from S3
- A Flask API (`app.py`) running on EC2, connecting to RDS
- Two operations: **Add** and **Delete** data in the `tbl_<first_name>_data` table

---

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
