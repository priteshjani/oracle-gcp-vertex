# Retail Supermarket Demo

This project demonstrates a retail supermarket application using **Google Cloud Platform (GCP)**, **Oracle Autonomous Database**, and **Vertex AI**.

## Architecture

*   **Frontend**: HTML/JS/CSS (Static Web App).
*   **Backend**: Python FastAPI.
*   **AI**: Vertex AI (Gemini) for natural language to SQL conversion.
*   **Database**: Oracle Autonomous Database (simulated connection/mock for demo).
*   **Infrastructure**: Shared VPC Architecture (Host Project + Service Project).

## Prerequisites

*   Google Cloud Platform Account.
*   [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated.
*   [Terraform](https://developer.hashicorp.com/terraform/downloads) installed.
*   Docker (optional, for local container testing).
*   Python 3.9+.

## Local Development

1.  **Install Dependencies**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2.  **Generate Mock Data**
    ```bash
    # From the root directory
    python scripts/generate_data.py
    ```
    This script generates mock inventory data and creates `scripts/init_db.sql`.

3.  **Run Backend**
    ```bash
    cd backend
    uvicorn main:app --reload --port 8000
    ```
    The API will be available at `http://localhost:8000`.

4.  **Run Frontend**
    Open `frontend/index.html` in your browser.
    *   Note: For full functionality, you might need a local server (e.g., `python -m http.server`) to avoid CORS issues with some browsers/file protocols, though the backend is configured to allow `*`.

## Deployment to GCP

### 1. Infrastructure Setup (Terraform)

The `infra/` directory contains Terraform code to set up the Shared VPC and Oracle peering.

1.  **Configure Variables**
    Edit `infra/variables.tf` or create a `terraform.tfvars` file:
    ```hcl
    host_project_id    = "your-host-project-id"
    service_project_id = "your-service-project-id"
    region             = "us-central1"
    ```

2.  **Apply Terraform**
    ```bash
    cd infra
    terraform init
    terraform apply
    ```

### 2. Oracle Database Setup

1.  Provision an **Oracle Autonomous Database** via the Google Cloud Marketplace (or OCI linked to GCP).
2.  Ensure the database is peered with the Shared VPC created by Terraform.
3.  Execute the SQL generated in `scripts/init_db.sql` to create the `INVENTORY` table and populate data.
4.  Note down the connection details (DSN, User, Password).

### 3. Backend Deployment (Cloud Run)

Deploy the backend to the **Service Project**.

1.  **Build and Push Container**
    ```bash
    cd backend
    gcloud builds submit --tag gcr.io/YOUR_SERVICE_PROJECT_ID/retail-backend
    ```

2.  **Deploy to Cloud Run**
    ```bash
    gcloud run deploy retail-backend \
      --image gcr.io/YOUR_SERVICE_PROJECT_ID/retail-backend \
      --platform managed \
      --region us-central1 \
      --project YOUR_SERVICE_PROJECT_ID \
      --allow-unauthenticated \
      --set-env-vars DB_USER=admin,DB_PASSWORD=secret,DB_DSN=your_dsn,PROJECT_ID=your_project_id
    ```
    *   Replace env vars with your actual Oracle DB credentials.
    *   Ensure the Cloud Run service connector (if used) or VPC access connector is configured to reach the Shared VPC if using private IP.

### 4. Frontend Deployment

1.  **Update API URL**
    Edit `frontend/script.js` and replace `http://localhost:8000/search` with your Cloud Run Service URL.
    ```javascript
    const API_URL = "https://retail-backend-xyz-uc.a.run.app/search";
    ```

2.  **Host Static Files**
    You can host the `frontend/` directory using **Firebase Hosting** or a **GCS Bucket**.

    **Example: GCS Bucket**
    ```bash
    gsutil mb gs://your-frontend-bucket
    gsutil -m rsync -r frontend/ gs://your-frontend-bucket
    gsutil iam ch allUsers:objectViewer gs://your-frontend-bucket
    ```

## Demo Usage

1.  Navigate to your frontend URL.
2.  Enter a query like: *"Show me shoes for boys size 7 in blue"*
3.  The system uses Vertex AI to interpret the query -> generates SQL -> queries Oracle DB -> displays results.
