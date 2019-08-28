docker stop flask-api
docker rm flask-api
docker rmi alfaruqi26/flask-api
docker run -d --name flaskbaru -p 5000:5000 alfaruqi26/flask-api:2.0
