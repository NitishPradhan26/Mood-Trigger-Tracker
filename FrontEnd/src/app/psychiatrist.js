'use client';
import React, { useState, useEffect } from 'react';
import { clientService } from '../services/api';
import styles from './psychiatrist.module.css';
import { LineChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Line, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';

const Psychiatrist = () => {
    const [patients, setPatients] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedPatient, setSelectedPatient] = useState(null);

    // Fetch clients on mount
    useEffect(() => {
        const fetchClients = async () => {
            try {
                setLoading(true);
                const data = await clientService.getAllClients();
                setPatients(data);
            } catch (err) {
                setError('Failed to load patients. Please try again later.');
                console.error('Error:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchClients();
    }, []);

    // Fetch both histories when a patient is selected
    useEffect(() => {
        const fetchData = async () => {
            if (!selectedPatient) return;

            try {
                const fullName = `${selectedPatient.first_name} ${selectedPatient.last_name}`;
                
                // Fetch regular histories
                const [triggerHistory, moodHistory] = await Promise.all([
                    clientService.getTriggerHistory(fullName),
                    clientService.getMoodHistory(fullName)
                ]);
                
                // Fetch chart data
                const chartData = await clientService.getChartData(fullName);
                
                setSelectedPatient(prev => ({
                    ...prev,
                    triggerHistory,
                    moodHistory,
                    chartData
                }));
            } catch (err) {
                console.error('Error fetching data:', err);
                setError('Failed to load patient data');
            }
        };

        fetchData();
    }, [selectedPatient?.client_id]);

    const getMoodEmoji = (mood) => {
        switch (Number(mood)) {
            case 1: return '😢';
            case 5: return '😐';
            case 10: return '😊';
            default: return '❓';
        }
    };

    // Filter patients based on search term
    const filteredPatients = patients.filter(patient =>
        `${patient.first_name} ${patient.last_name}`
            .toLowerCase()
            .includes(searchTerm.toLowerCase())
    );

    if (loading) return <div className={styles.loading}>Loading patients...</div>;
    if (error) return <div className={styles.error}>{error}</div>;

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Patient Dashboard</h1>
            
            {/* Search Section */}
            <div className={styles.searchSection}>
                <input
                    type="text"
                    placeholder="Search patient name..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className={styles.searchInput}
                />
            </div>

            {/* Patient List */}
            <div className={styles.patientList}>
                {filteredPatients.map(patient => (
                    <div
                        key={patient.client_id}
                        className={`${styles.patientCard} ${selectedPatient?.client_id === patient.client_id ? styles.selected : ''}`}
                        onClick={() => setSelectedPatient(patient)}
                    >
                        {`${patient.first_name} ${patient.last_name}`}
                    </div>
                ))}
            </div>

            {/* Patient Details */}
            {selectedPatient && (
                <div className={styles.patientDetails}>
                    <h2 className={styles.patientName}>
                        {`${selectedPatient.first_name} ${selectedPatient.last_name}`}
                    </h2>

                    {/* Mood History */}
                    <div className={styles.section}>
                        <h3 className={styles.sectionTitle}>Mood History</h3>
                        <div className={styles.historyList}>
                            {selectedPatient.moodHistory?.map((entry, index) => (
                                <div key={index} className={styles.historyItem}>
                                    <span className={styles.date}>{entry.date}</span>
                                    <span className={styles.mood}>
                                        {getMoodEmoji(entry.mood)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Trigger History */}
                    <div className={styles.section}>
                        <h3 className={styles.sectionTitle}>Trigger History</h3>
                        <div className={styles.historyList}>
                            {selectedPatient.triggerHistory?.map((entry, index) => (
                                <div key={index} className={styles.historyItem}>
                                    <span className={styles.date}>{entry.date}</span>
                                    <span className={styles.trigger}>{entry.trigger_name}</span>
                                    <span className={styles.intensity}>
                                        Intensity: {entry.intensity}/10
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Mood and Trigger Charts */}
            {selectedPatient && (
                <div className="grid grid-cols-1 gap-8 mb-8">
                    <div className="p-4 bg-white rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-4">Patient History</h3>
                        <div className="h-[400px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={selectedPatient.moodHistory}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis 
                                        dataKey="timestamp" 
                                        tickFormatter={(timestamp) => format(new Date(timestamp), 'MM/dd HH:mm')}
                                    />
                                    <YAxis domain={[0, 10]} />
                                    <Tooltip 
                                        labelFormatter={(timestamp) => format(new Date(timestamp), 'MM/dd HH:mm')}
                                    />
                                    <Legend />
                                    <Line
                                        type="monotone"
                                        dataKey="value"
                                        name="Mood"
                                        stroke="#8884d8"
                                        activeDot={{ r: 8 }}
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Psychiatrist;
