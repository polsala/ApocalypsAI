import React, { useState, useEffect } from 'react';
import { fetchResources, fetchSurvivalOdds, fetchThreatLevel, fetchAlerts } from '../utils/mockApi';

const Dashboard = () => {
  const [resources, setResources] = useState({});
  const [survivalOdds, setSurvivalOdds] = useState(0);
  const [threatLevel, setThreatLevel] = useState('medium');
  const [alert, setAlert] = useState('');
  const [loading, setLoading] = useState(true);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [resData, oddsData, threatData, alertData] = await Promise.all([
        fetchResources(),
        fetchSurvivalOdds(),
        fetchThreatLevel(),
        fetchAlerts()
      ]);
      setResources(resData);
      setSurvivalOdds(oddsData);
      setThreatLevel(threatData);
      setAlert(alertData);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
      setAlert("Failed to load critical survival data. Improvise!");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
    const intervalId = setInterval(loadDashboardData, 15000); // Refresh data every 15 seconds
    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  const getThreatLevelClass = (level) => {
    switch (level) {
      case 'low': return 'threat-low';
      case 'medium': return 'threat-medium';
      case 'high': return 'threat-high';
      default: return '';
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-card">
        <h3 className="card-title">Resource Status</h3>
        {loading ? (
          <p>Scavenging for supplies...</p>
        ) : (
          <ul className="resource-list">
            <li>Canned Goods: {resources.cannedGoods || 0}</li>
            <li>Clean Water: {resources.cleanWater || 0}</li>
            <li>Ammunition: {resources.ammo || 0}</li>
            <li>Medical Supplies: {resources.medicalSupplies || 0}</li>
          </ul>
        )}
      </div>

      <div className="dashboard-card">
        <h3 className="card-title">Survival Odds</h3>
        {loading ? (
          <p>Calculating probabilities...</p>
        ) : (
          <p className="survival-odds-value">{survivalOdds}%</p>
        )}
      </div>

      <div className="dashboard-card">
        <h3 className="card-title">Threat Level</h3>
        {loading ? (
          <p>Assessing environment...</p>
        ) : (
          <p className={`threat-level-indicator ${getThreatLevelClass(threatLevel)}`}>
            {threatLevel.toUpperCase()}
          </p>
        )}
      </div>

      <div className="dashboard-card">
        <h3 className="card-title">Whispers from the Void</h3>
        {loading ? (
          <p>Listening for cosmic murmurs...</p>
        ) : (
          <p className="alert-message">{alert || 'Silence... for now.'}</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
