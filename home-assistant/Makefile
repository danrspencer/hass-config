IP=			192.168.0.35
USER=		pi

get-config:
	scp ${USER}@${IP}:/home/homeassistant/.homeassistant/*.yaml ./config

put-config:
	scp -rp ./ ${USER}@${IP}:/home/pi/
	ssh ${USER}@${IP} "./scripts/put-config.sh"

restart-hass:
	ssh ${USER}@${IP} "sudo systemctl restart home-assistant@homeassistant.service"

tail-logs:
	ssh ${USER}@${IP} "tail -f /home/homeassistant/.homeassistant/home-assistant.log"

make secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

upgrade-hass:
	ssh ${USER}@${IP} "./scripts/upgrade-hass.sh"

put-authorized-keys:
	scp ~/.ssh/id_rsa.pub ${USER}@${IP}:/home/pi
	ssh ${USER}@${IP} "mkdir -p ~/.ssh \
									&& mv ./id_rsa.pub ~/.ssh/authorized_keys \
									&& chmod 600 ~/.ssh/authorized_keys"
