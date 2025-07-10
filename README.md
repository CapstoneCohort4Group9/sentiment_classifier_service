# sentiment_classifier_service


## Environment setup
```
powershell
python -m venv _env

 .\_env\Scripts\activate

 pip install -r requirements.txt

 .\_env\Scripts\deactivate
```

## To test it locally
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8095
```
 
 ```browser
http://localhost:8095/docs#/
```