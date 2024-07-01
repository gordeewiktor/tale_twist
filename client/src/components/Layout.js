import React from 'react';
import Header from './Header';
import NavBar from './NavBar';
import FlashMessages from './FlashMessages';
import Footer from './Footer';
import './Layout.css'; // Import CSS for Layout if you have specific styles

const Layout = ({ children, isAuthenticated }) => {
  return (
    <div>
      <Header />
      <NavBar isAuthenticated={isAuthenticated} />
      <FlashMessages />
      <main>{children}</main>
      <Footer />
    </div>
  );
};

export default Layout;
