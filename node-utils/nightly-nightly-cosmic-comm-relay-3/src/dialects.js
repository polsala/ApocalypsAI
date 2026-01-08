function defineDialects(dialectConfig) {
  const dialects = {};
  for (const name in dialectConfig) {
    if (Object.hasOwnProperty.call(dialectConfig, name)) {
      dialects[name] = {
        prefix: dialectConfig[name].prefix || '',
        suffix: dialectConfig[name].suffix || '',
        transform: dialectConfig[name].transform || ((msg) => msg) // Default identity transform
      };
    }
  }
  return dialects;
}

module.exports = { defineDialects };
