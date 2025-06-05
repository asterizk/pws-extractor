.PHONY: run clean config install uninstall

PLUGIN_NAME = swiftbar-pws-precip.5m.py
PLUGIN_DIR = $(HOME)/Library/Application\ Support/SwiftBar/Plugins

run:
	python3 $(PLUGIN_NAME)

clean:
	rm -rf __pycache__ *.pyc

config:
	cp weather.conf.example weather.conf

install:
	mkdir -p "$(PLUGIN_DIR)"
	ln -sf "$(PWD)/$(PLUGIN_NAME)" "$(PLUGIN_DIR)/$(PLUGIN_NAME)"

uninstall:
	rm -f "$(PLUGIN_DIR)/$(PLUGIN_NAME)"
