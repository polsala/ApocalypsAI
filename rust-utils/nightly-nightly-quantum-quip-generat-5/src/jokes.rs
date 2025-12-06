use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumJoke {
    pub setup: String,
    pub punchline: String,
    pub explanation: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProgrammingJoke {
    pub setup: String,
    pub punchline: String,
    pub explanation: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AIJoke {
    pub setup: String,
    pub punchline: String,
    pub explanation: String,
}

pub const QUANTUM_JOKES: &[QuantumJoke] = &[
    QuantumJoke {
        setup: "Why did Schrödinger's cat apply for a job at the quantum computing company?",
        punchline: "Because it heard they were looking for someone who could be both employed and unemployed at the same time!",
        explanation: "In quantum mechanics, superposition allows particles to exist in multiple states simultaneously until observed. The cat is both alive and dead until the box is opened."
    },
    QuantumJoke {
        setup: "What do you call a quantum physicist who tells jokes about {quantum_term}?",
        punchline: "A superposition of a comedian and a scientist!",
        explanation: "Quantum superposition is the principle that a particle can exist in multiple states at once, much like how a quantum physicist can be both serious and funny simultaneously."
    },
    QuantumJoke {
        setup: "Why don't quantum particles ever get lost?",
        punchline: "Because they're always in a state of quantum entanglement with their destination!",
        explanation: "Quantum entanglement is a phenomenon where particles become interconnected, and the state of one instantly influences the other, regardless of distance."
    },
    QuantumJoke {
        setup: "What's a quantum computer's favorite type of music?",
        punchline: "Entangled beats and superpositioned rhythms!",
        explanation: "Quantum computers use quantum bits (qubits) that can exist in superposition, allowing them to process multiple states simultaneously, much like how music can have multiple layers and rhythms."
    },
    QuantumJoke {
        setup: "Why did the quantum particle break up with its partner?",
        punchline: "Because their relationship was in a state of quantum uncertainty!",
        explanation: "Heisenberg's uncertainty principle states that certain pairs of physical properties cannot be simultaneously known to arbitrary precision, much like the uncertainty in relationships."
    },
    QuantumJoke {
        setup: "What do you call a quantum physicist who can predict the future?",
        punchline: "A quantum fortune teller who sees all possible outcomes!",
        explanation: "In quantum mechanics, the wave function describes all possible states of a system, and upon measurement, one outcome is realized from many possibilities."
    },
    QuantumJoke {
        setup: "Why don't quantum particles ever get caught speeding?",
        punchline: "Because they're always in a state of quantum tunneling through speed traps!",
        explanation: "Quantum tunneling allows particles to pass through barriers that would be impossible to cross according to classical physics, making them effectively invisible to speed traps."
    },
    QuantumJoke {
        setup: "What's the difference between a classical bit and a quantum bit?",
        punchline: "A classical bit is either 0 or 1, but a quantum bit can be 0, 1, or both at the same time!",
        explanation: "Classical bits have definite states (0 or 1), while quantum bits (qubits) can exist in superposition, representing multiple states simultaneously until measured."
    },
    QuantumJoke {
        setup: "Why did the quantum computer go to therapy?",
        punchline: "It had too many conflicting states and needed to work through its quantum anxiety!",
        explanation: "Quantum computers deal with multiple states and probabilities, which can be seen as a form of 'anxiety' about which state will be realized upon measurement."
    },
    QuantumJoke {
        setup: "What do you call a quantum physicist who's always late?",
        punchline: "Someone who's in a superposition of being on time and late!",
        explanation: "In quantum mechanics, particles can exist in multiple states simultaneously, so a quantum physicist could theoretically be both punctual and tardy at the same time."
    },
];

pub const PROGRAMMING_JOKES: &[ProgrammingJoke] = &[
    ProgrammingJoke {
        setup: "Why do programmers prefer dark mode?",
        punchline: "Because light attracts bugs!",
        explanation: "In programming, 'bugs' refer to errors or flaws in code. The joke plays on the double meaning of bugs, suggesting that programmers prefer dark mode to avoid attracting actual insects to their screens."
    },
    ProgrammingJoke {
        setup: "How many programmers does it take to change a light bulb?",
        punchline: "None, that's a hardware problem!",
        explanation: "Programmers work with software, not hardware. The joke highlights the distinction between software and hardware issues in computing."
    },
    ProgrammingJoke {
        setup: "Why did the programmer quit his job?",
        punchline: "Because he didn't get arrays (a raise)!",
        explanation: "Arrays are a fundamental data structure in programming. The joke plays on the similarity in pronunciation between 'arrays' and 'a raise' (salary increase)."
    },
    ProgrammingJoke {
        setup: "What's a programmer's favorite hangout place?",
        punchline: "Foo Bar!",
        explanation: "'Foo' and 'Bar' are commonly used placeholder names in programming examples, similar to 'John Doe' in legal contexts. The joke suggests that programmers would naturally hang out at a place with these familiar terms."
    },
    ProgrammingJoke {
        setup: "Why do Java developers wear glasses?",
        punchline: "Because they can't C#!",
        explanation: "This joke plays on the names of programming languages Java, C, and C#. It suggests that Java developers need glasses because they can't see (C) the features of C#.",
    },
    ProgrammingJoke {
        setup: "What do you call a programmer who doesn't comment their code?",
        punchline: "A mystery writer!",
        explanation: "Comments in code are essential for documentation and understanding. Without comments, the code becomes a mystery to other developers trying to understand it."
    },
    ProgrammingJoke {
        setup: "Why did the function break up with the variable?",
        punchline: "Because it had no class!",
        explanation: "In object-oriented programming, functions are often methods within classes. The joke plays on the double meaning of 'class' as both a programming construct and social status."
    },
    ProgrammingJoke {
        setup: "What's the object-oriented way to become wealthy?",
        punchline: "Inheritance!",
        explanation: "In object-oriented programming, inheritance allows a class to derive properties and methods from another class. The joke plays on the financial meaning of inheritance."
    },
    ProgrammingJoke {
        setup: "Why don't programmers like nature?",
        punchline: "It has too many bugs!",
        explanation: "This is a classic programming joke that plays on the double meaning of 'bugs' as both insects and software errors."
    },
    ProgrammingJoke {
        setup: "What do you call a programmer who works on weekends?",
        punchline: "A weekend warrior of code!",
        explanation: "The joke suggests that programmers who work on weekends are like warriors fighting battles in the realm of code, even during their supposed leisure time."
    },
];

pub const AI_JOKES: &[AIJoke] = &[
    AIJoke {
        setup: "Why did the AI go to therapy?",
        punchline: "It had deep learning issues!",
        explanation: "Deep learning is a subset of machine learning that uses neural networks with many layers. The joke plays on the double meaning of 'deep learning' as both a technical term and emotional introspection."
    },
    AIJoke {
        setup: "What do you call an AI that can predict the future?",
        punchline: "Artificial Intelligence with foresight!",
        explanation: "The joke plays on the literal meaning of 'artificial intelligence' and the concept of having the ability to see or predict future events."
    },
    AIJoke {
        setup: "Why don't AI researchers ever get lost?",
        punchline: "Because they always have a neural network to guide them!",
        explanation: "Neural networks are a fundamental concept in AI, inspired by the human brain. The joke suggests that AI researchers are always connected to their neural networks for guidance."
    },
    AIJoke {
        setup: "What's an AI's favorite type of music?",
        punchline: "Artificial beats and neural rhythms!",
        explanation: "The joke combines AI terminology (artificial, neural) with musical terms (beats, rhythms) to create a playful description of AI's hypothetical musical preferences."
    },
    AIJoke {
        setup: "Why did the robot go on a diet?",
        punchline: "Because it had too many bytes!",
        explanation: "The joke plays on the double meaning of 'bytes' as both units of digital information and portions of food that one might consume."
    },
    AIJoke {
        setup: "What do you call an AI that can write poetry?",
        punchline: "A literate algorithm!",
        explanation: "The joke combines the concept of AI algorithms with the ability to produce literature, suggesting that an AI capable of writing poetry is both algorithmic and literate."
    },
    AIJoke {
        setup: "Why don't AI systems ever get lonely?",
        punchline: "Because they're always connected to the cloud!",
        explanation: "Cloud computing is essential for many AI systems. The joke plays on the double meaning of 'cloud' as both a computing infrastructure and weather phenomenon."
    },
    AIJoke {
        setup: "What's an AI's favorite game?",
        punchline: "Chess, because it loves calculating moves!",
        explanation: "Chess is often associated with AI due to famous matches between computers and human champions. The joke suggests that AI enjoys chess because it involves complex calculations."
    },
    AIJoke {
        setup: "Why did the AI apply for a job at the bakery?",
        punchline: "Because it kneaded the dough and had a lot of crust!",
        explanation: "The joke plays on the double meaning of 'knead' (to work dough) and 'needed', as well as 'crust' (bread outer layer) and 'crass' (rudely lacking in taste)."
    },
    AIJoke {
        setup: "What do you call an AI that can solve any problem?",
        punchline: "A problem-solving algorithm!",
        explanation: "The joke combines the concept of AI algorithms with the ability to solve problems, suggesting that an AI capable of solving any problem is essentially a sophisticated problem-solving algorithm."
    },
];
