gcloud compute instances create-with-container tb-houston-vm \
   --container-image gcr.io/eagle-console-resources/tb-houston-service-image:latest \
   --container-command "python app.py" \
   --container-arg="config/gcp_development.py" \
   --container-arg="True"
