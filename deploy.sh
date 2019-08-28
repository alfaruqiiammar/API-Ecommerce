sudo docker stop flaskbaru
sudo docker rm flaskbaru
sudo docker rmi alfaruqi26/flask-api:2.0
sudo docker run -d --name flaskbaru -p 5000:5000 alfaruqi26/flask-api:2.0
