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
	}
}

const (
	FramesPerBuffer = 1024
)

func multiRecord(ctx *cli.Context) error {
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError(`too few arguments. need recording duration.
Usage: multirecord (-c num_ch -r sample_rate -b bits_per_sample -o /path/to/out.wav) 5`, 2)
	}

	name, ext := splitPathAndExt(ctx.String("o"))
	if ext != ".wav" {
		return cli.NewExitError(`incorrect file format. multirecord saves audio as .wav file.
Usage: multirecord -o /path/to/file.wav 5.0`, 2)
	}

	RecordSeconds, err := strconv.ParseFloat(ctx.Args().Get(0), 64)
	if err != nil {
		err = errors.Wrap(err, "error occurred while converting arg of recording time from string to float64")
		return cli.NewExitError(err, 5)
	}
	fmt.Printf("Record Seconds: %.1f [sec]\n", RecordSeconds)

	NumChannels := ctx.Int("c")
	fmt.Printf("Record on %d ch\n", NumChannels)

	SampleRate := ctx.Int("r")
	fmt.Printf("Record on %d sample per sec\n", SampleRate)

	BitsPerSample := ctx.Int("b")
	if BitsPerSample != 16 {
		return cli.NewExitError(`sorry, this app is only for 16 bits per sample for now`, 99)
	}
	fmt.Printf("Record on %d sample per sec\n", BitsPerSample)

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

	//paParam := portaudio.StreamParameters{
	//	Input:  portaudio.StreamDeviceParameters{inputDevice, NumChannels, inputDevice.DefaultLowInputLatency},
	//	Output: portaudio.StreamDeviceParameters{outputDevice, NumChannels, outputDevice.DefaultLowOutputLatency},
	//	Output:          portaudio.StreamDeviceParameters{nil, 0, outputDevice.DefaultLowOutputLatency},
	//SampleRate:      float64(SampleRate),
	//FramesPerBuffer: FramesPerBuffer * NumChannels,
	//Flags:           portaudio.NoFlag,
	//}

	//////////////////////////////////

	h, err := portaudio.DefaultHostApi()
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while searching host API")
		return cli.NewExitError(err, 5)
	}
	paParam := portaudio.LowLatencyParameters(h.DefaultInputDevice, h.DefaultOutputDevice)
	paParam.Input.Channels = NumChannels
	paParam.Output.Channels = 1
	//paParam.FramesPerBuffer = FramesPerBuffer * NumChannels
	paParam.FramesPerBuffer = FramesPerBuffer

	//fmt.Println("paParam.Input.Channels", paParam.Input.Channels)
	//fmt.Println("paParam.Output.Channels", paParam.Output.Channels)
	//fmt.Println("paParam.SampleRate", paParam.SampleRate)
	//fmt.Println("paParam.FramesPerBuffer", paParam.FramesPerBuffer)
	//
	//fmt.Printf("\n\nInput params\n\n")
	//
	//fmt.Println("paParam.Input.Device.Name", paParam.Input.Device.Name)
	//fmt.Println("paParam.Input.Device.MaxInputChannels", paParam.Input.Device.MaxInputChannels)
	//fmt.Println("paParam.Input.Device.DefaultSampleRate", paParam.Input.Device.DefaultSampleRate)
	//fmt.Println("paParam.Input.Device.HostApi", paParam.Input.Device.HostApi)
	//fmt.Println("paParam.Input.Device.DefaultLowInputLatency", paParam.Input.Device.DefaultLowInputLatency)
	//fmt.Println("paParam.Input.Device.DefaultHighInputLatency", paParam.Input.Device.DefaultHighInputLatency)
	//
	//fmt.Printf("\n\nOutput params\n\n")
	//
	//fmt.Println("paParam.Output.Device.Name", paParam.Output.Device.Name)
	//fmt.Println("paParam.Output.Device.MaxOutputChannels", paParam.Output.Device.MaxOutputChannels)
	//fmt.Println("paParam.Output.Device.DefaultSampleRate", paParam.Output.Device.DefaultSampleRate)
	//fmt.Println("paParam.Output.Device.HostApi", paParam.Output.Device.HostApi)
	//fmt.Println("paParam.Output.Device.DefaultLowOutputLatency", paParam.Output.Device.DefaultLowOutputLatency)
	//fmt.Println("paParam.Output.Device.DefaultHighOutputLatency", paParam.Output.Device.DefaultHighOutputLatency)

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

	fmt.Println("recording start...")

	st := time.Now()
	for time.Since(st).Seconds() < RecordSeconds {
		fmt.Printf("%.1f[sec] : %.1f[sec]\r", time.Since(st).Seconds(), RecordSeconds)
	}
	err = stream.Stop()
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while stopping stream")
		return cli.NewExitError(err, 5)
	}

	fmt.Printf("\nrecording end\n")

	fmt.Printf("\nSuccessfully recorded!!\n")
	fmt.Printf("File saved as `%v`\n", name+".wav")

	return nil
}

var w1 *wav.Writer

//func callback(inBuf, outBuf []int16) {
func callback(inBuf, outBuf []int16) {
	w1.WriteSamples(inBuf)
}
