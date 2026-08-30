use nightly_qr_cryptic::{rotate_matrix, render_ascii};

#[test]
fn test_rotate_once() {
    // 2x2 matrix: true false / false true
    let original = vec![
        vec![true, false],
        vec![false, true],
    ];
    let rotated = rotate_matrix(original, 1);
    let expected = vec![
        vec![false, true],
        vec![true, false],
    ];
    assert_eq!(rotated, expected);
}

#[test]
fn test_rotate_twice() {
    let original = vec![
        vec![true, false, true],
        vec![false, true, false],
        vec![true, false, true],
    ];
    let rotated = rotate_matrix(original.clone(), 2);
    // Rotating twice should equal a 180° flip (matrix reversed both axes)
    let mut expected = original.clone();
    expected.reverse();
    for row in &mut expected {
        row.reverse();
    }
    assert_eq!(rotated, expected);
}

#[test]
fn test_render_ascii() {
    let matrix = vec![
        vec![true, false],
        vec![false, true],
    ];
    let ascii = render_ascii(&matrix);
    let expected = "██  \n  ██\n";
    assert_eq!(ascii, expected);
}
