import React, { useEffect } from 'react';

function Home() {
  useEffect(() => {
    console.log('Home component rendered');
  }, []);

  return (
    <div>
      <h1>Home Page</h1>
      <p>Welcome to our website!</p>
    </div>
  );
}

export default Home;