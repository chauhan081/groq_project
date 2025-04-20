// src/components/AuthStatus.jsx
import React, { useState, useEffect } from 'react';
import {auth} from '../firebase';

function AuthStatus() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = auth().onAuthStateChanged(setUser);
    return () => unsubscribe();
  }, []);

  if (user) {
    return (
      <div>
        <h2>Welcome, {user.email}</h2>
      </div>
    );
  }

  return <div>Please log in to access your account.</div>;
}

export default AuthStatus;
