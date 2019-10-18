package cmd

import (
	"encoding/binary"
	"io/ioutil"
	"os"
	"reflect"
	"strings"

	"github.com/spf13/cobra"
	"github.com/takuyaohashi/go-wav"
	"github.com/tetsuzawa/converter"
)

type Options struct {
	Ch int `validate:"min=1,max=10"`
}

var (
	o = &Options{}
)

func NewCmdWtoD() *cobra.Command {

	cmd := &cobra.Command{
		Use:   "wtod",
		Short: "convert .wav to .DSB",
		PreRunE: func(cmd *cobra.Command, args []string) error {
			return validateParams(*o)
		},
		//Run: func(cmd *cobra.Command, args []string) {
		//	cmd.Printf("wtod called: optint: %d, optstr: %s", o.Ch)
		//},
		Run: wtod,
	}
	cmd.Flags().IntVarP(&o.Ch, "int", "c", 1, "ch option")

	return cmd
}

func init() {
}

func wtod(cmd *cobra.Command, args []string) {
	if len(args) == 0 {
		cmd.PrintErrf("Too few arguments. Need input file name")
		os.Exit(1)
	}

	fileName := args[0]
	nameParts := strings.Split(fileName, ".")
	name, ex := nameParts[0], nameParts[1]

	f, err := os.Open(fileName)
	if err != nil {
		cmd.PrintErrf("No such a file: %v", err)
		os.Exit(2)
	}
	defer f.Close()

	var data interface{}

	switch ex {
	case "wav":
		w, err := wav.NewReader(f)
		if err != nil {
			cmd.PrintErrln(err)
			os.Exit(3)
		}
		data, err = w.ReadSamples(int(w.GetSubChunkSize()) / int(w.GetNumChannels()))
		if err != nil {
			cmd.PrintErrln(err)
			os.Exit(3)
		}
		if reflect.TypeOf(data) != reflect.TypeOf([]int16{0,}) {
			cmd.PrintErrln(err)
			os.Exit(4)
		}
		cmd.Println("name: ", name)
		cmd.Println("type: ", reflect.TypeOf(data))
		cmd.Println("ex: ", ex)
		if value, ok := data.([]int16); ok {

			fw, err := os.Create(name + ".DSB")
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			cmd.Println("len of value: ", len(value))
			defer fw.Close()

			buf := make([]byte, 0)
			//buf := make([]byte, 2*len(value))

			for i, v := range value {
				cmd.Printf("working... %d%%\r", (i+1)*100/len(value))

				b := make([]byte, 2)
				ui := converter.Int16ToUint16(v)
				binary.LittleEndian.PutUint16(b, ui)
				//buf[i*2 : i*2+2] = b...
				buf = append(buf, b...)
			}
			_, err = fw.Write(buf)
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
		}
		cmd.Printf("\n\n")
		cmd.Println("end!!")

	case "DSB":
		buff, err := ioutil.ReadAll(f)
		if err != nil {
			cmd.PrintErrln(err)
			os.Exit(3)
		}
		data := converter.BytesToInt16(buff)
		cmd.Println(data)

	case "DDB":
		buff, err := ioutil.ReadAll(f)
		if err != nil {
			cmd.PrintErrln(err)
			os.Exit(3)
		}
		data := converter.BytesToFloat64s(buff)
		cmd.Println(data)
	default:
		cmd.PrintErrln("Unknown extention. Want: .wav, .DSB or .DDB. Got: " + ex)
		os.Exit(2)
	}
	//cmd.Println(data)
}
