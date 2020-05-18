SHELL=/bin/bash

.PHONY: build
build:
	PWD=$(pwd)
	BIN_NAME=$(basename ${PWD})
	go build -o bin/$(BIN_NAME) .


.PHONY: install
install:
	go install

.PHONY: test
test:
	go test -cover -v -race
