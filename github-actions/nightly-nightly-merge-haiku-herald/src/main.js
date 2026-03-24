const core = require('@actions/core');
const github = require('@actions/github');
const haikus = require('./haikus.json');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const targetType = core.getInput('target-type') || 'issue';
    const targetId = core.getInput('target-id', { required: true });

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;

    // Select a random haiku
    const haikuIndex = Math.floor(Math.random() * haikus.length);
    const selectedHaiku = haikus[haikuIndex];

    const commentBody = `### 📜 Nightly Merge Haiku Herald 📜\n\n${selectedHaiku}\n\n_A poetic nod from the ApocalypsAI Integrator._`;

    if (targetType === 'issue') {
      core.info(`Posting haiku to issue #${targetId} in ${owner}/${repo}...`);
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: parseInt(targetId, 10),
        body: commentBody
      });
      core.info(`Haiku posted to issue #${targetId}.`);
    } else if (targetType === 'discussion') {
      core.info(`Posting haiku to discussion #${targetId} in ${owner}/${repo}...`);
      
      const discussionQuery = `\n        query($owner: String!, $repo: String!, $discussionNumber: Int!) {\n          repository(owner: $owner, name: $repo) {\n            discussion(number: $discussionNumber) {\n              id\n            }\n          }\n        }\n      `;
      const discussionResponse = await octokit.graphql(discussionQuery, {
        owner,
        repo,
        discussionNumber: parseInt(targetId, 10)
      });

      const discussionNodeId = discussionResponse.repository.discussion.id;

      const addDiscussionCommentMutation = `\n        mutation($discussionId: ID!, $body: String!) {\n          addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {\n            comment {\n              id\n            }\n          }\n        }\n      `;
      await octokit.graphql(addDiscussionCommentMutation, {
        discussionId: discussionNodeId,
        body: commentBody
      });
      core.info(`Haiku posted to discussion #${targetId}.`);

    } else {
      core.setFailed(`Invalid target-type: ${targetType}. Must be 'issue' or 'discussion'.`);
      return;
    }

    core.setOutput('haiku-posted', true);

  } catch (error) {
    core.setFailed(error.message);
    core.setOutput('haiku-posted', false);
  }
}

module.exports = {
  run
};
