// Mock rationale: We simulate log lines and verify filtering/colorization logic without real file I/O.

mod tests {
    use super::*;

    #[test]
    fn test_log_level_parsing() {
        assert_eq!(LogLevel::from_str("ERROR"), Some(LogLevel::Error));
        assert_eq!(LogLevel::from_str("error"), Some(LogLevel::Error));
        assert_eq!(LogLevel::from_str("WARN"), Some(LogLevel::Warn));
        assert_eq!(LogLevel::from_str("info"), Some(LogLevel::Info));
        assert_eq!(LogLevel::from_str("debug"), Some(LogLevel::Debug));
        assert_eq!(LogLevel::from_str("unknown"), None);
    }

    #[test]
    fn test_log_level_matching() {
        let error = LogLevel::Error;
        let warn = LogLevel::Warn;
        let info = LogLevel::Info;
        let debug = LogLevel::Debug;

        // No filter should match everything
        assert!(error.matches(&None));
        assert!(warn.matches(&None));
        assert!(info.matches(&None));
        assert!(debug.matches(&None));

        // Filter by ERROR
        let filter_error = Some(LogLevel::Error);
        assert!(error.matches(&filter_error));
        assert!(!warn.matches(&filter_error));
        assert!(!info.matches(&filter_error));
        assert!(!debug.matches(&filter_error));

        // Filter by WARN
        let filter_warn = Some(LogLevel::Warn);
        assert!(error.matches(&filter_warn));
        assert!(warn.matches(&filter_warn));
        assert!(!info.matches(&filter_warn));
        assert!(!debug.matches(&filter_warn));

        // Filter by INFO
        let filter_info = Some(LogLevel::Info);
        assert!(error.matches(&filter_info));
        assert!(warn.matches(&filter_info));
        assert!(info.matches(&filter_info));
        assert!(!debug.matches(&filter_info));

        // Filter by DEBUG
        let filter_debug = Some(LogLevel::Debug);
        assert!(error.matches(&filter_debug));
        assert!(warn.matches(&filter_debug));
        assert!(info.matches(&filter_debug));
        assert!(debug.matches(&filter_debug));
    }
}
