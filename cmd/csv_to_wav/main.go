package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/tetsuzawa/go-research/tools"
)

func main() {

	var (
		csvPath string
		dataDir string
	)

	flag.StringVar(&csvPath, "path", "", "csv path")
	flag.StringVar(&dataDir, "dir", "./", "save dir")

	flag.Parse()

	if csvPath == ""{
		fmt.Printf("please specify csv path\n\n")
		flag.Usage()
		os.Exit(1)
	}

	name, ext := tools.SplitPathAndExt(csvPath)
	if ext != ".csv"{
		fmt.Printf("please specify csv path\n\n")
		flag.Usage()
		os.Exit(1)
	}


	fmt.Println("csvPath:", csvPath)
	fmt.Println("dataDir:", dataDir)

	_, _, e := tools.ReadDataFromCSV(csvPath)

	outputName := filepath.Base(name)

	data := tools.NormToMaxInt16(e)

	tools.SaveDataToWav(data, dataDir, outputName)

}
