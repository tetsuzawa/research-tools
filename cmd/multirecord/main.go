/*
Contents: multi channel record.
	This program works as typical recording app with multi channels.
	Output file format is .wav.
	Please run `multirecord --help` for details.
Usage: multirecord (-c ch -r rate -b bits -o /path/to/out.wav) sec
Author: Tetsu Takizawa
E-mail: tt15219@tomakomai.kosen-ac.jp
LastUpdate: 2019/11/18
DateCreated  : 2019/11/18
*/
package main

import (
	"os"

	"github.com/urfave/cli"
)

func main() {
	app := cli.NewApp()
	defer app.Run(os.Args)
	app.CustomAppHelpTemplate = HelpTemplate

	app.Name = "multirecord"
	app.Usage = `This app records sounds with multi channels and save as .wav file or .DSB files if --DSB is specified.`
	app.Version = "0.1.2"

	app.Action = multiRecord

	app.Flags = []cli.Flag{
		cli.IntFlag{
			Name:  "channel, c",
			Value: 1,
			Usage: "input number of channels",
		},
		cli.IntFlag{
			Name:  "bits, b",
			Value: 16,
			Usage: "number of bits per sample",
		},
		cli.IntFlag{
			Name:  "rate, r",
			Value: 48000,
			Usage: "number of sample rate",
		},
		cli.StringFlag{
			Name:  "outpath, o",
			Value: "out_multirecord.wav",
			Usage: "specify output path",
		},
		cli.BoolFlag{
			Name:  "params, p",
			Usage: "trace import statements",
		},
		cli.BoolFlag{
			Name:  "DSB, D",
			Usage: "make .DSB files",
		},
	}
}
