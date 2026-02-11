import mockEvents from '../data/mock_data.json';
import mockValidations from '../data/mock_validations.json';

const API_BASE = '/api';

export async function fetchEvents() {
  try {
    const response = await fetch(`${API_BASE}/events`);
    if (!response.ok) throw new Error('Failed to fetch events');
    const data = await response.json();
    return data.data || data;
  } catch (error) {
    console.warn('API unavailable, using mock data:', error.message);
    return mockEvents;
  }
}

export async function fetchEvent(eventId) {
  try {
    const response = await fetch(`${API_BASE}/events/${eventId}`);
    if (!response.ok) throw new Error('Failed to fetch event');
    return await response.json();
  } catch (error) {
    console.warn('API unavailable, using mock data:', error.message);
    return mockEvents.find((e) => e.event_id === eventId) || null;
  }
}

export async function fetchValidations() {
  try {
    const response = await fetch(`${API_BASE}/validations`);
    if (!response.ok) throw new Error('Failed to fetch validations');
    const data = await response.json();
    return data.data || data;
  } catch (error) {
    console.warn('API unavailable, using mock validations:', error.message);
    return mockValidations;
  }
}

export async function fetchPrice(ticker, range = '1d') {
  try {
    const response = await fetch(`${API_BASE}/price?ticker=${ticker}&range=${range}`);
    if (!response.ok) throw new Error('Failed to fetch price data');
    return await response.json();
  } catch (error) {
    console.warn('Price API unavailable:', error.message);
    // Return mock price data
    return {
      ticker,
      prices: Array.from({ length: 24 }, (_, i) => ({
        time: new Date(Date.now() - (24 - i) * 3600000).toISOString(),
        price: 100 + Math.sin(i * 0.5) * 5 + Math.random() * 2,
      })),
    };
  }
}

// For demo mode, just return mock data directly
export function getMockEvents() {
  return mockEvents;
}

export function getMockValidations() {
  return mockValidations;
}
