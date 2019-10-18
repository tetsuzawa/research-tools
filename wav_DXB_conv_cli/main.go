package main

import (
	"encoding/binary"
	"fmt"
	"github.com/takuyaohashi/go-wav"
	"github.com/urfave/cli"
	"io/ioutil"
	"os"
	"reflect"
	"strings"
)

type Data interface {
}

func main() {
	app := cli.NewApp()
	defer app.Run(os.Args)

	app.Name = "WavDXBConverter"
	app.Usage = "This app convert .wav file to .DXB file or .DXB to .wav file"
	app.Version = "0.0.1"

	app.Action = action

	app.Flags = []cli.Flag{
		cli.BoolFlag{
			Name:  "conv, c",
			Usage: "convert .wav to .DXB",
		},
	}
}

func action(ctx *cli.Context) error {
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError("Too few arguments. Need input file name", 2)
	}

	fileName := ctx.Args().Get(0)
	nameParts := strings.Split(fileName, ".")
	name, ex := nameParts[0], nameParts[1]

	f, err := os.Open(fileName)
	if err != nil {
		return cli.NewExitError("No such a file", 2)
	}
	defer f.Close()

	var data interface{}

	switch ex {
	case "wav":
		w, err := wav.NewReader(f)
		//w, err := wav2.New(f)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		data, err = w.ReadSamples(int(w.GetSubChunkSize()) / int(w.GetNumChannels()))
		//sc := w.GetSubChunkSize()
		//fmt.Println(sc)
		//data, err = w.ReadSamples(1024)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		//fmt.Printf("%T, %v\n", data)
		if reflect.TypeOf(data) != reflect.TypeOf([]int16{0,}) {
			return cli.NewExitError(err, 4)
		}
		fmt.Println("name: ", name)
		fmt.Println("type: ", reflect.TypeOf(data))
		fmt.Println("ex: ", ex)
		if value, ok := data.([]int16); ok {

			fw, err := os.Create(name + ".DSB")
			if err != nil {
				return cli.NewExitError(err, 3)
			}
			fmt.Println("len of value: ", len(value))
			defer fw.Close()

			buf := make([]byte, 0)
			//buf := make([]byte, 2*len(value))

			for i, v := range value {
				fmt.Printf("working... %d%%\r", (i+1)*100/len(value))

				b := make([]byte, 2)
				ui := Int16ToUint16(v)
				binary.LittleEndian.PutUint16(b, ui)
				//buf[i*2 : i*2+2] = b...
				buf = append(buf, b...)
			}
			_, err = fw.Write(buf)
			if err != nil {
				return cli.NewExitError(err, 3)
			}
		}
		fmt.Printf("\n\n")
		fmt.Println("end!!")

	case "DSB":
		buff, err := ioutil.ReadAll(f)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		data := bytesToInt16s(buff)
		fmt.Println(data)

	case "DDB":
		buff, err := ioutil.ReadAll(f)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		data := bytesToFloat64s(buff)
		fmt.Println(data)
	default:
		return cli.NewExitError("Unknown extention. Want: .wav, .DSB or .DDB. Got: "+ex, 2)
	}
	//fmt.Println(data)

	return nil
}
