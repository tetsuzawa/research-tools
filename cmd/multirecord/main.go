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
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/gordonklaus/portaudio"
	"github.com/pkg/errors"
	"github.com/tetsuzawa/go-wav"
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

const (
	FramesPerBuffer = 1024
)

var w1 *wav.Writer
var RecordSeconds float64
var NumChannels int
var SampleRate int
var BitsPerSample int
var NumSamplesToWrite int
var NumWritten int
var err error

func multiRecord(ctx *cli.Context) error {
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError(`too few arguments. need recording duration.
								Usage: multirecord (-c ch -r rate -b bits -o /path/to/out.wav) duration
								`, 2)
	}

	name, ext := splitPathAndExt(ctx.String("o"))
	if ext != ".wav" {
		return cli.NewExitError(`incorrect file format. multirecord saves audio as .wav file.
											Usage: multirecord -o /path/to/file.wav 5.0`, 2)
	}
	RecordSeconds, err = strconv.ParseFloat(ctx.Args().Get(0), 64)
	if err != nil {
		err = errors.Wrap(err, "error occurred while converting arg of recording time from string to float64")
		return cli.NewExitError(err, 5)
	}
	NumChannels = ctx.Int("c")
	SampleRate = ctx.Int("r")
	BitsPerSample := ctx.Int("b")
	if BitsPerSample != 16 {
		return cli.NewExitError(`sorry, this app is only for 16 bits per sample for now`, 99)
	}
	NumSamplesToWrite = int(RecordSeconds * float64(SampleRate))

	fmt.Printf("\nOutput File: \t`%s`\n", name+".wav")
	fmt.Printf("Channels: \t%d \n", NumChannels)
	fmt.Printf("Sample Rate: \t%d\n", SampleRate)
	fmt.Printf("Precision: \t%d-bits\n", BitsPerSample)
	fmt.Printf("Duration: \t%f [sec] = %d samples\n", RecordSeconds, NumSamplesToWrite)
	fmt.Printf("Encoding: \t%d-bits Signed Integer PCM\n\n", BitsPerSample)

	f1, err := os.Create(name + ".wav")
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while creating output file")
		return cli.NewExitError(err, 5)
	}
	defer f1.Close()

	err = portaudio.Initialize()
	defer portaudio.Terminate()
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while initializing portaudio")
		return cli.NewExitError(err, 5)
	}

	h, err := portaudio.DefaultHostApi()
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while searching host API")
		return cli.NewExitError(err, 5)
	}
	paParam := portaudio.LowLatencyParameters(h.DefaultInputDevice, h.DefaultOutputDevice)
	paParam.Input.Channels = NumChannels
	paParam.Output.Channels = 1
	paParam.FramesPerBuffer = FramesPerBuffer

	if ctx.Bool("p") {
		fmt.Printf("\nFrames Per Buffer\n", paParam.FramesPerBuffer)

		fmt.Printf("\nInput Device Parameters\n")
		fmt.Printf("Input Device Name\t\t\t%v\n", paParam.Input.Device.Name)
		fmt.Printf("Input Device MaxInputChannels\t\t%v\n", paParam.Input.Device.MaxInputChannels)
		fmt.Printf("Input Device DefaultSampleRate\t\t%v\n", paParam.Input.Device.DefaultSampleRate)
		fmt.Printf("Input Device HostApi\t\t\t%v\n", paParam.Input.Device.HostApi)
		fmt.Printf("Input Device DefaultLowInputLatency\t%v\n", paParam.Input.Device.DefaultLowInputLatency)
		fmt.Printf("Input Device DefaultHighInputLatency\t%v\n", paParam.Input.Device.DefaultHighInputLatency)

		fmt.Printf("\n\nOutput params\n")
		fmt.Printf("Output Device Name\t\t\t%v\n", paParam.Output.Device.Name)
		fmt.Printf("Output Device MaxOutputChannels\t\t%v\n", paParam.Output.Device.MaxOutputChannels)
		fmt.Printf("Output Device DefaultSampleRate\t\t%v\n", paParam.Output.Device.DefaultSampleRate)
		fmt.Printf("Output Device HostApi\t\t\t%v\n", paParam.Output.Device.HostApi)
		fmt.Printf("Output Device DefaultLowOutputLatency\t%v\n", paParam.Output.Device.DefaultLowOutputLatency)
		fmt.Printf("Output Device DefaultHighOutputLatency\t%v\n", paParam.Output.Device.DefaultHighOutputLatency)

	}

	//open strea
	stream, err := portaudio.OpenStream(paParam, callback)
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while opening stream on portaudio")
		return cli.NewExitError(err, 5)
	}
	defer stream.Close()

	//make input.wav
	p := wav.WriterParam{
		SampleRate:    uint32(SampleRate),
		BitsPerSample: uint16(BitsPerSample),
		NumChannels:   uint16(NumChannels),
		AudioFormat:   1,
	}
	w1, err = wav.NewWriter(f1, p)
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while creating wav writer")
		return cli.NewExitError(err, 5)
	}
	defer w1.Close()

	err = stream.Start()
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while starting stream")
		return cli.NewExitError(err, 5)
	}

	fmt.Printf("\nrecording...\n")

	st := time.Now()
	for time.Since(st).Seconds() < RecordSeconds {
		fmt.Printf("%.1f[sec] : %.1f[sec]\r", time.Since(st).Seconds(), RecordSeconds)
	}
	err = stream.Stop()
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while stopping stream")
		return cli.NewExitError(err, 5)
	}

	fmt.Printf("\n\nSuccessfully recorded!!\n")

	return nil
}

func callback(inBuf, outBuf []int16) {
	if NumWritten+FramesPerBuffer > NumSamplesToWrite {
		numWrite := NumSamplesToWrite - NumWritten
		NumWritten += numWrite
		w1.WriteSamples(inBuf[:numWrite])
		return
	}
	NumWritten += len(inBuf) / NumChannels
	w1.WriteSamples(inBuf)
}
