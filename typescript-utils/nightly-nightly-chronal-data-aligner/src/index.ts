export interface ChronalEcho {
  id: string;
  timestamp: number; // Unix epoch milliseconds
  source: string;
  dataType: string;
  payload: Record<string, any>;
}

export interface AlignedData {
  id: string;
  alignedTimestamp: Date;
  originalSource: string;
  alignedType: string;
  harmonizedPayload: Record<string, any>;
}

export class AlignmentError extends Error {
  constructor(message: string, public echoId?: string, public field?: string) {
    super(message);
    this.name = 'AlignmentError';
  }
}

/**
 * Validates if a raw object conforms to the ChronalEcho interface.
 * @param data The raw object to validate.
 * @returns True if the object is a valid ChronalEcho, false otherwise.
 */
export function isValidChronalEcho(data: any): data is ChronalEcho {
  if (typeof data !== 'object' || data === null) {
    return false;
  }
  if (typeof data.id !== 'string' || data.id.trim() === '') {
    return false;
  }
  if (typeof data.timestamp !== 'number' || isNaN(data.timestamp)) {
    return false;
  }
  if (typeof data.source !== 'string' || data.source.trim() === '') {
    return false;
  }
  if (typeof data.dataType !== 'string' || data.dataType.trim() === '') {
    return false;
  }
  if (typeof data.payload !== 'object' || data.payload === null) {
    return false;
  }
  return true;
}

/**
 * Aligns a valid ChronalEcho into a standardized AlignedData structure.
 * Performs basic type-specific transformations and timestamp conversion.
 * @param echo The ChronalEcho to align.
 * @returns An AlignedData object or an AlignmentError if alignment fails.
 */
export function alignChronalEcho(echo: ChronalEcho): AlignedData | AlignmentError {
  try {
    const alignedTimestamp = new Date(echo.timestamp);
    if (isNaN(alignedTimestamp.getTime())) {
      return new AlignmentError('Invalid timestamp value', echo.id, 'timestamp');
    }

    // Basic payload harmonization based on dataType (can be extended)
    let harmonizedPayload = { ...echo.payload };
    switch (echo.dataType) {
      case 'sensor_reading':
        if (typeof harmonizedPayload.temperature === 'string') {
          harmonizedPayload.temperature = parseFloat(harmonizedPayload.temperature);
        }
        if (isNaN(harmonizedPayload.temperature)) {
          // If parsing failed, keep original or set to null/default based on policy
          // For now, we'll leave it as is if it's not a number after parsing attempt
        }
        break;
      case 'resource_report':
        if (typeof harmonizedPayload.quantity === 'string') {
          harmonizedPayload.quantity = parseInt(harmonizedPayload.quantity, 10);
        }
        if (isNaN(harmonizedPayload.quantity)) {
          // Same as above
        }
        break;
      // Add more data type specific harmonizations here
    }

    return {
      id: echo.id,
      alignedTimestamp: alignedTimestamp,
      originalSource: echo.source,
      alignedType: echo.dataType,
      harmonizedPayload: harmonizedPayload,
    };
  } catch (error: any) {
    return new AlignmentError(`Failed to align echo: ${error.message}`, echo.id);
  }
}

/**
 * Merges a new AlignedData entry into an existing array of AlignedData.
 * If an entry with the same ID exists, it updates it if the new entry has a newer timestamp.
 * Otherwise, it adds the new entry.
 * @param existingData An array of existing AlignedData.
 * @param newData The new AlignedData entry to merge.
 * @returns A new array with the merged data.
 */
export function mergeAlignedData(existingData: AlignedData[], newData: AlignedData): AlignedData[] {
  const existingIndex = existingData.findIndex(d => d.id === newData.id);

  if (existingIndex !== -1) {
    // If new data is newer, replace the existing entry
    if (newData.alignedTimestamp.getTime() > existingData[existingIndex].alignedTimestamp.getTime()) {
      const updatedData = [...existingData];
      updatedData[existingIndex] = newData;
      return updatedData;
    } else {
      // New data is older or same, keep existing entry
      return existingData;
    }
  } else {
    // No existing data with this ID, add it
    return [...existingData, newData];
  }
}
