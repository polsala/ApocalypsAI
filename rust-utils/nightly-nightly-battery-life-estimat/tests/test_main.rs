// These tests run the compiled binary using std::process::Command.
// They are deterministic and do not require network access.

#[cfg(test)]
mod cli_tests {
    use std::process::Command;
    use std::str;

    fn run_tool(args: &[&str]) -> String {
        let output = Command::new("cargo")
            .args(&["run", "--quiet", "--"])
            .args(args)
            .output()
            .expect("Failed to execute cargo run");
        str::from_utf8(&output.stdout).unwrap().trim().to_string()
    }

    #[test]
    fn test_cli_normal() {
        let out = run_tool(&["5000", "250"]);
        assert_eq!(out, "Estimated runtime: 20.00 hours");
    }

    #[test]
    fn test_cli_apocalypse() {
        let out = run_tool(&["5000", "250", "--apocalypse"]);
        assert_eq!(out, "Estimated runtime (apocalypse mode): 15.00 hours");
    }
}
