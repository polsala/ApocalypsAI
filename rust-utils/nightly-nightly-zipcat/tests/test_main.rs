use std::io::Write;
use tempfile::tempdir;
use zip::write::FileOptions;
use nightly_zipcat::list_zip;

#[test]
fn test_list_zip_basic() {
    // Create a temporary zip file with two entries
    let dir = tempdir().unwrap();
    let zip_path = dir.path().join("test.zip");
    let file = std::fs::File::create(&zip_path).unwrap();
    let mut zip = zip::ZipWriter::new(file);
    let options = FileOptions::default().compression_method(zip::CompressionMethod::Stored);

    zip.start_file("hello.txt", options).unwrap();
    zip.write_all(b"Hello, world!").unwrap();

    zip.start_file("data.bin", options).unwrap();
    zip.write_all(&[0xde, 0xad, 0xbe, 0xef]).unwrap();

    zip.finish().unwrap();

    // Call the library function
    let previews = list_zip(&zip_path, 4, None).unwrap();

    // Verify we got two entries sorted alphabetically
    assert_eq!(previews.len(), 2);
    assert_eq!(previews[0].name, "data.bin");
    assert_eq!(previews[0].preview_bytes, vec![0xde, 0xad, 0xbe, 0xef]);
    assert_eq!(previews[1].name, "hello.txt");
    assert_eq!(previews[1].preview_bytes, b"Hell".to_vec());
}
