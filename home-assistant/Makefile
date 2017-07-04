IP=			192.168.0.35
USER=		pi
PASS=		raspberry

get-config: pass-to-clipboard
	scp ${USER}@${IP}:/home/homeassistant/.homeassistant/*.yaml ./config

put-config: pass-to-clipboard
	scp -rp ./ ${USER}@${IP}:/home/pi/
	ssh ${USER}@${IP} "./scripts/put-config.sh"

restart-hass: pass-to-clipboard
	ssh ${USER}@${IP} "sudo systemctl restart home-assistant@homeassistant.service"

tail-logs: pass-to-clipboard
	ssh ${USER}@${IP} "tail -f /home/homeassistant/.homeassistant/home-assistant.log"

make secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

upgrade-hass: pass-to-clipboard
	ssh ${USER}@${IP} "./scripts/upgrade-hass.sh"

pass-to-clipboard:
	echo ${PASS} | pbcopy
