package goresearch

import (
	"errors"
	"fmt"
	"math"

	"github.com/mjibson/go-dsp/fft"
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

func CalcMSE(a []float64, b []float64) (float64, error) {
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

func Convolve(xs, ys []float64) []float64 {
	var convLen, sumLen = len(xs), len(ys)
	if convLen > sumLen {
		ys = append(ys, make([]float64, convLen-sumLen)...)
	} else {
		convLen, sumLen = sumLen, convLen
		xs = append(xs, make([]float64, convLen-sumLen)...)
	}
	var rs = make([]float64, convLen)
	var nodeSum float64
	var i, j int
	for i = 0; i < convLen; i++ {
		for j = 0; j < sumLen; j++ {
			if i-j < 0 {
				continue
			}
			nodeSum += xs[i-j] * ys[j]
		}
		rs[i] = nodeSum
		nodeSum = 0
	}
	return rs
}

// FastConvolve - Linear fast convolution
func FastConvolve(xs, ys []float64) []float64 {
	L := len(xs)
	N := len(ys)
	M := N + L - 1

	// zero padding
	xsz := append(xs, make([]float64, M-L)...)
	ysz := append(ys, make([]float64, M-N)...)

	var rs = make([]float64, M)
	var Rs = make([]complex128, M)

	fmt.Printf("calcurating fft...\n")

	Xs := fft.FFT(Float64sToComplex128s(xsz))
	Ys := fft.FFT(Float64sToComplex128s(ysz))

	for i := 0; i < M; i++ {
		// progress
		fmt.Printf("calucurating convolution... %d%%\r", (i+1)*100/M)
		Rs[i] = Xs[i] * Ys[i]
	}
	fmt.Printf("\ncalcurating ifft...\n")

	rs = Complex128sToFloat64s(fft.IFFT(Rs))

	return rs
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
