package main

import (
	"reflect"
	"testing"
)

func TestAbsFloat64s(t *testing.T) {
	type args struct {
		fs []float64
	}
	tests := []struct {
		name string
		args args
		want []float64
	}{
		{
			name: "maxint16",
			args: args{
				fs: []float64{-23443, 5564, -7924, 30234, -37706},
			},
			want: []float64{23443, 5564, 7924, 30234, 37706},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := AbsFloat64s(tt.args.fs); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("AbsFloat64s() = %v, want %v", got, tt.want)
			}
		})
	}
}
