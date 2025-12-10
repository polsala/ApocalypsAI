use std::time::Duration;
use mockall::mock;
use tokio::time::sleep;

mock! {
    pub Timer {
        pub fn sleep(&self, _dur: Duration);
    }
}

#[tokio::test]
async fn test_timer_flow() {
    let mut mock_timer = TimerMock::new();
    mock_timer.expect_sleep().withf(|d| d.as_secs() > 0).times(2).returning(|_| {});

    let original_sleep = std::mem::replace(&mut sleep, Box::new(|_| Box::pin(mock_timer.sleep(Duration::from_secs(0))));

    let output = std::process::Command::new("cargo").args(["run", "--", "25", "5"]).output().unwrap();
    assert!(output.status.success());
    assert!(String::from_utf8_lossy(&output.stdout).contains("Brewing focus"));
    assert!(String::from_utf8_lossy(&output.stdout).contains("Tea break over"));

    sleep = original_sleep;
}
