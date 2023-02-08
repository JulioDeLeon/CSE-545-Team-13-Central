echo $1 | sudo -S ufw allow out to any port 80   # http
echo $1 | sudo -S ufw allow out to any port 443  # https
echo $1 | sudo -S ufw allow out to any port 53   # DNS
echo $1 | sudo -S ufw reload