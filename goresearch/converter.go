package goresearch

import (
	"math"

	"gonum.org/v1/gonum/floats"
)

func abs(x int) int {
	if x < 0 {
		return -1 * x
	}
	return x
}

func AbsFloat64s(fs []float64) []float64 {
	fsAbs := make([]float64, len(fs))
	for i, v := range fs {
		fsAbs[i] = math.Abs(v)
	}
	return fsAbs
}

func AbsInts(is []int) []int {
	isAbs := make([]int, len(is))
	for i, v := range is {
		isAbs[i] = abs(v)
	}
	return isAbs
}

func NormToMaxInt16(data []float64) []float64 {

	maxAmp := floats.Max(AbsFloat64s(data))
	if maxAmp > math.MaxInt16+1 {
		reductionRate := math.MaxInt16 / maxAmp
		for i, _ := range data {
			data[i] *= reductionRate
		}
	}
	return data
}

func Int16sToInts(i16s []int16) []int {
	var is = make([]int, len(i16s))
	for i, v := range i16s {
		is[i] = int(v)
	}
	return is
}

func Float64sToInts(fs []float64) []int {
	is := make([]int, len(fs))
	for i, s := range fs {
		is[i] = int(s)
	}
	return is
}

func IntsToFloat64s(is []int) []float64 {
	fs := make([]float64, len(is))
	for i, s := range is {
		fs[i] = float64(s)
	}
	return fs
}
func Float64sToComplex128s(fs []float64) []complex128 {
	cs := make([]complex128, len(fs))
	for i, f := range fs {
		cs[i] = complex(f, 0)
	}
	return cs
}

func Complex128sToFloat64s(cs []complex128) []float64 {
	fs := make([]float64, len(cs))
	for i, c := range cs {
		fs[i] = real(c)
	}
	return fs
}
