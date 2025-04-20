// src/components/Logout.jsx
import React from 'react';
import {auth} from '../firebase';

function Logout() {
  const handleLogout = () => {
    auth().signOut();
    alert('Logged out successfully!');
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Logout;
