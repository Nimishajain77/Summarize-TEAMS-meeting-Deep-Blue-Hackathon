import Image from "next/image";
import React from "react";
import Office1 from "../public/assets/officeImage1.png";
import Office2 from "../public/assets/officeImage2.png";

function About() {
  return (
    <section id="about" className="bg-white dark:bg-gray-900">
      <div className="gap-16 items-center py-8 px-4 mx-auto max-w-screen-xl lg:grid lg:grid-cols-2 lg:py-16 lg:px-6">
        <div className="font-light text-gray-500 sm:text-lg dark:text-gray-400">
          <h2 className="mb-4 text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white">
            We are accumulating all the solutions
          </h2>
          <p className="mb-4">
            Since there is no conclusive solution out there, covering all other
            aspects of the problem description while summarizing the discussion
            is really important. We can delve deeply and produce an accurate
            result and by finding a solution to this issue, we can automate
            summary and eliminate the necessity for individual note-taking.
          </p>
          <p>
            With the help of Artificial Intelligence and Machine Learning, we
            have the potential to completely revolutionize businesses by
            assisting them in achieving quantifiable results.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-4 mt-8">
          <Image
            className="w-full rounded-lg"
            src={Office2}
            alt="office content 2"
          />
          <Image
            className="mt-4 w-full lg:mt-10 rounded-lg"
            src={Office1}
            alt="office content 1"
          />
        </div>
      </div>
    </section>
  );
}

export default About;
