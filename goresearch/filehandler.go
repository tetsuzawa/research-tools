package goresearch

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
)

func ReadDataFromCSV(inputPath string) (ds []float64, ys []float64, es []float64) {
	fr, err := os.Open(inputPath)
	check(err)
	sc := bufio.NewScanner(fr)
	var ss []string
	var d float64
	var y float64
	var e float64
	for sc.Scan() {
		ss = strings.Split(sc.Text(), ",")
		d, err = strconv.ParseFloat(ss[0], 64)
		check(err)
		ds = append(ds, d)
		y, err = strconv.ParseFloat(ss[1], 64)
		check(err)
		ys = append(ys, y)
		e, err = strconv.ParseFloat(ss[2], 64)
		check(err)
		es = append(es, e)
	}
	return ds, ys, es
}

func ReadDataFromCSVOne(inputPath string, column int) (fs []float64) {
	fr, err := os.Open(inputPath)
	check(err)
	sc := bufio.NewScanner(fr)
	var ss []string
	var f float64
	for sc.Scan() {
		ss = strings.Split(sc.Text(), ",")
		f, err = strconv.ParseFloat(ss[column], 64)
		check(err)
		fs = append(fs, f)
	}
	return fs
}

func ReadCoefFromCSV(inputPath string) (ws []float64) {
	fr, err := os.Open(inputPath)
	check(err)
	sc := bufio.NewScanner(fr)
	var ss []string
	var w float64
	for sc.Scan() {
		ss = strings.Split(sc.Text(), ",")
		w, err = strconv.ParseFloat(ss[0], 64)
		check(err)
		ws = append(ws, w)
	}
	return ws
}

func ReadDataFromWav(name string) []int {
	f, err := os.Open(name)
	check(err)
	defer f.Close()
	wavFile := wav.NewDecoder(f)
	check(err)

	wavFile.ReadInfo()
	ch := int(wavFile.NumChans)
	//byteRate := int(w.BitDepth/8) * ch
	//bps := byteRate / ch
	fs := int(wavFile.SampleRate)
	fmt.Println("ch", ch, "fs", fs)

	buf, err := wavFile.FullPCMBuffer()
	check(err)
	fmt.Printf("SourceBitDepth: %v\n", buf.SourceBitDepth)

	return buf.Data
}

func SaveDataAsWav(data []float64, dataDir string, name string) {
	outputPath := filepath.Join(dataDir, name+".wav")
	fw, err := os.Create(outputPath)
	check(err)

	const (
		SampleRate    = 48000
		BitsPerSample = 16
		NumChannels   = 1
		PCM           = 1
	)

	w1 := wav.NewEncoder(fw, SampleRate, BitsPerSample, NumChannels, PCM)
	aBuf := new(audio.IntBuffer)
	aBuf.Format = &audio.Format{
		NumChannels: NumChannels,
		SampleRate:  SampleRate,
	}
	aBuf.SourceBitDepth = BitsPerSample

	aBuf.Data = Float64sToInts(data)
	err = w1.Write(aBuf)
	check(err)

	err = w1.Close()
	check(err)

	err = fw.Close()
	check(err)

	fmt.Printf("\nwav file saved at: %v\n", outputPath)
}

func SaveDataAsCSV(d, y, e, mse []float64, dataDir string, testName string) {
	n := len(d)
	fw, err := os.Create(filepath.Join(dataDir, testName+".csv"))
	check(err)
	writer := bufio.NewWriter(fw)
	for i := 0; i < n; i++ {
		if i >= len(mse) {
			_, err = fmt.Fprintf(writer, "%g,%g,%g\n", d[i], y[i], e[i])
			check(err)
			continue
		}
		_, err = fmt.Fprintf(writer, "%g,%g,%g,%g\n", d[i], y[i], e[i], mse[i])
		check(err)
	}
	err = writer.Flush()
	check(err)
	err = fw.Close()
	check(err)
}

func SaveDataAsCSVOne(fs []float64, dataDir string, testName string) {
	n := len(fs)
	fw, err := os.Create(filepath.Join(dataDir, testName+".csv"))
	check(err)
	writer := bufio.NewWriter(fw)
	for i := 0; i < n; i++ {
		_, err = fmt.Fprintf(writer, "%g\n", fs[i])
		check(err)
	}
	err = writer.Flush()
	check(err)
	err = fw.Close()
	check(err)

	fmt.Printf("output file is saved at: %v\n", testName+".csv")
}

func SplitPathAndExt(path string) (string, string) {
	return filepath.Join(filepath.Dir(filepath.Clean(path)), filepath.Base(path[:len(path)-len(filepath.Ext(path))])), filepath.Ext(path)
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
