const API_URL = 'http://192.168.156.131:5678';

export const getPositions = async () => {
  try {
    const response = await fetch(`${API_URL}/positions`);


    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching positions:', error);
    return null;
  }
};
