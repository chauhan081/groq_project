// src/components/Login.jsx
import React, { useState } from 'react';
import { auth } from '../firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      await signInWithEmailAndPassword(auth, email, password);
      alert('Logged in successfully!');
      navigate('/chat'); // ✅ login success hone par chat pe redirect
    } catch (err) {
      setError(err.message);

      // ❌ Agar error user-not-found ho to signup page par redirect karo
      if (err.code === 'auth/user-not-found') {
        setTimeout(() => {
          navigate('/signup');
        }, 2000); // 2 sec wait before redirect
      }
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          style={{ display: 'block', width: '100%', marginBottom: '10px' }}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          style={{ display: 'block', width: '100%', marginBottom: '10px' }}
        />
        <button type="submit" style={{ width: '100%' }}>Login</button>
      </form>

      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

      <hr style={{ margin: '20px 0' }} />

      <p>
        Don&apos;t have an account?{' '}
        <button onClick={() => navigate('/signup')} style={{ color: 'blue', background: 'none', border: 'none', cursor: 'pointer' }}>
          Signup here
        </button>
      </p>
    </div>
  );
}

export default Login;
