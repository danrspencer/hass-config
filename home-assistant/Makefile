IP=			192.168.0.35
USER=		pi
PASS=		raspberry

get-config:
	echo ${PASS} | pbcopy
	scp ${USER}@${IP}:/home/homeassistant/.homeassistant/*.yaml ./config

put-config:
	echo ${PASS} | pbcopy
	scp -rp ./ ${USER}@${IP}:/home/pi/
	ssh ${USER}@${IP} "sudo cp ./config/*.yaml /home/homeassistant/.homeassistant/ && sudo reboot"

make secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

upgrade-hass:
	echo ${PASS} | pbcopy
	ssh ${USER}@${IP} "sudo pip3 install --upgrade homeassistant && sudo reboot"
