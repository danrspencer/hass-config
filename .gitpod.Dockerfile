FROM gitpod/workspace-full

RUN apt-get install dbus-python
RUN pip3 install homeassistant


# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/
