const core = require('@actions/core')
const github = require('@actions/github')

/**
 * Determine which labels to apply based on a list of changed file paths.
 * @param {string[]} files - Array of file paths changed in the PR.
 * @returns {string[]} Array of label names (unique).
 */
function determineLabels(files) {
  const labels = new Set()
  for (const file of files) {
    if (file.startsWith('docs/') || file.endsWith('.md')) {
      labels.add('documentation')
    } else if (file.startsWith('tests/') || file.endsWith('.test.js') || file.endsWith('_test.py')) {
      labels.add('tests')
    } else if (file.startsWith('.github/') || file.endsWith('.yml') || file.endsWith('.yaml')) {
      labels.add('ci')
    } else if (file.endsWith('.py') || file.endsWith('.js') || file.endsWith('.ts') || file.endsWith('.rs')) {
      labels.add('code')
    }
  }
  return Array.from(labels)
}

async function run() {
  try {
    const token = core.getInput('repo-token', { required: true })
    const octokit = github.getOctokit(token)
    const context = github.context

    if (!context.payload.pull_request) {
      core.setFailed('No pull request found in the context.')
      return
    }

    const prNumber = context.payload.pull_request.number
    const { owner, repo } = context.repo

    // Gather all changed files (paginate in case of many files)
    const changedFiles = await octokit.paginate(
      octokit.rest.pulls.listFiles,
      { owner, repo, pull_number: prNumber },
      response => response.data.map(f => f.filename)
    )

    const labels = determineLabels(changedFiles)
    if (labels.length === 0) {
      core.info('No matching labels to add.')
      return
    }

    await octokit.rest.issues.addLabels({
      owner,
      repo,
      issue_number: prNumber,
      labels
    })
    core.info(`Added labels: ${labels.join(', ')}`)
  } catch (error) {
    core.setFailed(error.message)
  }
}

run()

module.exports = { determineLabels, run }
