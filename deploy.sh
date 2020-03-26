gcloud compute instances create-with-container tb-houston-vm \
   --container-image gcr.io/tranquility-base-images/tb-houston-service:alpha \
   --container-command "python app.py" \
   --container-arg="config/gcp_development.py" \
   --container-arg="True"
