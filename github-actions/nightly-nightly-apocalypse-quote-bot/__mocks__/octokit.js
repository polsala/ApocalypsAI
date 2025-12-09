const createMockOctokit = () => ({
  rest: {
    issues: {
      createComment: jest.fn()
    }
  }
});

module.exports = { createMockOctokit };
