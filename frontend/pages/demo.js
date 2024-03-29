import { useState } from 'react';
import axios from 'axios';
import { Api } from '../userComponents/Api';
import React from 'react';
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.css';

export default function Demo() {
  const [file, setFile] = useState(null);
  const [loading,setLoading] =useState(false)
  const [title,setTitle] = useState('');
  const [date,setDate] = useState('');
  const [meetingAttendees,setMeetingAttendees] = useState('');
  const [summary, setSummary] = useState('');
  const [actionItems,setActionItems] = useState('')


  const handleChange = (event) => {
    setFile(event.target.files[0]);
  };

  function validateForm(){
    const name = document.getElementById('name').value;
    if(file ==""){
      alert('Please select a file')
      return false;
    }
    // const allowedExtensions=/(\.txt)$/i;
    // if(!allowedExtensions.exec(file)){
    //   alert('Invalid file type. Only .txt files are allowed.')
    //   return false;
    // }
    // if(name === ''){
    //   alert('Please enter a name for the transcript')
    //   return false;
    // }
    return true;
  }
  
  const handleSubmitTxt = async (event) => {
    event.preventDefault();
    const isValid=validateForm();
    if(!isValid){
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:5000/summarize_txt',
        formData
      );
      setTitle(response.data.title)
      setDate(response.data.date)
      setMeetingAttendees(response.data.meetingAttendees)
      setSummary(response.data.summary);
      setActionItems(response.data.actionItems);

    } catch (error) {
      // console.error(error);
      // alert(' Oops! Something went wrong : '+error.message)
      Swal.fire({
   
        background:'#000c19',
        icon: 'error',
        title: 'Oops...',
        text: `Something went wrong: ${error.message}`,
        confirmButtonColor: '#0066ff',
        confirmButtonText: 'OK',
      });
    
    }
    finally{
      setLoading(false);
    }
  };
  const handleSubmitVtt = async (event) => {
    event.preventDefault();
    const isValid=validateForm();
    if(!isValid){
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:5000/summarize_vtt',
        formData
      );
      setTitle(response.data.title)
      setDate(response.data.date)
      setMeetingAttendees(response.data.meetingAttendees)
      setSummary(response.data.summary);
      setActionItems(response.data.actionItems);

    } catch (error) {
      // console.error(error);
      // alert(' Oops! Something went wrong : '+error.message)
      Swal.fire({
   
        background:'#000c19',
        icon: 'error',
        title: 'Oops...',
        text: `Something went wrong: ${error.message}`,
        confirmButtonColor: '#0066ff',
        confirmButtonText: 'OK',
      });
    
    }
    finally{
          setLoading(false);
        }
  };
  return (
    <section className="bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col justify-center mx-auto py-8 px-4 max-w-screen-xl sm:py-16 lg:px-6">
        <div className="grid md:grid-cols-2 sm:grid-cols-1 gap-6">
          <div>
            <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">
              Summarize a Transcript
            </h2>
            <form onSubmit={handleSubmitTxt}>
              <div className="grid gap-4 sm:grid-cols-2 sm:gap-6">
                <div className="sm:col-span-2">
                  <label
                    htmlFor="name"
                    className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                  >
                    Transcript Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    id="name"
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                    placeholder="Type transcript name"
                    required
                  />
                </div>
                <div className="sm:col-span-2 flex items-center justify-center w-full">
                  <label
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
                        <span className="font-semibold">Click to upload</span>{' '}
                        or drag and drop
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mb-5">
                        TXT, DOC, DOCX or PDF (MAX. 10MB)
                      </p>
                    </div>
                    <input
                      id="dropzone-file"
                      type="file"
                      className="hidden"
                      onChange={handleChange}
                    />
                  </label>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  TXT, DOC, DOCX or PDF (MAX. 10MB)
                </p>
              </div>
              <button
                type="submit"
                className="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800"
              >
                Summarize
              </button>
            </form>
            <div>
            {title && (
              <div className="mt-4">
                {/* <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3> */}
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {title}
                </p>
              </div>
            )}
            </div>
            <div>
            {date && (
              <div className="mt-4">
                {/* <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3> */}
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {date}
                </p>
              </div>
            )}
            </div>
            <div>
            {meetingAttendees && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {meetingAttendees}
                </p>
              </div>
            )}
            </div>
            <div>
            {summary && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {summary}
                </p>
              </div>
            )}
            </div>
            <div>
            {actionItems && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Action Items
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {actionItems}
                </p>
              </div>
            )}
            </div>
            
          </div>
          <div>
            <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">
              Summarize a Speech (Audio File)
            </h2>
            <form onSubmit={handleSubmitVtt}>
              <div className="grid gap-4 sm:grid-cols-2 sm:gap-6">
                <div className="sm:col-span-2">
                  <label
                    htmlFor="name"
                    className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                  >
                    Audio File Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    id="name"
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                    placeholder="Type audio file name"
                    required
                  />
                </div>
                <div className="sm:col-span-2 flex items-center justify-center w-full">
                  <label
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
                        <span className="font-semibold">Click to upload</span>{' '}
                        or drag and drop
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mb-5">
                        MP3, WAV, or MP4 (MAX. 10MB)
                      </p>
                    </div>
                    <input id="dropzone-file" type="file" className="hidden"  onChange={handleChange} />
                  </label>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  MP3, WAV, or MP4 (MAX. 10MB)
                </p>
              </div>
              <button
                type="submit"
                className="inline-flex items-center px-5 py-2.5 mt-4 sm:mt-6 text-sm font-medium text-center text-white bg-primary-700 rounded-lg focus:ring-4 focus:ring-primary-200 dark:focus:ring-primary-900 hover:bg-primary-800"
              >
                Summarize
              </button>
            </form>
            <div>
            {title && (
              <div className="mt-4">
                {/* <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3> */}
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {title}
                </p>
              </div>
            )}
            </div>
            <div>
            {date && (
              <div className="mt-4">
                {/* <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3> */}
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {date}
                </p>
              </div>
            )}
            </div>
            <div>
            {meetingAttendees && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {meetingAttendees}
                </p>
              </div>
            )}
            </div>
            <div>
            {summary && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Summary
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {summary}
                </p>
              </div>
            )}
            </div>
            <div>
            {actionItems && (
              <div className="mt-4">
                <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">
                  Action Items
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  {actionItems}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
      </div>
    </section>
  );
}