.PHONY: fmt
fmt:
	sh ./scripts/fmt.sh

.PHONY: lint
lint:
	sh ./scripts/lint.sh

.PHONY: install-ffmpeg
install-ffmpeg:
	python ./tools/install_ffmpeg.py
