echo $1 | sudo -S ufw default allow incoming
echo $1 | sudo -S ufw default allow outgoing
echo $1 | sudo -S ufw reload