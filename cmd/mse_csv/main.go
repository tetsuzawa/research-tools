package main

import (
	"bufio"
	"flag"
	"fmt"
	"github.com/pkg/errors"
	"gonum.org/v1/gonum/floats"
	"math"
	"os"
	"path/filepath"
	"strconv"
	"strings"
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

	ds, ys, es := ReadDataFromCSV(inputPath)

	var mse = make([]float64, len(es)-tap)
	var v float64
	var err error
	for i := 0; i < len(es)-tap; i++ {
		v, err = MSE(es[i:i+tap], nil)
		check(err)
		mse[i] = 20 * math.Log10(v)
	}
	floats.AddConst(-1*floats.Max(mse), mse)

	name, _ := splitPathAndExt(inputPath)
	outputName := filepath.Base(name) + "_mse"

	SaveDataAsCSV(ds, ys, es, mse, dataDir, outputName)

}

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

func MSE(a []float64, b []float64) (float64, error) {
	if b == nil {
		b = make([]float64, len(a))
	} else if len(a) != len(b) {
		return 0, errors.New("length of a and b must agree")
	}
	var sum float64
	for i := 0; i < len(a); i++ {
		sum += (a[i] - b[i]) * (a[i] - b[i])
	}

	return sum / float64(len(a)), nil

}

func splitPathAndExt(path string) (string, string) {
	return filepath.Join(filepath.Dir(filepath.Clean(path)), filepath.Base(path[:len(path)-len(filepath.Ext(path))])), filepath.Ext(path)
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
