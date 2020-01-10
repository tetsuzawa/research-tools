package main

import (
	"flag"
	"fmt"
	"log"
	"math"
	"os"
	"path/filepath"

	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
	"gonum.org/v1/gonum/floats"

	tools "github.com/tetsuzawa/go-research"
)

func main() {

	log.SetFlags(log.LstdFlags | log.Lshortfile)

	var (
		wavFilepath1 string
		wavFilepath2 string
		outputDir    string
	)

	flag.StringVar(&wavFilepath1, "x", "/path/to/name.wav", "designate wav file path")
	flag.StringVar(&wavFilepath2, "y", "/path/to/name.wav", "designate wav file path")
	flag.StringVar(&outputDir, "o", "/path/to/dir/", "designate ouput directory")

	flag.Parse()

	if wavFilepath1 == "/path/to/name.wav" ||
		wavFilepath2 == "/path/to/name.wav" ||
		outputDir == "/path/to/dir/" {
		flag.Usage()
		os.Exit(1)
	}

	fmt.Println("wav 1 file path:", wavFilepath1)
	fmt.Println("wav 2 file path:", wavFilepath2)
	fmt.Println("ouput directory:", outputDir)

	f1, err := os.Open(wavFilepath1)
	check(err)
	w1 := wav.NewDecoder(f1)

	f2, err := os.Open(wavFilepath2)
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

	amp1 := tools.IntsToFloat64s(buf1.Data)
	amp2 := tools.IntsToFloat64s(buf2.Data)

	amp_out := tools.Convolve(amp1, amp2)

	var (
		fw         *os.File
		ww         *wav.Encoder
		wBuf       = new(audio.IntBuffer)
		outputName string
		outputPath string
	)

	wBuf.Format = &audio.Format{
		NumChannels: ch1,
		SampleRate:  fs1,
	}
	wBuf.SourceBitDepth = bitDepth1

	maxAmp := floats.Max(tools.AbsFloat64s(amp_out))
	if maxAmp > math.MaxInt16+1 {
		reductionRate := math.MaxInt16 / maxAmp
		for i, _ := range amp_out {
			amp_out[i] *= reductionRate
		}
	}

	wBuf.Data = tools.Float64sToInts(amp_out)
	//dataCopy := make([]int, len(wBuf.Data))
	//copy(dataCopy, wBuf.Data)
	//sort.Ints(AbsInts(dataCopy))
	//log.Println("Clip judge!!")
	//if dataCopy[0] < math.MinInt16 || dataCopy[len(dataCopy)-1] > math.MaxInt16 {
	//	log.Fatalln("Clip!!")
	//}

	outputName, _ = tools.SplitPathAndExt(wavFilepath1)
	outputPath = filepath.Join(outputDir, filepath.Base(outputName)+".wav")
	fw, err = os.Create(outputPath)
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
