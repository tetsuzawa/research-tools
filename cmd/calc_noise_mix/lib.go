package main

import (
	"math"
	"path/filepath"
)

func CalcAdjustedRMS(cleanRMS float64, snr float64) (noiseRMS float64) {
	a := snr / 20
	noiseRMS = cleanRMS / (math.Pow(10, a))
	return noiseRMS
}

func CalcRMS(amp []float64) float64 {
	var sum float64
	for _, v := range amp {
		sum += v * v
	}
	return math.Sqrt(sum / float64(len(amp)))
}

func IntsToFloat64s(is []int) []float64 {
	fs := make([]float64, len(is))
	for i, s := range is {
		fs[i] = float64(s)
	}
	return fs
}

func Float64sToInts(fs []float64) []int {
	is := make([]int, len(fs))
	for i, v := range fs {
		is[i] = int(v)
	}
	return is
}

func LinSpace(start, end float64, n int) []float64 {
	res := make([]float64, n)
	if n == 1 {
		res[0] = end
		return res
	}
	delta := (end - start) / (float64(n) - 1)
	for i := 0; i < n; i++ {
		res[i] = start + (delta * float64(i))
	}
	return res
}

func splitPathAndExt(path string) (string, string) {
	return filepath.Join(filepath.Dir(filepath.Clean(path)), filepath.Base(path[:len(path)-len(filepath.Ext(path))])), filepath.Ext(path)
}
