.PHONY: check install release

check:
	plutil -lint 'Nickel.bbpackage/Contents/Language Modules/Nickel.plist'
	python3 -m unittest discover -s tests -v

install:
	./scripts/install.sh

release: check
	mkdir -p dist
	python3 scripts/release.py
