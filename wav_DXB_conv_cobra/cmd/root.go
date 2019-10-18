package cmd

import (
	"fmt"
	"github.com/mitchellh/go-homedir"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"os"
)

var cfgFile string

func NewCmdRoot() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "wdconv",
		Short: "WDConv is a .wav .DxB converter.",
		Long: `A .wav .DxB converter built with Golang.
This app convert .wav file to .DXB file or .DXB to .wav file`,
	}
	cobra.OnInitialize(initConfig)

	cmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.cmd-test.yaml")
	cmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")

	cmd.AddCommand(NewCmdWtoD())
	return cmd
}

func Execute() {
	cmd := NewCmdRoot()
	cmd.SetOut(os.Stdout)
	if err := cmd.Execute(); err != nil {
		cmd.SetErr(os.Stdout)
		cmd.Println(err)
		os.Exit(1)
	}
}

func init() {
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, err := homedir.Dir()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		viper.AddConfigPath(home)
		viper.SetConfigName(".cmd-t")
	}

	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err == nil {
		fmt.Println("Using config file:", viper.ConfigFileUsed())
	}
}
