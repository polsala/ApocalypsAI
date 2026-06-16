const { getLabelsFromTitle } = require('../src/index');

test('detect bug label', () => {
  const labels = getLabelsFromTitle('Fix typo in README');
  expect(labels).toContain('bug');
});

test('detect enhancement label', () => {
  const labels = getLabelsFromTitle('Add new feature for export');
  expect(labels).toContain('enhancement');
});

test('detect documentation label', () => {
  const labels = getLabelsFromTitle('Update docs for API');
  expect(labels).toContain('documentation');
});

test('multiple labels', () => {
  const labels = getLabelsFromTitle('Fix bug and add docs');
  expect(labels).toEqual(expect.arrayContaining(['bug', 'documentation']));
});
