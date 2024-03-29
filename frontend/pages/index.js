import Head from "next/head";
import { Inter } from "@next/font/google";
import Hero from "../homeComponents/Hero";
import Feature from "../homeComponents/Feature";
import About from "../homeComponents/About";
import Summarize from "../homeComponents/Summarize";
import Team from "../homeComponents/Team";
const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      <Head>
        <title>STM</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Hero></Hero>
      <Feature></Feature>
      <About></About>
      <Summarize></Summarize>
      <Team></Team>
    </>
  );
}
