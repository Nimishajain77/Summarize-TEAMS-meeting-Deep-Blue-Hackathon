import React from "react";
import {useState} from 'react'
import {Api} from './Api'
function TranscriptSummarize() {
  const {transcript,setTranscript}=useState('');
  const[summary,setSummary]=useState('');

  const handleSubmit=async(e)=>{
   e.preventDefault();
   const summary=await Api(transcript);
   setSummary(summary);
  }
  return (
    <div className="px-4 mx-auto max-w-2xl lg:mb-16">
      <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">
        Summarize a Transcript
      </h2>
      <form onSubmit={handleSubmit}>
        <div className="grid gap-4 sm:grid-cols-2 sm:gap-6">
          <div className="sm:col-span-2 flex items-center justify-center w-full">
            {' '}
            
            {/* <label
              htmlFor="dropzone-file"
              className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
            >
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  aria-hidden="true"
                  className="w-10 h-10 mb-3 mt-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  ></path>
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mb-5">
                  TXT, DOC, DOCX or PDF (MAX. 10MB)
                </p>
              </div>
              <input id="dropzone-file" type="file" className="hidden" />
            </label>*/}
            <label htmlFor="transcript">Meeting Transcript:</label>
            <textarea
              id="transcript"
              name="transcript"
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
            />
            <br />
          </div>
          {/* <p className="text-sm text-gray-500 dark:text-gray-300">
            TXT, DOC, DOCX or PDF (MAX. 10MB)
          </p> */}
        </div>
        <button
          type="submit"
          className="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800"
        >
          Summarize
        </button>
      </form>
    </div>
  );
}

export default TranscriptSummarize;
