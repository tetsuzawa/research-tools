package cmd

import "github.com/spf13/cobra"

func NewCmdWtoD() *cobra.Command {
	type Options struct {
		Optint int    `validate:"min=0,max=10"`
		Optstr string `validate:"required,alphanum"`
	}

	var (
		o = &Options{}
	)

	cmd := &cobra.Command{
		Use:   "wtod",
		Short: "convert .wav to .DSB",
		PreRunE: func(cmd *cobra.Command, args []string) error {
			return validateParams(*o)
		},
		Run: func(cmd *cobra.Command, args []string) {
			cmd.Printf("wtod called: optint: %d, optstr: %s", o.Optint, o.Optstr)
		},
	}
	cmd.Flags().IntVarP(&o.Optint, "int", "i", 0, "int option")
	cmd.Flags().StringVarP(&o.Optstr, "str", "s", "", "string option")

	return cmd
}

func init() {

}
