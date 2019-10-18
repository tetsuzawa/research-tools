package main

import (
	"encoding/binary"
	"gonum.org/v1/gonum/floats"
	"math"
)

func Float32ToBytes(f float32) []byte {
	bits := math.Float32bits(f)
	b := make([]byte, 8)
	binary.LittleEndian.PutUint32(b, bits)
	return b
}

func BytesToFloat32(b []byte) float32 {
	ui32 := binary.LittleEndian.Uint32(b)
	f := math.Float32frombits(ui32)
	return f
}

func Float64ToBytes(f float64) []byte {
	bits := math.Float64bits(f)
	b := make([]byte, 8)
	binary.LittleEndian.PutUint64(b, bits)
	return b
}

func BytesToFloat64(b []byte) float64 {
	ui64 := binary.LittleEndian.Uint64(b)
	f := math.Float64frombits(ui64)
	return f
}


func Uint16ToBytes(ui uint16) []byte{
	b := make([]byte, 2)
	binary.LittleEndian.PutUint16(b, ui)
	return b
}

func BytesToUint16(b []byte) uint16 {
	ui := binary.LittleEndian.Uint16(b)
	return ui
}

func Uint32ToBytes(ui uint32) []byte{
	b := make([]byte, 4)
	binary.LittleEndian.PutUint32(b, ui)
	return b
}

func BytesToUint32(b []byte) uint32 {
	ui := binary.LittleEndian.Uint32(b)
	return ui
}

func Uint64ToBytes(ui uint64) []byte{
	b := make([]byte, 8)
	binary.LittleEndian.PutUint64(b, ui)
	return b
}

func BytesToUint64(b []byte) uint64 {
	ui := binary.LittleEndian.Uint64(b)
	return ui
}

////////////////////////////////////

func Int16ToUint16(i int16) uint16 {
	var ui uint16
	if 0 < i {
		ui = uint16(i)
	} else {
		ui = (^uint16(-i) + 1)
	}
	return ui
}

func Uint16ToInt16(ui uint16) int16 {
	var i int16
	if ui > math.MaxInt16 {
		i = int16(ui - math.MaxUint16 - 1)
	} else {
		i = int16(ui)
	}
	return i
}

func Int32ToUint32(i int32) uint32 {
	var ui uint32
	if 0 < i {
		ui = uint32(i)
	} else {
		ui = (^uint32(-i) + 1)
	}
	return ui
}

func Uint32ToInt32(ui uint32) int32 {
	var i int32
	if ui > math.MaxInt32 {
		i = int32(ui - math.MaxUint32 - 1)
	} else {
		i = int32(ui)
	}
	return i
}

func Int64ToUint64(i int64) uint64 {
	var ui uint64
	if 0 < i {
		ui = uint64(i)
	} else {
		ui = (^uint64(-i) + 1)
	}
	return ui
}

func Uint64ToInt64(ui uint64) int64 {
	var i int64
	if ui > math.MaxInt64 {
		i = int64(ui - math.MaxUint64 - 1)
	} else {
		i = int64(ui)
	}
	return i
}

func float32sToBytes(fs []float32) []byte {
	bs := make([]byte, len(fs)*4)
	b := make([]byte, 4)
	for _, f := range fs {
		bits := math.Float32bits(f)
		binary.LittleEndian.PutUint32(b, bits)
		bs = append(bs, b...)
	}
	return bs

}

func bytesToFloat64s(bs []byte) []float64 {
	fs := make([]float64, len(bs)/8)
	var idx int
	for i := 0; i < len(bs)/4; i++ {
		idx = i * 8
		ui := binary.LittleEndian.Uint64(bs[idx : idx+8])
		f := math.Float64frombits(ui)
		fs[i] = f
	}
	return fs
}

func NormalizeFloat32s(fs []float32) []float32 {
	fs64 := make([]float64, len(fs))
	for i, s := range fs {
		fs64[i] = float64(s)
	}
	m := floats.Max(fs64)
	for i, s := range fs64 {
		fs[i] = float32(s / m)
	}
	return fs
}

func NormalizeFloat64s(fs []float64) []float64 {
	m := floats.Max(fs)
	for i, f := range fs {
		fs[i] = f / m
	}
	return fs
}

func Float32sToInt16s(fs []float32) []int16 {
	fs = NormalizeFloat32s(fs)
	is := make([]int16, len(fs))
	for i, s := range fs {
		is[i] = int16(s * math.MaxInt16)
	}
	return is
}

func Float64sToInt16s(fs []float64) []int16 {
	fs = NormalizeFloat64s(fs)
	is := make([]int16, len(fs))
	for i, s := range fs {
		is[i] = int16(s * math.MaxInt16)
	}
	return is
}

func Bytes2int(bytes ...byte) int64 {
	if 0x7f < bytes[0] {
		mask := uint64(1<<uint(len(bytes)*8-1) - 1)

		bytes[0] &= 0x7f
		i := Bytes2uint(bytes...)
		i = (^i + 1) & mask
		return int64(-i)

	} else {
		i := Bytes2uint(bytes...)
		return int64(i)
	}
}

// Bytes2uint converts []byte to uint64
func Bytes2uint(bytes ...byte) uint64 {
	padding := make([]byte, 8-len(bytes))
	i := binary.LittleEndian.Uint64(append(padding, bytes...))
	return i
}

// Int2bytes converts int to []byte
func Int2bytes(i int, size int) []byte {
	var ui uint64
	if 0 < i {
		ui = uint64(i)
	} else {
		ui = (^uint64(-i) + 1)
	}
	return Uint2bytes(ui, size)
}

// Uint2bytes converts uint64 to []byte
func Uint2bytes(i uint64, size int) []byte {
	bytes := make([]byte, 8)
	binary.LittleEndian.PutUint64(bytes, i)
	return bytes[8-size : 8]
}

func bytesToInt16(b []byte) int16 {
	ui := binary.LittleEndian.Uint16(b)
	i := Uint16ToInt16(ui)
	return i
}

func bytesToInt16s(bs []byte) []int16 {
	is := make([]int16, len(bs)/2)
	var idx int
	for i := 0; i < len(bs)/2; i++ {
		idx = i * 2
		//bs[idx] sonomama
		ui := binary.LittleEndian.Uint16(bs[idx : idx+2])
		in := Uint16ToInt16(ui)
		//f := math.Float64frombits(ui)
		is[i] = in
	}
	return is
}
