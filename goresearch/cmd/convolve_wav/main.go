package main

import (
	"flag"
	"fmt"
	"log"
	"math"
	"os"

	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
	"gonum.org/v1/gonum/floats"

	"github.com/tetsuzawa/research-tools/goresearch"
)

func main() {

	log.SetFlags(log.LstdFlags | log.Lshortfile)

	var (
		inputFilePath1 string
		inputFilePath2 string
		outputFilePath string
	)

	flag.StringVar(&inputFilePath1, "x", "/path/to/name.wav", "designate input wav file path")
	flag.StringVar(&inputFilePath2, "y", "/path/to/name.wav", "designate input wav file path")
	flag.StringVar(&outputFilePath, "o", "/path/to/name.wav", "designate output wav file path")

	flag.Parse()

	if inputFilePath1 == "/path/to/name.wav" ||
		inputFilePath2 == "/path/to/name.wav" ||
		outputFilePath == "/path/to/name.wav" {
		flag.Usage()
		os.Exit(1)
	}

	fmt.Println("wav_1 file path:", inputFilePath1)
	fmt.Println("wav_2 file path:", inputFilePath2)
	fmt.Println("output file path:", outputFilePath)

	f1, err := os.Open(inputFilePath1)
	check(err)
	w1 := wav.NewDecoder(f1)

	f2, err := os.Open(inputFilePath2)
	check(err)
	w2 := wav.NewDecoder(f2)

	w1.ReadInfo()
	w2.ReadInfo()
	ch1 := int(w1.NumChans)
	ch2 := int(w2.NumChans)
	bitDepth1 := int(w1.BitDepth)
	bitDepth2 := int(w2.BitDepth)
	bps1 := bitDepth1 / 8
	bps2 := bitDepth2 / 8
	fs1 := int(w1.SampleRate)
	fs2 := int(w2.SampleRate)

	buf1, err := w1.FullPCMBuffer()
	check(err)
	buf2, err := w2.FullPCMBuffer()
	check(err)

	err = f1.Close()
	check(err)
	err = f2.Close()
	check(err)

	if ch1 != ch2 ||
		bitDepth1 != bitDepth2 ||
		bps1 != bps2 ||
		fs1 != fs2 {
		err = fmt.Errorf("format of wav files are not agree")
		panic(err)
	}

	amp1 := goresearch.IntsToFloat64s(buf1.Data)
	amp2 := goresearch.IntsToFloat64s(buf2.Data)

	ampOut := goresearch.Convolve(amp1, amp2)

	var (
		fw             *os.File
		ww             *wav.Encoder
		wBuf           = new(audio.IntBuffer)
		outputFileName string
		outputPath_1   string
	)

	wBuf.Format = &audio.Format{
		NumChannels: ch1,
		SampleRate:  fs1,
	}
	wBuf.SourceBitDepth = bitDepth1

	maxAmp := floats.Max(goresearch.AbsFloat64s(ampOut))
	if maxAmp > math.MaxInt16+1 {
		reductionRate := math.MaxInt16 / maxAmp
		for i, _ := range ampOut {
			ampOut[i] *= reductionRate
		}
	}

	wBuf.Data = goresearch.Float64sToInts(ampOut)

	outputFileName, _ = goresearch.SplitPathAndExt(outputFilePath)

	outputPath_1 = outputFileName + ".wav"
	fw, err = os.Create(outputPath_1)
	check(err)
	ww = wav.NewEncoder(fw, fs1, bitDepth1, ch1, 1)
	err = ww.Write(wBuf)
	check(err)
	err = ww.Close()
	check(err)

	fmt.Printf("\nSuccessfully calcurated convolution! \n")
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
