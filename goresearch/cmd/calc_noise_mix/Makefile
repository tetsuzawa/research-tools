BIN_NAME="calc_noise_mix"

.PHONY: build
build:
	go build -o bin/$(BIN_NAME) .


.PHONY: install
install:
	go install

.PHONY: test
test:
	go test -cover -v -race
