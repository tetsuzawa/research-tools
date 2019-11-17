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

	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
	"github.com/gordonklaus/portaudio"
	"github.com/pkg/errors"
	"github.com/urfave/cli"
)

const (
	FramesPerBuffer = 1024
	PCM             = 1
)

var (
	w1                *wav.Encoder
	RecordSeconds     float64
	NumChannels       int
	SampleRate        int
	BitsPerSample     int
	NumSamplesToWrite int
	NumWritten        int
	aBuf              = new(audio.IntBuffer)
	err               error
)

func multiRecord(ctx *cli.Context) error {
	// ************* check argument *************
	if ctx.Args().Get(0) == "" {
		return cli.NewExitError(`too few arguments. need recording duration.
								Usage: multirecord (-c ch -r rate -b bits -o /path/to/out.wav) duration
								`, 2)
	}

	// ************* ext validation *************
	name, ext := splitPathAndExt(ctx.String("o"))
	if ext != ".wav" {
		return cli.NewExitError(`incorrect file format. multirecord saves audio as .wav file.
											Usage: multirecord -o /path/to/file.wav 5.0`, 2)
	}

	// ************* parameter validation *************
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

	// ************* output file creation *************
	f1, err := os.Create(name + ".wav")
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while creating output file")
		return cli.NewExitError(err, 5)
	}
	defer f1.Close()

	w1 = wav.NewEncoder(f1, SampleRate, BitsPerSample, NumChannels, PCM)
	aBuf.Format = &audio.Format{
		NumChannels: NumChannels,
		SampleRate:  SampleRate,
	}
	aBuf.SourceBitDepth = BitsPerSample

	// ************* portaudio initialization *************
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
	paParam.SampleRate = float64(SampleRate)
	paParam.Input.Channels = NumChannels
	paParam.Output.Channels = 1
	paParam.FramesPerBuffer = FramesPerBuffer

	stream, err := portaudio.OpenStream(paParam, callback)
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while opening stream on portaudio")
		return cli.NewExitError(err, 5)
	}
	defer stream.Close()

	// ************* parameter expression *************
	fmt.Printf("\nOutput File: \t`%s`\n", name+".wav")
	fmt.Printf("Channels: \t%d \n", NumChannels)
	fmt.Printf("Sample Rate: \t%d\n", SampleRate)
	fmt.Printf("Precision: \t%d-bits\n", BitsPerSample)
	fmt.Printf("Duration: \t%f [sec] = %d samples\n", RecordSeconds, NumSamplesToWrite)
	fmt.Printf("Encoding: \t%d-bits Signed Integer PCM\n\n", BitsPerSample)

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

	// ************* recording *************
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
	err = w1.Close()
	check(err)

	fmt.Printf("\n\nSuccessfully recorded!!\n")

	return nil
}

// ************* callback function *************
func callback(inBuf, outBuf []int16) {
	if NumWritten+FramesPerBuffer > NumSamplesToWrite {
		numWrite := NumSamplesToWrite - NumWritten
		NumWritten += numWrite
		aBuf.Data = int16sToInts(inBuf[:numWrite])
		err = w1.Write(aBuf)
		check(err)
		return
	}
	NumWritten += len(inBuf) / NumChannels
	aBuf.Data = int16sToInts(inBuf)
	err = w1.Write(aBuf)
	check(err)
}
