.PHONY: build
build:
#	go build -o build/$(BIN_NAME)  -ldflags '-s -w' .
	go build -o bin/$(BIN_NAME) .


.PHONY: install
install:
	go install

.PHONY: test
test:
	go test -cover -v -race
