package main

import (
	"encoding/binary"
	"fmt"
	"os"
	"reflect"

	"github.com/takuyaohashi/go-wav"
	"github.com/tetsuzawa/converter"
	"github.com/urfave/cli"
)

func wtod(f *os.File, name string) error {

	w, err := wav.NewReader(f)
	if err != nil {
		return cli.NewExitError(err, 3)
	}

	var data interface{}
	data, err = w.ReadSamples(int(w.GetSubChunkSize()) / int(w.GetNumChannels()))
	if err != nil {
		return cli.NewExitError(err, 3)
	}

	if reflect.TypeOf(data) != reflect.TypeOf([]int16{0,}) {
		return cli.NewExitError(err, 4)
	}
	value, ok := data.([]int16)
	if !ok {
		return cli.NewExitError("Data type is not valid", 5)
	}

	fw, err := os.Create(name + ".DSB")
	if err != nil {
		return cli.NewExitError(err, 3)
	}
	defer fw.Close()

	b := make([]byte, 2)
	buf := make([]byte, 0)

	for i, v := range value {
		fmt.Printf("working... %d%%\r", (i+1)*100/len(value))

		ui := converter.Int16ToUint16(v)
		binary.LittleEndian.PutUint16(b, ui)
		buf = append(buf, b...)
	}
	_, err = fw.Write(buf)
	if err != nil {
		return cli.NewExitError(err, 3)
	}
	fmt.Printf("\n\n")
	fmt.Println("end!!")

	return nil
}
