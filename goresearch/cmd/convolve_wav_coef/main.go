package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/tetsuzawa/research-tools/goresearch"
)

func main() {
	var (
		wavPath  string
		coefPath string
		dataDir  string
	)

	flag.StringVar(&wavPath, "wav", "", "wav path")
	flag.StringVar(&coefPath, "coef", "", "coefficients path (.wav or .csv)")
	flag.StringVar(&dataDir, "dir", "./", "save dir")

	flag.Parse()

	if wavPath == "" {
		fmt.Printf("please specify wav path\n\n")
		flag.Usage()
		os.Exit(1)
	}

	if coefPath == "" {
		fmt.Printf("please specify coef path\n\n")
		flag.Usage()
		os.Exit(1)
	}

	name, ext := goresearch.SplitPathAndExt(wavPath)
	if ext != ".wav" {
		fmt.Printf("please specify wav path\n\n")
		flag.Usage()
		os.Exit(1)
	}

	fmt.Println("wavPath:", wavPath)
	fmt.Println("coefPath:", coefPath)
	fmt.Println("dataDir:", dataDir)

	wData := goresearch.ReadDataFromWav(wavPath)

	_, cExt := goresearch.SplitPathAndExt(coefPath)
	var cData []float64
	switch cExt {
	case ".wav":
		cData = goresearch.IntsToFloat64s(goresearch.ReadDataFromWav(coefPath))
	case ".csv":
		cData = goresearch.ReadCoefFromCSV(coefPath)
	default:
		fmt.Printf("file type is not valid. coefficients file name:%v", coefPath)
		os.Exit(1)
	}

	wDataF := goresearch.IntsToFloat64s(wData)
	convData := goresearch.FastConvolve(wDataF, cData)

	outputName := filepath.Base(name) + "_convoluted"

	data := goresearch.NormToMaxInt16(convData)

	goresearch.SaveDataAsWav(data, dataDir, outputName)

}
