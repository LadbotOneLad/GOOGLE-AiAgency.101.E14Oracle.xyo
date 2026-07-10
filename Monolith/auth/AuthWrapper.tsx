import React, { useState } from 'react';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';

export default function AuthWrapper() {
  const [mode, setMode] = useState('login');
  return (
    <div className='auth-shell'>
      <div className='auth-toggle'>
        <button onClick={() => setMode('login')}>Login</button>
        <button onClick={() => setMode('signup')}>Signup</button>
      </div>
      {mode === 'login' ? <LoginForm /> : <SignupForm />}
    </div>
  );
}
