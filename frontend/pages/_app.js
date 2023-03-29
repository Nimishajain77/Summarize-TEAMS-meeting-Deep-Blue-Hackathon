import "../styles/globals.css";
import Layout from "../layout/Layout";
import { Auth } from "@supabase/auth-ui-react";
// import supabaseClient from "../config/client";

export default function App({ Component, pageProps }) {
  return (
    <>
      {/* <Auth.UserContextProvider supabaseClient={supabaseClient}> */}
        <Layout>
          <Component {...pageProps} />
        </Layout>
      {/* </Auth.UserContextProvider> */}
    </>
  );
}
