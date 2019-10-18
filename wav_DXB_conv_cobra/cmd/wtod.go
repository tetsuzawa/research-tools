package cmd

import (
	"encoding/binary"
	"fmt"
	"io/ioutil"
	"os"
	"reflect"
	"strings"

	"github.com/spf13/cobra"
	"github.com/takuyaohashi/go-wav"
	"github.com/tetsuzawa/converter"
)

type Options struct {
	Ch      int    `validate:"min=1,max=2"`
	OutName string `validate:"excludesall=!&%*;:."`
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
	cmd.Flags().IntVarP(&o.Ch, "channel", "c", 1, "ch [num]")
	cmd.Flags().StringVarP(&o.OutName, "outname", "o", "", "outname [name]")

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

	var name string
	fmt.Println("flags: ", o.Ch, o.OutName)
	if o.OutName != "" {
		name = o.OutName
	} else {
		name = nameParts[0]
	}
	ex := nameParts[1]

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

		value, ok := data.([]int16)
		if !ok {
			cmd.PrintErrf("Data type is not valid")
			os.Exit(5)
		}

		if o.Ch == 1 {
			fw, err := os.Create(name + ".DSB")
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			defer fw.Close()
			b := make([]byte, 2)
			buf := make([]byte, 0)

			for i, v := range value {
				cmd.Printf("working... %d%%\r", (i+1)*100/len(value))

				ui := converter.Int16ToUint16(v)
				binary.LittleEndian.PutUint16(b, ui)
				buf = append(buf, b...)
			}
			_, err = fw.Write(buf)
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			cmd.Printf("\n\n")
			cmd.Println("end!!")
		} else {
			fw1, err := os.Create(name + "ch1.DSB")
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			defer fw1.Close()
			fw2, err := os.Create(name + "ch2.DSB")
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			defer fw2.Close()
			b := make([]byte, 2)
			buf1 := make([]byte, 0)
			buf2 := make([]byte, 0)
			for i := 0; i < len(value)/2; i++ {
				cmd.Printf("working... %d%%\r", (i+1)*100*2/len(value))

				ui1 := converter.Int16ToUint16(value[i*2])
				ui2 := converter.Int16ToUint16(value[i*2+1])
				binary.LittleEndian.PutUint16(b, ui1)
				binary.LittleEndian.PutUint16(b, ui2)
				buf1 = append(buf1, b...)
				buf2 = append(buf2, b...)
			}
			_, err = fw1.Write(buf1)
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			_, err = fw2.Write(buf2)
			if err != nil {
				cmd.PrintErrln(err)
				os.Exit(3)
			}
			cmd.Printf("\n\n")
			cmd.Println("end!!")
		}
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
