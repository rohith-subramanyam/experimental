/*
Package main functionally tests the containersvc package.

Copyright (c) 2017 Nutanix Inc. All rights reserved.

Author: rohith.subramanyam@nutanix.com
*/
package main

import (
	"flag"

	"github.com/golang/glog"

	"containersvc"
)

// Main tests the exposed functions/APIs: Start, Status and Stop.
// It assumes that the docker daemon is running and should be run at the same
// permission level as the docker daemon.
// When run with 2 arguments, it starts a container with the path to image as
// the first argument and the image name/ID as the second argument.
// 	$ sudo ./testcontainer /tmp/nutanix_test.tar nutanix_test
// When run with 3 arguments, the 3rd argument is the volumes to be mounted in
// the container.
// 	$ sudo ./testcontainer /tmp/nutanix_test.tar nutanix_test
// 		nucalm_test:/data
// When run with 1 argument, it prints the status of running containers of image
// = the first argument, stops the container and again checks for its status.
// 	$ sudo ./testcontainer nutanix_test
func main() {
	flag.Parse()
	flag.Set("logtostderr", "true")

	if flag.NArg() == 2 {
		if err := containersvc.Start(flag.Arg(0), flag.Arg(1),
			&containersvc.Config{}); err != nil {

			glog.Fatal(err)
		}

		return
	}

	if flag.NArg() == 3 {
		vols := flag.Args()[2:]
		if err := containersvc.Start(flag.Arg(0), flag.Arg(1),
			&containersvc.Config{Volumes: vols}); err != nil {

			glog.Fatal(err)
		}

		return
	}

	if flag.NArg() == 1 {
		img := flag.Arg(0)
		if err := containersvc.Status(img, ""); err != nil {
			glog.Fatal(err)
		}
		if err := containersvc.Stop(img, "", false); err != nil {
			glog.Fatal(err)
		}
		if err := containersvc.Status(img, ""); err != nil {
			glog.Fatal(err)
		}

		return
	}
}
