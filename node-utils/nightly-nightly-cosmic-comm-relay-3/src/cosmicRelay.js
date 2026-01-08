class CosmicRelay {
  constructor(dialects = {}) {
    this.entities = {}; // Stores entityName: { dialectName: string }
    this.dialects = dialects;
  }

  registerEntity(entityName, dialectName) {
    if (!this.dialects[dialectName]) {
      throw new Error(`Dialect '${dialectName}' not found.`);
    }
    this.entities[entityName] = { dialectName };
    console.log(`Entity '${entityName}' registered with dialect '${dialectName}'.`);
  }

  sendMessage(senderName, receiverName, message) {
    if (!this.entities[senderName]) {
      throw new Error(`Sender entity '${senderName}' not registered.`);
    }
    if (!this.entities[receiverName]) {
      throw new Error(`Receiver entity '${receiverName}' not registered.`);
    }

    const senderDialect = this.dialects[this.entities[senderName].dialectName];
    const receiverDialect = this.dialects[this.entities[receiverName].dialectName];

    let transformedMessage = message;
    if (senderDialect && senderDialect.transform) {
      transformedMessage = senderDialect.transform(transformedMessage);
    }

    let finalMessage = transformedMessage;
    if (receiverDialect) {
      if (receiverDialect.prefix) {
        finalMessage = receiverDialect.prefix + finalMessage;
      }
      if (receiverDialect.suffix) {
        finalMessage = finalMessage + receiverDialect.suffix;
      }
    }

    return finalMessage;
  }
}

module.exports = { CosmicRelay };
