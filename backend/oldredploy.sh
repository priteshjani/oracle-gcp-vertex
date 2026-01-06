gcloud builds submit --tag gcr.io/my-service-prj-476616/oracle-vertex-app --project=my-service-prj-476616

gcloud run deploy oracle-vertex-service \
  --project=my-service-prj-476616 \
  --image=gcr.io/my-service-prj-476616/oracle-vertex-app \
  --region=us-east4 \
  --vpc-connector=projects/my-service-prj-476616/locations/us-east4/connectors/us-east4-cloudrun-connect \
  --service-account=787355230775-compute@developer.gserviceaccount.com \
  --set-env-vars="PYTHONUNBUFFERED=1" \
  --set-env-vars="PROJECT_ID=my-service-prj-476616" \
  --set-env-vars="LOCATION=us-east4" \
  --set-env-vars="DB_USER=agent_demo" \
  --set-env-vars="DB_PASSWORD=Agent_D8m0_next" \
  --set-env-vars="DB_CONNECT=(description=(retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=10.10.0.228))(connect_data=(service_name=gfce23053262d16_adbdemo_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=no)))" \
  --no-allow-unauthenticated

gcloud run services add-iam-policy-binding oracle-vertex-service   --region=us-east4   --member="allUsers"   --role="roles/run.invoker"   --project=my-service-prj-476616
