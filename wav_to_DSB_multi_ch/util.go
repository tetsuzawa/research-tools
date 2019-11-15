package main

import "path/filepath"

func getFileNameWithoutExt(path string) string {
	return filepath.Base(path[:len(path)-len(filepath.Ext(path))])
}

func splitFilePath(path string) (string, string) {
	return filepath.Base(path[:len(path)-len(filepath.Ext(path))]), filepath.Ext(path)
}
