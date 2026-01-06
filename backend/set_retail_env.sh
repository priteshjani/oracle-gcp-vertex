# 1. Standardize your variables
export PROJECT_ID=$(gcloud config get-value project)
export REPO_NAME="oracel-retail-demo-repo"
export REGION="us-east4"
export IMAGE_NAME="oracle-retail"
export FULL_IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:latest"
