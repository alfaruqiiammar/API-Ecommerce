sudo docker stop flask-api
sudo docker rm flask-api
sudo docker rmi alfaruqi26/flask-api
sudo docker run -d --name flaskbaru -p 5000:5000 alfaruqi26/flask-api:2.0
