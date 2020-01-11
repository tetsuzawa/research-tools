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
	"bytes"
	"encoding/binary"
	"fmt"
	"os"

	"github.com/go-audio/wav"
	"github.com/pkg/errors"
	"github.com/urfave/cli"
)

func wavToDSB(ctx *cli.Context, name string) error {

	// ************* create output file *************
	f, err := os.Open(name + ".wav")
	if err != nil {
		err = errors.Wrap(err, "internal error: error occurred while creating output file")
		return cli.NewExitError(err, 5)
	}
	defer f.Close()
	w := wav.NewDecoder(f)
	if err != nil {
		err = errors.Wrap(err, "error occurred while processing .wav file")
		return cli.NewExitError(err, 3)
	}

	// ************* validate parameter *************
	w.ReadInfo()
	ch := int(w.NumChans)
	byteRate := int(w.BitDepth/8) * ch
	bps := byteRate / ch
	fs := int(w.SampleRate)

	if fs != 48000 || bps != 2 || w.WavAudioFormat != 1 {
		errMsg := fmt.Sprintf(`audio format error: wav format must be as follows.
sample rate: want 48000 Hz, got %v Hz
sampling bit rate: want 16 bits per sample, got %v bits per sample
audio format: want 1 (PCM), got %v`, fs, w.BitDepth, w.WavAudioFormat)
		return cli.NewExitError(errMsg, 3)
	}

	aBuf, err := w.FullPCMBuffer()
	if err != nil {
		err = errors.Wrap(err, "error occurred while processing .wav file")
		return cli.NewExitError(err, 3)
	}

	if aBuf.SourceBitDepth != 16 {
		err = errors.New("sampling bit rate is incorrect. need 16 bits per sample")
		err = errors.Wrap(err, "error occurred while processing .wav file")
		return cli.NewExitError(err, 3)
	}

	iter := aBuf.NumFrames()
	wBuf := make([]byte, iter*bps)

	// ************* split channel and write to .DSB files *************
	var fw *os.File
	for j := 0; j < ch; j++ {
		if ch == 1 {
			fw, err = os.Create(fmt.Sprintf("%s.DSB", name))
		} else {
			fw, err = os.Create(fmt.Sprintf("%s_ch%d.DSB", name, j+1))
		}
		if err != nil {
			return cli.NewExitError(err, 3)
		}
		defer fw.Close()

		for i := 0; i < iter; i++ {
			fmt.Printf("converting... %d%%\r", (i+1)*100/iter)
			b := new(bytes.Buffer)
			//err = binary.Write(b, binary.LittleEndian, value[ch*i+j])
			err = binary.Write(b, binary.LittleEndian, int16(aBuf.Data[ch*i+j]))
			if err != nil {
				err = errors.Wrap(err, "internal error: error occurred while writing data to buffer")
				return cli.NewExitError(err, 5)
			}
			copy(wBuf[bps*i:bps*(i+1)], b.Bytes())
		}
		_, err = fw.Write(wBuf)
		if err != nil {
			err = errors.Wrap(err, "error occurred while writing data to .DSB file")
			return cli.NewExitError(err, 3)
		}

	}
	if ch == 1 {
		fmt.Printf("\n\n%d file created as `%s.DSB`\n", ch, name)
	} else {
		fmt.Printf("\n\n%d files created as `%s_chX.DSB`\n", ch, name)
	}

	fmt.Printf("\n")
	fmt.Println("end!!")

	return nil
}
