package main

import (
	"io/ioutil"
	"strings"
	"testing"
)

func TestModuleStructure(t *testing.T) {
	files := []string{"main.tf", "variables.tf", "outputs.tf"}
	for _, f := range files {
		content, err := ioutil.ReadFile(f)
		if err != nil {
			t.Fatalf("Failed to read %s: %v", f, err)
		}
		if len(content) == 0 {
			t.Fatalf("%s is empty", f)
		}
	}
}

func TestMainTFContents(t *testing.T) {
	content, err := ioutil.ReadFile("main.tf")
	if err != nil {
		t.Fatalf("Failed to read main.tf: %v", err)
	}
	str := string(content)
	if !strings.Contains(str, "resource \"aws_s3_bucket\"") {
		t.Errorf("main.tf does not contain aws_s3_bucket resource")
	}
	if !strings.Contains(str, "versioning") {
		t.Errorf("main.tf does not contain versioning block")
	}
	if !strings.Contains(str, "lifecycle_rule") {
		t.Errorf("main.tf does not contain lifecycle_rule block")
	}
}

func TestVariablesTFContents(t *testing.T) {
	content, err := ioutil.ReadFile("variables.tf")
	if err != nil {
		t.Fatalf("Failed to read variables.tf: %v", err)
	}
	str := string(content)
	if !strings.Contains(str, "variable \"bucket_name\"") {
		t.Errorf("variables.tf does not define bucket_name")
	}
	if !strings.Contains(str, "variable \"region\"") {
		t.Errorf("variables.tf does not define region")
	}
}

func TestOutputsTFContents(t *testing.T) {
	content, err := ioutil.ReadFile("outputs.tf")
	if err != nil {
		t.Fatalf("Failed to read outputs.tf: %v", err)
	}
	str := string(content)
	if !strings.Contains(str, "output \"bucket_id\"") {
		t.Errorf("outputs.tf does not define bucket_id")
	}
	if !strings.Contains(str, "output \"bucket_arn\"") {
		t.Errorf("outputs.tf does not define bucket_arn")
	}
}
