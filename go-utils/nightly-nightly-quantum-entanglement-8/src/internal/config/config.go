package config

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"gopkg.in/yaml.v3"
)

// Config represents the application configuration
type Config struct {
	Server ServerConfig `yaml:"server" json:"server"`
	Quantum QuantumConfig `yaml:"quantum" json:"quantum"`
	Logging LoggingConfig `yaml:"logging" json:"logging"`
}

// ServerConfig contains server settings
type ServerConfig struct {
	Port int    `yaml:"port" json:"port"`
	Host string `yaml:"host" json:"host"`
}

// QuantumConfig contains quantum simulation settings
type QuantumConfig struct {
	DefaultFidelity    float64 `yaml:"default_fidelity" json:"default_fidelity"`
	DecoherenceRate    float64 `yaml:"decoherence_rate" json:"decoherence_rate"`
	MeasurementThreshold float64 `yaml:"measurement_threshold" json:"measurement_threshold"`
}

// LoggingConfig contains logging settings
type LoggingConfig struct {
	Level string `yaml:"level" json:"level"`
}

// Default returns a default configuration
func Default() *Config {
	return &Config{
		Server: ServerConfig{
			Port: 8080,
			Host: "0.0.0.0",
		},
		Quantum: QuantumConfig{
			DefaultFidelity:    0.95,
			DecoherenceRate:    0.01,
			MeasurementThreshold: 0.8,
		},
		Logging: LoggingConfig{
			Level: "info",
		},
	}
}

// Load loads configuration from a YAML file
func Load(filename string) (*Config, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to open config file: %w", err)
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	cfg := Default()
	err = yaml.Unmarshal(content, cfg)
	if err != nil {
		return nil, fmt.Errorf("failed to parse config file: %w", err)
	}

	return cfg, nil
}

// Save saves configuration to a YAML file
func (c *Config) Save(filename string) error {
	content, err := yaml.Marshal(c)
	if err != nil {
		return fmt.Errorf("failed to marshal config: %w", err)
	}

	err = os.WriteFile(filename, content, 0644)
	if err != nil {
		return fmt.Errorf("failed to write config file: %w", err)
	}

	return nil
}

// Validate validates the configuration
func (c *Config) Validate() error {
	if c.Server.Port <= 0 || c.Server.Port > 65535 {
		return fmt.Errorf("invalid server port: %d", c.Server.Port)
	}

	if c.Quantum.DefaultFidelity <= 0 || c.Quantum.DefaultFidelity > 1 {
		return fmt.Errorf("invalid default fidelity: %f", c.Quantum.DefaultFidelity)
	}

	if c.Quantum.DecoherenceRate < 0 || c.Quantum.DecoherenceRate > 1 {
		return fmt.Errorf("invalid decoherence rate: %f", c.Quantum.DecoherenceRate)
	}

	if c.Quantum.MeasurementThreshold <= 0 || c.Quantum.MeasurementThreshold > 1 {
		return fmt.Errorf("invalid measurement threshold: %f", c.Quantum.MeasurementThreshold)
	}

	return nil
}

// String implements Stringer interface
func (c *Config) String() string {
	content, _ := json.MarshalIndent(c, "", "  ")
	return string(content)
}
