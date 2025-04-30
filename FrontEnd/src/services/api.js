// Define base URL as a constant
const API_BASE_URL = 'http://127.0.0.1:5000';

const DEFAULT_HEADERS = {
    'Content-Type': 'application/json'
};

// API error handler
class APIError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
        this.name = 'APIError';
    }
}

// API services
export const clientService = {
    // Record mood entry
    recordMood: async (clientId, mood) => {
        console.log('reached record mood before api call')
        try {
            // Log the full URL and request data
            console.log('Making request to:', `${API_BASE_URL}/mood`)
            console.log('Request data:', { client_id: clientId, mood: mood })
            
            const response = await fetch(`${API_BASE_URL}/mood`, {
                method: 'POST',
                headers: DEFAULT_HEADERS,
                body: JSON.stringify({
                    client_id: clientId,
                    mood: mood
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Server error:', errorData);
                throw new APIError('Failed to record mood', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Mood recording error:', error);
            throw error;
        }
    },

    // Record trigger entry
    recordTrigger: async (triggerName, intensity) => {
        try {
            const response = await fetch(`${API_BASE_URL}/trigger-history`, {
                method: 'POST',
                headers: DEFAULT_HEADERS,
                body: JSON.stringify({
                    trigger_name: triggerName,
                    intensity: intensity
                })
            });

            if (!response.ok) {
                throw new APIError('Failed to record trigger', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Trigger recording error:', error);
            throw error;
        }
    },

    // Get all clients
    getAllClients: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/clients`);
            
            if (!response.ok) {
                throw new APIError('Failed to fetch clients', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching clients:', error);
            throw error;
        }
    },

    // Get client's trigger history
    getTriggerHistory: async (fullName) => {
        try {
            const response = await fetch(`${API_BASE_URL}/trigger-history/${fullName}`);
            
            if (!response.ok) {
                throw new APIError('Failed to fetch trigger history', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching trigger history:', error);
            throw error;
        }
    },

    // Get client's mood history
    getMoodHistory: async (fullName) => {
        try {
            console.log('reached get mood history before api call')
            const response = await fetch(`${API_BASE_URL}/mood-history/${fullName}`);
            
            if (!response.ok) {
                throw new APIError('Failed to fetch mood history', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching mood history:', error);
            throw error;
        }
    },

    // Get all triggers
    getAllTriggers: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/triggers`);
            
            if (!response.ok) {
                throw new APIError('Failed to fetch triggers', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching triggers:', error);
            throw error;
        }
    },

    // Record triggers batch
    recordTriggersBatch: async (triggers) => {
        try {
            const response = await fetch(`${API_BASE_URL}/trigger-history/batch`, {
                method: 'POST',
                headers: DEFAULT_HEADERS,
                body: JSON.stringify({ triggers })
            });

            if (!response.ok) {
                throw new APIError('Failed to record triggers', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Trigger recording error:', error);
            throw error;
        }
    },

    // Get chart data for a client
    getChartData: async (fullName) => {
        try {
            const response = await fetch(`${API_BASE_URL}/chart-data/${fullName}`);
            
            if (!response.ok) {
                throw new APIError('Failed to fetch chart data', response.status);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching chart data:', error);
            throw error;
        }
    },
}; 