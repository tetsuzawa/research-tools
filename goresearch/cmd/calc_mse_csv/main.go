package main

import (
	"flag"
	"fmt"
	"gonum.org/v1/gonum/floats"
	"math"
	"path/filepath"

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

	ds, ys, es := goresearch.ReadDataFromCSV(inputPath)

	var mse = make([]float64, len(es)-tap)
	var v float64
	var err error
	for i := 0; i < len(es)-tap; i++ {

		fmt.Printf("working... %d%%\r", (i+1)*100/(len(es)-tap))

		v, err = goresearch.MSE(es[i:i+tap], nil)
		check(err)
		mse[i] = 20 * math.Log10(v)
	}
	floats.AddConst(-1*floats.Max(mse), mse)

	name, _ := goresearch.SplitPathAndExt(inputPath)
	outputName := filepath.Base(name) + "_mse"

	goresearch.SaveDataAsCSV(ds, ys, es, mse, dataDir, outputName)

}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
