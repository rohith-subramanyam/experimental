package main

import (
	"fmt"
	"github.com/davecgh/go-spew/spew"
	"github.com/nutanix-core/acs-utils/crypto"
)

func main() {
	ntnxCrypto := crypto.GetNtnxCrypto("")
	pw := ""
	fmt.Printf("pw: %s\n", spew.Sdump(pw))
	encryptedPwBytes, err := ntnxCrypto.Encrypt(pw)
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("bytes: %s\n", spew.Sdump(encryptedPwBytes))
	encryptedPwStr := string(encryptedPwBytes)
	fmt.Printf("string: %s\n", spew.Sdump(encryptedPwStr))
	var decryptedPw string
	//ntnxCrypto.Decrypt("\x19?\x97#'\x87zk\xeag\xa4\x8c5\x9e\b\xce\x06\x16\xeb\x1byB\xa5_\t\v\x19K\xd3白", decryptedPw)
	ntnxCrypto.Decrypt([]byte(encryptedPwStr), &decryptedPw)
	fmt.Printf("decrypted: %s", spew.Sdump(decryptedPw))
}
