import React, { useState, useEffect } from 'react';
import { clientService } from '../services/api';
import styles from './client.module.css';
import Vapi from "@vapi-ai/web";


const Client = () => {
    const [mood, setMood] = useState(null);
    const [triggerIntensity, setTriggerIntensity] = useState(5);
    const [selectedTrigger, setSelectedTrigger] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [triggers, setTriggers] = useState([]);


    // Initialize Vapi with API key
    const API_KEY = process.env.NEXT_PUBLIC_VAPI_SDK_KEY;
    const API_KEY_RESTENDPOINT = process.env.NEXT_PUBLIC_VAPI_REST_KEY;
    const vapi = new Vapi(API_KEY);

 
    // Fetch triggers on component mount
    useEffect(() => {
        const fetchTriggers = async () => {
            try {
                const data = await clientService.getAllTriggers();
                setTriggers(data);
            } catch (err) {
                console.error('Failed to fetch triggers:', err);
                setError('Failed to load triggers');
            }
        };

        fetchTriggers();
    }, []); // Empty dependency array means this runs once on mount

    

    const handleMoodSelect = (selectedMood) => {
        setMood(selectedMood);
    };

    // Convert mood emoji to number
    const convertMoodToNumber = (mood) => {
        switch (mood) {
            case 'sad': return 1;
            case 'neutral': return 5;
            case 'happy': return 10;
            default: return 5;
        }
    };

    const handleSubmit = async () => {
        setIsSubmitting(true);
        setError(null);

        try {
            // Record mood
            await clientService.recordMood(1, convertMoodToNumber(mood));

            // Record trigger if selected
            if (selectedTrigger) {
                await clientService.recordTrigger(selectedTrigger, triggerIntensity);
            }

            // Clear form on success
            setMood(null);
            setSelectedTrigger('');
            setTriggerIntensity(5);
            
            // Optional: Show success message
            alert('Entry recorded successfully!');

        } catch (error) {
            setError(error.message);
            alert('Failed to record entry. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleVoiceCall = async () => {
        const callConfig = {
            assistantId: process.env.NEXT_PUBLIC_VAPI_ASSISTANT_ID,
            phoneNumberId: process.env.NEXT_PUBLIC_VAPI_PHONE_ID,
            customer: {
                number: "+14039264437"
            },
            assistantOverrides: {
                variableValues: {
                    name: "Nitish",
                    triggers: triggers.map(t => t.name)
                }
            }
        };
        
        try {
            const response = await fetch('https://api.vapi.ai/call', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${API_KEY_RESTENDPOINT}`,  // Use API_KEY directly
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(callConfig)
            });

            if (!response.ok) {
                throw new Error('Failed to initiate call');
            }

            console.log('Call initiated successfully');
        } catch (error) {
            console.error('Voice call error:', error);
            setError('Failed to start voice call');
        }
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>How are you feeling today?</h1>
            
            {/* Mood Selection */}
            <div className={styles.moodSection}>
                <h2 className={styles.sectionTitle}>Select your mood:</h2>
                <div className={styles.moodButtons}>
                    <button 
                        onClick={() => handleMoodSelect('sad')}
                        className={`${styles.moodButton} ${mood === 'sad' ? styles.selected : ''}`}
                    >
                        😢
                    </button>
                    <button 
                        onClick={() => handleMoodSelect('neutral')}
                        className={`${styles.moodButton} ${mood === 'neutral' ? styles.selected : ''}`}
                    >
                        😐
                    </button>
                    <button 
                        onClick={() => handleMoodSelect('happy')}
                        className={`${styles.moodButton} ${mood === 'happy' ? styles.selected : ''}`}
                    >
                        😊
                    </button>
                </div>
            </div>

            {/* Trigger Selection */}
            <div className={styles.triggerSection}>
                <h2 className={styles.sectionTitle}>What triggered this feeling?</h2>
                <select 
                    value={selectedTrigger}
                    onChange={(e) => setSelectedTrigger(e.target.value)}
                    className={styles.triggerSelect}
                >
                    <option value="">Select a trigger</option>
                    {triggers.map(trigger => (
                        <option key={trigger.trigger_id} value={trigger.name}>
                            {trigger.name} - {trigger.feelings}
                        </option>
                    ))}
                </select>

                {selectedTrigger && (
                    <div className={styles.intensitySection}>
                        <h2 className={styles.sectionTitle}>How strong was this trigger? (1-10)</h2>
                        <div className={styles.intensityControl}>
                            <input
                                type="range"
                                min="1"
                                max="10"
                                value={triggerIntensity}
                                onChange={(e) => setTriggerIntensity(Number(e.target.value))}
                                className={styles.slider}
                            />
                            <span className={styles.intensityValue}>{triggerIntensity}</span>
                        </div>
                    </div>
                )}
            </div>

            {error && <div className={styles.error}>{error}</div>}
            
            <button 
                onClick={handleSubmit}
                className={styles.submitButton}
                disabled={!mood || !selectedTrigger || isSubmitting}
            >
                {isSubmitting ? 'Saving...' : 'Save Entry'}
            </button>

            <div className={styles.voiceSection}>
                <p className={styles.voiceDescription}>
                    Want to talk instead? Use our Voice Agent to discuss your feelings and triggers.
                </p>
                <button 
                    onClick={handleVoiceCall}
                    className={`${styles.submitButton} ${styles.voiceButton}`}
                >
                    Call Patient
                </button>
            </div>
        </div>
    );
};

export default Client;
