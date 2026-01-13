export function getPairings(selected) {
  const pairMap = {
    Chocolate: ['Cheese', 'Nuts'],
    Cheese: ['Chocolate', 'Crackers'],
    Fruit: ['Nuts', 'Salsa'],
    Nuts: ['Chocolate', 'Fruit'],
    Crackers: ['Cheese'],
    Salsa: ['Fruit'],
    Popcorn: ['Salsa'],
  };
  const suggestions = new Set();
  selected.forEach((snack) => {
    const pairs = pairMap[snack] || [];
    pairs.forEach((p) => {
      if (!selected.includes(p)) {
        suggestions.add(`${snack} + ${p}`);
      }
    });
  });
  return Array.from(suggestions);
}
