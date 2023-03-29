import React from "react";
import Footer from "./Footer";
import Header from "./Header";
// import supabaseClient from "../config/client";

function Layout({ children }) {
  return (
    <>
      <div className="dark">
        {/* <Header supabaseClient={supabaseClient} /> */}
        <main>{children}</main>
        <Footer />
      </div>
    </>
  );
}

export default Layout;
