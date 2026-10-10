const LOCAL_STORAGE_KEY = 'temporalAnomalies';

/**
 * Loads anomalies from local storage.
 * @returns {Array} An array of anomaly objects.
 */
export const loadAnomalies = () => {
  try {
    const serializedState = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (serializedState === null) {
      return [];
    }
    return JSON.parse(serializedState);
  } catch (error) {
    console.error("Error loading anomalies from local storage:", error);
    return [];
  }
};

/**
 * Saves anomalies to local storage.
 * @param {Array} anomalies - An array of anomaly objects to save.
 */
export const saveAnomalies = (anomalies) => {
  try {
    const serializedState = JSON.stringify(anomalies);
    localStorage.setItem(LOCAL_STORAGE_KEY, serializedState);
  } catch (error) {
    console.error("Error saving anomalies to local storage:", error);
  }
};
