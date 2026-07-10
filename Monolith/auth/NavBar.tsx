import React from 'react';
export default function NavBar() {
  return (
    <nav className='w-full flex justify-center items-center py-4 bg-white shadow'>
      <ul className='flex gap-8 text-gray-700 font-medium'>
        <li>Home</li>
        <li>About</li>
        <li>Login</li>
        <li>Signup</li>
      </ul>
    </nav>
  );
}
