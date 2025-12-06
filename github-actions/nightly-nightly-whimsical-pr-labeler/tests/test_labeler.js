const { context, github } = require('@actions/github')
const nock = require('nock')

beforeEach(() => {
  context.payload = {
    pull_request: { number: 123, changed_files: 0 }
  }
})

it('applies correct label for 1 file', async () => {
  context.payload.pull_request.changed_files = 1
  nock('https://api.github.com')
    .post('/repos/owner/repo/issues/123/labels')
    .reply(200)
  require('../action').run()
  expect(github.issues.addLabels).toHaveBeenCalledWith({
    owner: 'owner',
    repo: 'repo',
    issue_number: 123,
    labels: ['🌱']
  })
})

it('applies correct label for 7 files', async () => {
  context.payload.pull_request.changed_files = 7
  nock('https://api.github.com')
    .post('/repos/owner/repo/issues/123/labels')
    .reply(200)
  require('../action').run()
  expect(github.issues.addLabels).toHaveBeenCalledWith({
    owner: 'owner',
    repo: 'repo',
    issue_number: 123,
    labels: ['部落']
  })
})

it('applies max label for 15 files', async () => {
  context.payload.pull_request.changed_files = 15
  nock('https://api.github.com')
    .post('/repos/owner/repo/issues/123/labels')
    .reply(200)
  require('../action').run()
  expect(github.issues.addLabels).toHaveBeenCalledWith({
    owner: 'owner',
    repo: 'repo',
    issue_number: 123,
    labels: ['🌪️']
  })
})
