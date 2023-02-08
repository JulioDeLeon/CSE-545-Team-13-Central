echo $1 | sudo -S ufw default deny incoming
echo $1 | sudo -S ufw default deny outgoing
echo $1 | sudo -S ufw reload