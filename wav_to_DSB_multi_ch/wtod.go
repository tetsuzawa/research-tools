package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"github.com/takuyaohashi/go-wav"
	"github.com/urfave/cli"
	"os"
	"strconv"
)

func wtod(ctx *cli.Context, f *os.File, name string) error {
	w, err := wav.NewReader(f)
	if err != nil {
		return cli.NewExitError(err, 3)
	}

	//var data interface{}
	//data, err = w.ReadSamples(int(w.GetSubChunkSize()) / int(w.GetNumChannels()))
	//if err != nil {
	//	return cli.NewExitError(err, 3)
	//}
	//data, err := w.ReadSamples(int(w.GetSubChunkSize()) / (int(w.GetNumChannels()) * int(w.GetBitsPerSample())) * 8)

	ch := int(w.GetNumChannels())
	bps := int(w.GetBlockAlign())
	//bps = 4
	//bps * ch = 8
	//omotteta bps * ch = 4
	//bps / ch = 2

	//data, err := w.ReadSamples(int(w.GetSubChunkSize()) / (bps * ch))
	data, err := w.ReadSamples(int(w.GetSubChunkSize()) / bps)
	if err != nil {
		return cli.NewExitError(err, 3)
	}

	//if reflect.TypeOf(data) != reflect.TypeOf([]int16{0,}) {
	//	return cli.NewExitError(err, 4)
	//}
	value, ok := data.([]int16)
	if !ok {
		return cli.NewExitError("bits per sample is incorrect. need 16 bits per sample", 5)
	}

	//b := make([]byte, 2)

	iter := len(value) / ch
	b := new(bytes.Buffer)
	buf := make([]byte, iter*bps)
	fmt.Println(bps)

	for j := 0; j < ch; j++ {
		fw, err := os.Create(fmt.Sprintf("%s_%s.DSB", name, strconv.Itoa(j)))
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		defer fw.Close()

		for i := 0; i < iter; i++ {
			fmt.Printf("working... %d%%\r", (i+1)*100/iter)
			err = binary.Write(b, binary.LittleEndian, value[ch*i+j])
			if err != nil {
				return cli.NewExitError(err, 5)
			}
			copy(buf[bps*i:bps*i+bps], b.Bytes())
		}

		_, err = fw.Write(buf)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
	}
	fmt.Printf("\n\n")
	fmt.Println("end!!")

	return nil
}
