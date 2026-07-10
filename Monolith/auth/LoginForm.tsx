import React from 'react';
export default function LoginForm() {
  return (
    <form className='flex flex-col gap-4'>
      <input type='email' placeholder='Email' aria-label='Email' />
      <input type='password' placeholder='Password' aria-label='Password' />
      <button>Login</button>
    </form>
  );
}
