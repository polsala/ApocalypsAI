const formatDate = (date) => {
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleDateString(undefined, options);
};

const getPrediction = (date) => {
  const day = date.getDay(); // 0 Sunday
  const predictions = [
    'The wind whispers of hidden caches.',
    'A lone wanderer may cross your path.',
    'The sky is clear, but danger lurks.',
    'A storm is brewing; stay safe.',
    'You will find a forgotten relic.',
    'The silence is deafening; listen closely.',
    'A new alliance may form today.'
  ];
  return predictions[day];
};

module.exports = { formatDate, getPrediction };
