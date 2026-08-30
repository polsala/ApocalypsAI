const { getFact } = require('./fun_fact');\n\nfunction run() {\n  const fact = getFact();\n  // GitHub Actions notice command\n  console.log(`::notice::Fun Fact: ${fact}`);\n}\n\nrun();
