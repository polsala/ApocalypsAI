module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
    'plugin:prettier/recommended'
  ],
  parserOptions: {
    "ecmaVersion": 2020,
    "sourceType": "module"
  },
  env: {
    node: true,
    jest: true
  },
  rules: {
    // Add any specific rules here
  }
};
