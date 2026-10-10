const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFFT }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFFT(onPerfEntry);
    });
  }
};

export default reportWebVitals;
