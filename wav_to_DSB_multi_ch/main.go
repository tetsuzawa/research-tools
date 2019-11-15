package main

import (
	"fmt"
	"github.com/urfave/cli"
	"os"
)

type Data interface {
}

func main() {
	app := cli.NewApp()
	defer app.Run(os.Args)

	app.Name = "WavDSBConverter"
	app.Usage = "this app converts .wav file to .DSB file"
	app.Version = "0.0.1"

	app.Action = action

	app.Flags = []cli.Flag{
		//cli.IntFlag{
		//	Name:  "channel, c",
		//	Usage: "output channel num",
		//	Value: 1,
		//},
		cli.StringFlag{
			Name:  "outname, o",
			Usage: "designate output file name",
		},
	}
}

func action(ctx *cli.Context) error {
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError("too few arguments. need input file path", 2)
	}

	fileName := ctx.Args().Get(0)
	fmt.Println("filename: ", fileName)
	//nameParts := strings.Split(fileName, ".")
	name, ext := splitFilePath(fileName)
	fmt.Println(name, ext)

	if ext != ".wav" {
		return cli.NewExitError("incorrect file format. need .wav file", 2)
	}

	fmt.Println("ctx: ", ctx.Int("channel"), "outname: ", ctx.String("outname"))

	if ctx.String("o") != "" {
		name = ctx.String("o")
	}
	//ex := nameParts[1]

	f, err := os.Open(fileName)
	if err != nil {
		return cli.NewExitError("No such a file", 2)
	}
	defer f.Close()

	return wtod(ctx, f, name)
}
