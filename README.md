# AutoML 

Web Application for automatic learning and validation of Time Series Models. All .env files were added to repo for convinience. 

## Run
```bash
docker-compose --env-file .env.dev up --build   
```

## Stop
```bash
docker-compose --env-file .env.dev down --remove-orphans 
```

## Usage

### Minio Object Storage base creds and URL
- User: AKIAIOSFODNN7EXAMPLE
- Password: bPxRfiCYEXAMPLEKEY
- URL: 0.0.0.0:9001

### Model Manager Swagger
- URL: 0.0.0.0:8000/api/docs