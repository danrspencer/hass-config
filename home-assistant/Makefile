IP=			hassio.local
USER=		root

put-config:
	scp -rp ./config/* ${USER}@${IP}:/config
	# ssh ${USER}@${IP} "sudo cp -r ./config/* /config/ \
	# 							&& ./scripts/check-config.sh"

get-config:
	scp -rp ${USER}@${IP}:/config/* ./config

tail-logs:
	ssh ${USER}@${IP} "hassio homeassistant logs"

restart-hass:
	ssh ${USER}@${IP} "hassio homeassistant restart"

upgrade-hass:
	ssh ${USER}@${IP} "hassio homeassistant restart"

install-app-daemon:
	ssh ${USER}@${IP} "./scripts/install-app-daemon.sh"

secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

put-authorized-keys:
	scp ~/.ssh/id_rsa.pub ${USER}@${IP}:/home/pi
	ssh ${USER}@${IP} "mkdir -p ~/.ssh \
									&& mv ./id_rsa.pub ~/.ssh/authorized_keys \
									&& chmod 600 ~/.ssh/authorized_keys"


setup-new-hass: secrets put-authorized-keys put-config upgrade-hass install-dependencies install-app-daemon

reset-nest:
	ssh ${USER}@${IP} "sudo rm /home/homeassistant/.homeassistant/nest.con"
