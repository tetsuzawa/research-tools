/*
Contents: multi channel record.
	This program works as typical recording app with multi channels.
	Output file format is .wav.
	Please run `multirecord --help` for details.
Usage: multirecord (-c num_ch -r sample_rate -b bits_per_sample -o /path/to/out.wav) 5
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
	app.Usage = `This app records sounds with multi channels and save as .wav file.`
	app.Version = "0.0.1"

	app.Action = multiRecord

	app.Flags = []cli.Flag{
		cli.IntFlag{
			Name:  "channel, c",
			Value: 1,
			Usage: "specify input numver of channels like as `-c 2`",
		},
		cli.IntFlag{
			Name:  "bits, b",
			Value: 16,
			Usage: "specify number of bits per sample like as `-b 16`",
		},
		cli.IntFlag{
			Name:  "rate, r",
			Value: 48000,
			Usage: "specify number of sample rate like as `-r 48000`",
		},
		cli.StringFlag{
			Name:  "outpath, o",
			Value: "out_multirecord.wav",
			Usage: "specify output path like as `-o /path/to/file`",
		},
		cli.BoolFlag{
			Name:  "params, p",
			Usage: "trace import statements",
		},
	}
}
