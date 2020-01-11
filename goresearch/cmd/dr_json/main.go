package main

import (
	"encoding/json"
	"flag"
	"fmt"
	research "github.com/tetsuzawa/go-research/ADF/automatic_equalizer"
	"os"
	"path/filepath"
)

func main() {
	var (
		wavName string
		adfName string
		L       int
		Mu      float64
		order   int
		dataDir string
	)

	flag.StringVar(&wavName, "wav", "../wavfiles/dr_static_20.wav", "wav name")
	flag.StringVar(&adfName, "adf", "NLMS", "algorithm")
	flag.Float64Var(&Mu, "mu", 1.0, "mu")
	flag.IntVar(&L, "L", 256, "L")
	flag.IntVar(&order, "order", 8, "order")
	flag.StringVar(&dataDir, "dir", "./", "save dir")

	flag.Parse()

	fmt.Println("wavName:", wavName)
	fmt.Println("adfName:", adfName)
	fmt.Println("mu:", Mu)
	fmt.Println("L:", L)
	fmt.Println("order:", order)
	fmt.Println("dataDir:", dataDir)

	var testName string
	applicationName := "static"

	switch adfName {
	case "LMS":
		testName = fmt.Sprintf("%v_%v_L-%v", adfName, applicationName, L)
	case "NLMS":
		testName = fmt.Sprintf("%v_%v_L-%v", adfName, applicationName, L)
	case "AP":
		testName = fmt.Sprintf("%v_%v_L-%v_order-%v", adfName, applicationName, L, order)
	case "RLS":
		testName = fmt.Sprintf("%v_%v_L-%v", adfName, applicationName, L)
	default:
		err := fmt.Errorf("\nadfName is not valid:%v\n", adfName)
		fmt.Println(err)
		fmt.Printf("Failed!\n")
		os.Exit(1)
	}
	fmt.Printf("testName: %v\n", testName)

	var adf = &research.OptStepADF{
		WavName: wavName,
		AdfName: adfName,
		Mu:      Mu,
		L:       L,
		Order:   order,
	}

	outadfJSON, err := json.Marshal(adf)
	check(err)
	fw, err := os.Create(filepath.Join(dataDir, testName+".json"))
	check(err)
	defer fw.Close()
	_, err = fw.Write(outadfJSON)
	check(err)

	fmt.Printf("json file saved at :%v\n", filepath.Join(dataDir, testName+".json"))

}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
