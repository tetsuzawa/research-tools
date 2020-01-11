/*
Contents: wav to DSB converter.
	This program converts .wav file to .DSB files.
	Please run `wav_to_DSB --help` for details.
Usage: wav_to_DSB (-o /path/to/out.DSB) /path/to/file.wav
Author: Tetsu Takizawa
E-mail: tt15219@tomakomai.kosen-ac.jp
LastUpdate: 2019/11/16
DateCreated  : 2019/11/16
*/
package main

import (
	"os"

	"github.com/pkg/errors"
	"github.com/urfave/cli"
)

func main() {
	app := cli.NewApp()
	defer app.Run(os.Args)
	app.CustomAppHelpTemplate = HelpTemplate

	app.Name = "wav_to_DSB"
	app.Usage = `This app converts .wav file to .DSB file.`
	app.Version = "0.1.0"

	app.Action = action

	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name:  "outpath, o",
			Usage: "specify output path like as /path/to/file",
		},
	}
}

func action(ctx *cli.Context) error {
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError("too few arguments. need input file path. \nUsage: wav-to-DSB-multi /path/to/file.wav", 2)
	}

	fileName := ctx.Args().Get(0)
	name, ext := splitPathAndExt(fileName)

	if ext != ".wav" {
		return cli.NewExitError("incorrect file format. need .wav file. \nUsage: wav-to-DSB-multi /path/to/file.wav", 2)
	}

	if ctx.String("o") != "" {
		argName := ctx.String("o")
		name, _ = splitPathAndExt(argName)
	}

	f, err := os.Open(fileName)
	if err != nil {
		err = errors.Wrap(err, "error occurred while opening input file")
		return cli.NewExitError("no such a file", 2)
	}
	defer f.Close()

	return wavToDSB(ctx, f, name)
}
