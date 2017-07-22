IP=			hassbian.local
USER=		pi

put-config:
	scp -rp ./ ${USER}@${IP}:/home/pi/
	ssh ${USER}@${IP} "sudo cp -r ./config/* /home/homeassistant/.homeassistant/ \
									&& sudo cp ./appdaemon/conf/*.yaml /opt/appdaemon/conf/ \
									&& ./scripts/check-config.sh"

tail-logs:
	ssh ${USER}@${IP} "tail -f /home/homeassistant/.homeassistant/home-assistant.log"

restart-hass:
	ssh ${USER}@${IP} "sudo systemctl restart home-assistant@homeassistant.service"

upgrade-hass:
	ssh ${USER}@${IP} "./scripts/upgrade-hass.sh"

install-app-daemon:
	ssh ${USER}@${IP} "./scripts/install-app-daemon.sh"

secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

put-authorized-keys:
	scp ~/.ssh/id_rsa.pub ${USER}@${IP}:/home/pi
	ssh ${USER}@${IP} "mkdir -p ~/.ssh \
									&& mv ./id_rsa.pub ~/.ssh/authorized_keys \
									&& chmod 600 ~/.ssh/authorized_keys"

get-config:
	scp ${USER}@${IP}:/home/homeassistant/.homeassistant/*.yaml ./config
	scp ${USER}@${IP}:/opt/appdaemon/conf/*.yaml ./appdaemon/conf

setup-new-hass: secrets put-authorized-keys put-config upgrade-hass install-dependencies install-app-daemon

reset-nest:
	ssh ${USER}@${IP} "sudo rm /home/homeassistant/.homeassistant/nest.con"
