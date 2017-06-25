IP=			192.168.0.35
USER=		pi
PASS=		raspberry

get-config:
	echo raspberry | pbcopy
	scp ${USER}@${IP}:/home/homeassistant/.homeassistant/*.yaml ./config

put-config:
	echo raspberry | pbcopy
	scp -rp ./ ${USER}@${IP}:/home/pi/
	ssh ${USER}@${IP} "make finish-put-config"

finish-put-config:
	sudo cp ./config/*.yaml /home/homeassistant/.homeassistant/
	sudo reboot

make secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml
