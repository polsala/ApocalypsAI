const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(githubToken);

    const quotes = [
      "The only true wisdom is in knowing you know nothing. - Socrates",
      "The unexamined life is not worth living. - Socrates",
      "I think, therefore I am. - René Descartes",
      "Man is condemned to be free. - Jean-Paul Sartre",
      "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson",
      "The mind is everything. What you think you become. - Buddha",
      "We are what we repeatedly do. Excellence, then, is not an act, but a habit. - Aristotle",
      "It is not the strongest of the species that survives, nor the most intelligent that survives. It is the one that is most adaptable to change. - Charles Darwin",
      "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
      "Life is what happens when you're busy making other plans. - John Lennon"
    ];

    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

    if (github.context.eventName === 'pull_request' && github.context.payload.pull_request) {
      const prNumber = github.context.payload.pull_request.number;
      const repo = github.context.repo;

      await octokit.rest.issues.createComment({
        owner: repo.owner,
        repo: repo.repo,
        issue_number: prNumber,
        body: `✨ A moment of contemplation for your Pull Request, fellow traveler:\n\n> _\"${randomQuote}\"_`
      });
      core.setOutput('quote', randomQuote);
      core.info(`Pondered PR #${prNumber} with: \"${randomQuote}\"`)
    } else {
      core.warning('This action is intended to run on pull_request events.');
      core.setOutput('quote', 'No PR context available for pondering.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
