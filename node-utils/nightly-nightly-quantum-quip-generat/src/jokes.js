// Quantum Computing Jokes Database
// Each joke should be family-friendly and include an explanation

const jokes = [
  {
    text: "Why don't quantum programmers ever make mistakes?\nBecause they exist in a superposition of correct and incorrect until observed!",
    category: "superposition",
    explanation: "In quantum mechanics, particles can exist in multiple states simultaneously until measured. Similarly, quantum programmers might argue their code is both correct and incorrect until someone actually runs it!"
  },
  {
    text: "Why are quantum particles terrible gossips?\nBecause once they're entangled, they always know what the other is up to!",
    category: "entanglement",
    explanation: "Quantum entanglement is a phenomenon where particles become linked and instantly affect each other regardless of distance. It's like having a quantum-level group chat!"
  },
  {
    text: "How many quantum programmers does it take to change a light bulb?\nNone - they just observe it in the dark state until it decides to turn on!",
    category: "superposition",
    explanation: "This plays on the observer effect in quantum mechanics, where observation can influence the state of a system."
  },
  {
    text: "Why did the qubit break up with the classical bit?\nBecause the qubit wanted a more meaningful relationship - one with superposition and entanglement!",
    category: "qubits",
    explanation: "Classical bits are either 0 or 1, while qubits can be in superposition of both states, making them more complex and 'interesting'!"
  },
  {
    text: "What do you call a quantum computer that's having an identity crisis?\nA superpositioned individual!",
    category: "superposition",
    explanation: "Superposition allows quantum systems to exist in multiple states at once, much like someone having an identity crisis can't decide who they are!"
  },
  {
    text: "Why don't quantum algorithms need coffee?\nBecause they're already in a state of quantum coherence!",
    category: "algorithms",
    explanation: "Quantum coherence is a key property that allows quantum computers to perform calculations. It's like being 'wired in' to the universe's processing power!"
  },
  {
    text: "What's a quantum computer's favorite type of music?\nEntangled harmonies!",
    category: "entanglement",
    explanation: "Entanglement creates correlations between quantum particles, similar to how harmonies create beautiful correlations between musical notes."
  },
  {
    text: "Why did Schrödinger's cat start a tech company?\nBecause it knew how to be both successful and failed until the funding round closed!",
    category: "superposition",
    explanation: "Schrödinger's cat is a famous thought experiment where a cat in a box is simultaneously alive and dead until observed, similar to a startup's uncertain fate before funding."
  },
  {
    text: "How do quantum computers send secret messages?\nThrough quantum key distribution - it's impossible to eavesdrop without being noticed!",
    category: "algorithms",
    explanation: "Quantum key distribution uses quantum mechanics principles to create theoretically unbreakable encryption."
  },
  {
    text: "Why don't quantum computers get lonely?\nBecause they're always entangled with their quantum processors!",
    category: "entanglement",
    explanation: "Entanglement creates strong correlations between quantum particles, ensuring they're never truly alone in their quantum state!"
  },
  {
    text: "What do you call a group of qubits playing cards?\nA superposition of poker faces!",
    category: "qubits",
    explanation: "Qubits can exist in multiple states simultaneously, so they could literally have multiple 'faces' at the same time during a poker game!"
  },
  {
    text: "Why did the quantum physicist refuse to play hide and seek?\nBecause they knew they could be found in multiple places at once!",
    category: "superposition",
    explanation: "Quantum particles can exist in multiple locations simultaneously due to superposition, making hide and seek rather pointless!"
  },
  {
    text: "What's the difference between a classical bit and a qubit at a party?\nThe classical bit is either dancing or not, but the qubit is doing both until someone looks!",
    category: "qubits",
    explanation: "This illustrates the fundamental difference between classical bits (definite states) and qubits (superposition of states)."
  },
  {
    text: "Why don't quantum computers need antivirus software?\nBecause any attempt to observe their state would collapse their wave function!",
    category: "hardware",
    explanation: "The observer effect in quantum mechanics means that measuring a quantum system changes its state, making traditional hacking approaches ineffective."
  },
  {
    text: "How do quantum computers apologize?\nThey say 'I'm sorry for being in such a superposition of wrong states!'",
    category: "superposition",
    explanation: "This plays on the idea that quantum systems can be in multiple states at once, including both right and wrong states simultaneously."
  },
  {
    text: "Why did the quantum algorithm go to therapy?\nIt had too many complex issues to resolve in superposition!",
    category: "algorithms",
    explanation: "Quantum algorithms often deal with complex mathematical problems that can be solved more efficiently using quantum superposition."
  },
  {
    text: "What do you call a quantum computer that tells jokes?\nA superpositioned comedian!",
    category: "general",
    explanation: "A play on words combining quantum superposition with the idea of a comedian being in multiple 'states' of humor at once."
  },
  {
    text: "Why don't quantum computers ever get jet lag?\nBecause they're already in multiple time zones simultaneously!",
    category: "general",
    explanation: "This is a playful take on quantum superposition, suggesting quantum computers can exist in multiple states (including time zones) at the same time."
  },
  {
    text: "What's a qubit's favorite social media platform?\nEntanglegram!",
    category: "qubits",
    explanation: "A pun combining 'entanglement' (quantum phenomenon) with 'Instagram', suggesting qubits love to connect and share their quantum states."
  },
  {
    text: "Why did the quantum computer go to art school?\nTo learn how to draw superpositioned portraits!",
    category: "hardware",
    explanation: "This joke plays on the idea that quantum computers can represent multiple states simultaneously, like an artist drawing multiple versions of a portrait at once."
  },
  {
    text: "How do quantum particles stay in touch?\nThey use quantum entanglement - no need for cell phones!",
    category: "entanglement",
    explanation: "Quantum entanglement allows particles to instantaneously affect each other regardless of distance, making traditional communication methods unnecessary."
  },
  {
    text: "Why don't quantum algorithms need GPS?\nBecause they can explore all possible paths simultaneously!",
    category: "algorithms",
    explanation: "Quantum algorithms can evaluate multiple solutions at once through superposition, unlike classical algorithms that must check each path sequentially."
  },
  {
    text: "What do you call a quantum computer that's always indecisive?\nA superpositioned processor!",
    category: "hardware",
    explanation: "This plays on the idea that quantum computers can exist in multiple states at once, making them perpetually 'indecisive' about their exact state."
  },
  {
    text: "Why did the qubit go to school?\nTo learn how to be in multiple states of knowledge at once!",
    category: "qubits",
    explanation: "Qubits can represent multiple states simultaneously, so they could theoretically learn multiple subjects or concepts at the same time."
  },
  {
    text: "What's a quantum computer's favorite game?\nQuantum leap frog!",
    category: "general",
    explanation: "A play on 'leapfrog' combined with 'quantum leap', referencing the quantum tunneling phenomenon where particles can 'jump' through barriers."
  },
  {
    text: "Why don't quantum computers need coffee breaks?\nThey're already operating at quantum speed!",
    category: "hardware",
    explanation: "Quantum computers can perform certain calculations much faster than classical computers, so they don't need breaks to maintain their performance."
  },
  {
    text: "How do quantum physicists organize their bookshelves?\nIn superposition - the books are both alphabetized and not alphabetized until observed!",
    category: "general",
    explanation: "This extends the quantum superposition concept to everyday life, suggesting that quantum physicists might apply quantum principles to mundane tasks."
  },
  {
    text: "Why did the quantum algorithm break up with the classical algorithm?\nIt said their relationship lacked the depth of quantum entanglement!",
    category: "algorithms",
    explanation: "This personifies algorithms and uses quantum entanglement as a metaphor for deep, meaningful connections."
  },
  {
    text: "What do you call a quantum computer that's always late?\nA superpositioned time keeper!",
    category: "hardware",
    explanation: "A playful take on quantum superposition, suggesting a quantum computer could be both on time and late simultaneously."
  },
  {
    text: "Why don't quantum computers need passwords?\nBecause their security is based on the uncertainty principle!",
    category: "algorithms",
    explanation: "Quantum cryptography uses principles like the uncertainty principle to create theoretically unbreakable security systems."
  }
];

module.exports = jokes;
