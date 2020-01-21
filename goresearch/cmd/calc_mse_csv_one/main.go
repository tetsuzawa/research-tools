package main

import (
	"flag"
	"fmt"
	"gonum.org/v1/gonum/floats"
	"math"
	"path/filepath"
	"strconv"

	"github.com/tetsuzawa/research-tools/goresearch"
)

func main() {
	var tap int
	flag.IntVar(&tap, "tap", 256, "mse taps")
	flag.Parse()

	fmt.Println("mse taps:", tap)

	inputPath := flag.Arg(0)
	fmt.Println("inputPath:", inputPath)

	dataDir := flag.Arg(1)
	fmt.Println("dataDir:", dataDir)

	calcColumn := flag.Arg(2)
	fmt.Println("calcColumn:", calcColumn)
	calcColumnInt, err := strconv.Atoi(calcColumn)
	check(err)

	fs := goresearch.ReadDataFromCSVOne(inputPath, calcColumnInt)

	var mse = make([]float64, len(fs)-tap)
	var v float64
	for i := 0; i < len(fs)-tap; i++ {

		fmt.Printf("working... %d%%\r", (i+1)*100/(len(fs)-tap))

		v, err = goresearch.CalcMSE(fs[i:i+tap], nil)
		check(err)
		mse[i] = 20 * math.Log10(v)
	}
	floats.AddConst(-1*floats.Max(mse), mse)

	name, _ := goresearch.SplitPathAndExt(inputPath)
	outputName := filepath.Base(name) + "_mse"

	goresearch.SaveDataAsCSVOne(fs, dataDir, outputName)
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
