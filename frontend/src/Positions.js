
import React, { useEffect, useState } from 'react';
import { getPositions } from './api';

const Positions = () => {
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    const fetchPositions = async () => {
      const data = await getPositions();
      setPositions(data);
    };
    fetchPositions();
  }, []);

  return (
    <div>
      <h1>Positions</h1>
      <ul>
        {positions.map((position, index) => (
          <li key={index}>{position.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Positions;
