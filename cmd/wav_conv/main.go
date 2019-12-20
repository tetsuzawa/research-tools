package main

import (
	"flag"
	"fmt"
	research "github.com/tetsuzawa/go-research/ADF/automatic_equalizer"
	"github.com/tetsuzawa/go-research/tools"
	"os"
	"path/filepath"
)

func main()  {
	var (
		wavPath string
		coefPath string
		dataDir string
	)

	flag.StringVar(&wavPath, "wav", "", "wav path")
	flag.StringVar(&coefPath, "coef", "", "coefficients path (.wav or .csv)")
	flag.StringVar(&dataDir, "dir", "./", "save dir")

	flag.Parse()

	if wavPath == ""{
		fmt.Printf("please specify wav path\n\n")
		flag.Usage()
		os.Exit(1)
	}

	if coefPath == ""{
		fmt.Printf("please specify coef path\n\n")
		flag.Usage()
		os.Exit(1)
	}

	name, ext := tools.SplitPathAndExt(wavPath)
	if ext != ".wav"{
		fmt.Printf("please specify wav path\n\n")
		flag.Usage()
		os.Exit(1)
	}


	fmt.Println("wavPath:", wavPath)
	fmt.Println("coefPath:", coefPath)
	fmt.Println("dataDir:", dataDir)

	wData := tools.ReadDataFromWav(wavPath)

	_, cExt := tools.SplitPathAndExt(coefPath)
	var cData []float64
	switch cExt {
	case ".wav":
		cData = tools.IntsToFloat64s(tools.ReadDataFromWav(coefPath))
	case ".csv":
		cData = tools.ReadCoefFromCSV(coefPath)
	default:
		fmt.Printf("file type is not valid. coefficients file name:%v", coefPath)
		os.Exit(1)
	}

	wDataF := tools.IntsToFloat64s(wData)
	convData := research.Convolve(wDataF, cData)

	outputName := filepath.Base(name) + "_conv"

	data := tools.NormToMaxInt16(convData)

	tools.SaveDataToWav(data, dataDir, outputName)

}
