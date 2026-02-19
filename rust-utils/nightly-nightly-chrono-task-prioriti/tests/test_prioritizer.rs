#![cfg(test)]

use crate::Task;
use std::cmp::Ordering;

// Mock rationale: These tests operate on in-memory Task structs, simulating input data
// without requiring file I/O or external dependencies, ensuring determinism and offline execution.

#[test]
fn test_task_creation_and_priority_calculation() {
    let task1 = Task::new("Task A".to_string(), 1, 10).unwrap();
    // (10+1) / (1+1) = 11 / 2 = 5.5
    assert_eq!(task1.priority_score, 5.5f32);
    assert_eq!(task1.name, "Task A");
    assert_eq!(task1.decay_rate, 1);
    assert_eq!(task1.survival_impact, 10);

    let task2 = Task::new("Task B".to_string(), 8, 5).unwrap();
    // (5+1) / (8+1) = 6 / 9 = 0.666...
    assert!((task2.priority_score - 0.6666667f32).abs() < f32::EPSILON);

    let task3 = Task::new("Task C".to_string(), 0, 1).unwrap();
    // (1+1) / (0+1) = 2 / 1 = 2.0
    assert_eq!(task3.priority_score, 2.0f32);

    let task4 = Task::new("Task D".to_string(), 10, 10).unwrap();
    // (10+1) / (10+1) = 11 / 11 = 1.0
    assert_eq!(task4.priority_score, 1.0f32);

    let task5 = Task::new("Task E".to_string(), 5, 0).unwrap();
    // (0+1) / (5+1) = 1 / 6 = 0.166...
    assert!((task5.priority_score - 0.1666667f32).abs() < f32::EPSILON);
}

#[test]
fn test_task_creation_invalid_values() {
    assert!(Task::new("Invalid Decay".to_string(), 11, 5).is_err());
    assert!(Task::new("Invalid Impact".to_string(), 5, 11).is_err());
    assert!(Task::new("Both Invalid".to_string(), 11, 11).is_err());
    assert!(Task::new("Valid".to_string(), 10, 10).is_ok());
}

#[test]
fn test_task_sorting_order() {
    let task1 = Task::new("High Priority".to_string(), 1, 10).unwrap(); // 5.5
    let task2 = Task::new("Medium Priority".to_string(), 3, 7).unwrap(); // 2.66
    let task3 = Task::new("Low Priority".to_string(), 8, 5).unwrap(); // 0.66
    let task4 = Task::new("Zero Decay, Low Impact".to_string(), 0, 1).unwrap(); // 2.0
    let task5 = Task::new("High Decay, High Impact".to_string(), 10, 10).unwrap(); // 1.0

    let mut tasks = vec![task3.clone(), task1.clone(), task5.clone(), task2.clone(), task4.clone()];
    tasks.sort();

    // Expected order: task1 (5.5), task2 (2.66), task4 (2.0), task5 (1.0), task3 (0.66)
    assert_eq!(tasks[0], task1);
    assert_eq!(tasks[1], task2);
    assert_eq!(tasks[2], task4);
    assert_eq!(tasks[3], task5);
    assert_eq!(tasks[4], task3);
}

#[test]
fn test_task_sorting_with_equal_priority() {
    let task_a = Task::new("Task A".to_string(), 1, 1).unwrap(); // (1+1)/(1+1) = 1.0
    let task_b = Task::new("Task B".to_string(), 2, 2).unwrap(); // (2+1)/(2+1) = 1.0
    let task_c = Task::new("Task C".to_string(), 0, 0).unwrap(); // (0+1)/(0+1) = 1.0

    let mut tasks = vec![task_a.clone(), task_b.clone(), task_c.clone()];
    tasks.sort();

    // When priorities are equal, the order is stable but not strictly defined by name.
    // We just ensure they are all present and have the correct priority.
    assert_eq!(tasks[0].priority_score, 1.0);
    assert_eq!(tasks[1].priority_score, 1.0);
    assert_eq!(tasks[2].priority_score, 1.0);
    assert!(tasks.contains(&task_a));
    assert!(tasks.contains(&task_b));
    assert!(tasks.contains(&task_c));
}

#[test]
fn test_empty_tasks_list_sort() {
    let mut tasks: Vec<Task> = Vec::new();
    tasks.sort();
    assert!(tasks.is_empty());
}

// The `main` function's file/stdin reading and printing logic is harder to unit test directly
// without mocking `std::io` or using integration tests. For this self-contained utility,
// focusing on the core `Task` struct and its `Ord` implementation is sufficient for unit tests.
// Integration tests would involve running the compiled binary and capturing stdout, which is beyond
// the scope of a simple unit test file for this agent's output format.
