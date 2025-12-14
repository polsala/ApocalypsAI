package main

import (
	"os"
	"strings"
	"testing"
)

func TestMainTFContainsBucketResource(t *testing.T) {
	content, err := os.ReadFile("../terraform-modules/nightly-terraform-s3-bucket/src/main.tf")
	if err != nil {
		t.Fatalf("failed to read main.tf: %v", err)
	}
	if !strings.Contains(string(content), "resource \"aws_s3_bucket\" \"this\"") {
		t.Errorf("main.tf does not contain aws_s3_bucket resource")
	}
}

func TestVariablesTFContainsBucketName(t *testing.T) {
	content, err := os.ReadFile("../terraform-modules/nightly-terraform-s3-bucket/src/variables.tf")
	if err != nil {
		t.Fatalf("failed to read variables.tf: %v", err)
	}
	if !strings.Contains(string(content), "variable \"bucket_name\"") {
		t.Errorf("variables.tf does not contain bucket_name variable")
	}
}

func TestOutputsTFContainsBucketID(t *testing.T) {
	content, err := os.ReadFile("../terraform-modules/nightly-terraform-s3-bucket/src/outputs.tf")
	if err != nil {
		t.Fatalf("failed to read outputs.tf: %v", err)
	}
	if !strings.Contains(string(content), "output \"bucket_id\"") {
		t.Errorf("outputs.tf does not contain bucket_id output")
	}
}
