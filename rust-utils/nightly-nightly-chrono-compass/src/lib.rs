use std::time::Duration;

pub fn get_temporal_status(uptime: Duration) -> String {
    let total_seconds = uptime.as_secs();
    let hours = total_seconds / 3600;
    let minutes = (total_seconds % 3600) / 60;
    let seconds = total_seconds % 60;

    let drift_message = if hours < 1 {
        "Perfectly Aligned with the Chrono-Flow."
    } else if hours < 24 {
        "Slightly Drifting, but within acceptable parameters."
    } else if hours < 72 {
        "Temporal Anomaly Detected! Consider a system reboot for realignment."
    } else {
        "Critical Temporal Instability! Seek immediate system recalibration!"
    };

    format!(
        "Uptime: {}h {}m {}s\nTemporal Status: {}",
        hours, minutes, seconds, drift_message
    )
}
