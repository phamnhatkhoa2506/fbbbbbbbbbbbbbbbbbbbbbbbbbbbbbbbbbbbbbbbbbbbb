* Deploy
    1. gcloud auth login
    2. gcloud secrets create APIFY_KEYS --replication-policy=automatic
    3. echo '["APIFY_TOKEN_1", "APIFY_TOKEN_2", "APIFY_TOKEN_3"]' | gcloud secrets versions add APIFY_KEYS --data-file=-
    4. gcloud functions deploy crawl_facebook_pages --runtime python312 --trigger-http --entry-point crawl_facebook_pages --region asia-southeast1 --memory 2GB --service-account export-social-data@creator-dev-453406.iam.gserviceaccount.com --timeout 500
    5. $token = gcloud auth print-identity-token
        $headers = @{ Authorization = "Bearer $token" }
    6. Invoke-WebRequest -Uri "https://asia-southeast1-creator-dev-453406.cloudfunctions.net/crawl_facebook_pages" -Method GET -Headers $headers

* Code fix:
    from google.cloud import secretmanager
    from apify_client import ApifyClient

    /////
    def get_api_key():
        """Lấy API key dựa theo ngày hiện tại"""
        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/APIFY_KEYS/versions/latest"
        
        response = client.access_secret_version(request={"name": secret_name})
        api_keys = json.loads(response.payload.data.decode("UTF-8"))

        # Lấy API key theo ngày (luân phiên)
        day_index = datetime.datetime.utcnow().day % len(api_keys)
        return api_keys[day_index]