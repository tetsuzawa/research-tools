package main

import (
	"fmt"
	"github.com/tetsuzawa/converter"
	"github.com/urfave/cli"
	"io/ioutil"
	"os"
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
		cli.IntFlag{
			Name:  "channel, c",
			Usage: "output channel num",
			Value: 1,
		},
		cli.StringFlag{
			Name:  "outname, o",
			Usage: "designate output file name",
		},
	}
}

func action(ctx *cli.Context) error {
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError("Too few arguments. Need input file name", 2)
	}

	fileName := ctx.Args().Get(0)
	fmt.Println("filename: ", fileName)
	nameParts := strings.Split(fileName, ".")
	var name string
	fmt.Println("ctx: ", ctx.Int("channel"), ctx.String("outname"))
	if ctx.String("o") != "" {
		name = ctx.String("o")
	} else {
		name = nameParts[0]
	}
	ex := nameParts[1]

	f, err := os.Open(fileName)
	if err != nil {
		return cli.NewExitError("No such a file", 2)
	}
	defer f.Close()

	switch ex {
	case "wav":
		return wtod(ctx, f, name)

	case "DSB":
		buff, err := ioutil.ReadAll(f)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		data := converter.BytesToInt16s(buff)
		fmt.Println(data)

	case "DDB":
		buff, err := ioutil.ReadAll(f)
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		data := converter.BytesToFloat64s(buff)
		fmt.Println(data)
	default:
		return cli.NewExitError("Unknown extention. Want: .wav, .DSB or .DDB. Got: "+ex, 2)
	}
	//fmt.Println(data)

	return nil
}
