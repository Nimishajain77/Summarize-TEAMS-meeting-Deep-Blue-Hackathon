import React, { useState } from "react";
import table from "../utils/table";
import EditModal from "./EditModal";

function Table() {
  const [showEditModal, setShowEditModal] = useState(false);

  return (
    <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <caption className="p-5 text-lg font-semibold text-left text-gray-900 bg-white dark:text-white dark:bg-gray-800">
        Summarized Transcripts
        <p className="mt-1 text-sm font-normal text-gray-500 dark:text-gray-400">
          This table contains a summary of all transcripts in the database.
          Click on a transcript name or the size or the date to sort by size.
          Click on the actions to edit or delete a transcript.
        </p>
      </caption>
      <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" className="py-3 px-6">
            Transcript Name
          </th>
          <th scope="col" className="py-3 px-6">
            <div className="flex items-center">
              Date
              <a href="#">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="ml-1 w-3 h-3"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 320 512"
                >
                  <path d="M27.66 224h264.7c24.6 0 36.89-29.78 19.54-47.12l-132.3-136.8c-5.406-5.406-12.47-8.107-19.53-8.107c-7.055 0-14.09 2.701-19.45 8.107L8.119 176.9C-9.229 194.2 3.055 224 27.66 224zM292.3 288H27.66c-24.6 0-36.89 29.77-19.54 47.12l132.5 136.8C145.9 477.3 152.1 480 160 480c7.053 0 14.12-2.703 19.53-8.109l132.3-136.8C329.2 317.8 316.9 288 292.3 288z" />
                </svg>
              </a>
            </div>
          </th>
          <th scope="col" className="py-3 px-6">
            <div className="flex items-center">
              Type of File
              <a href="#">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="ml-1 w-3 h-3"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 320 512"
                >
                  <path d="M27.66 224h264.7c24.6 0 36.89-29.78 19.54-47.12l-132.3-136.8c-5.406-5.406-12.47-8.107-19.53-8.107c-7.055 0-14.09 2.701-19.45 8.107L8.119 176.9C-9.229 194.2 3.055 224 27.66 224zM292.3 288H27.66c-24.6 0-36.89 29.77-19.54 47.12l132.5 136.8C145.9 477.3 152.1 480 160 480c7.053 0 14.12-2.703 19.53-8.109l132.3-136.8C329.2 317.8 316.9 288 292.3 288z" />
                </svg>
              </a>
            </div>
          </th>
          <th scope="col" className="py-3 px-6">
            <div className="flex items-center">
              Summarization
              <a href="#">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="ml-1 w-3 h-3"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 320 512"
                >
                  <path d="M27.66 224h264.7c24.6 0 36.89-29.78 19.54-47.12l-132.3-136.8c-5.406-5.406-12.47-8.107-19.53-8.107c-7.055 0-14.09 2.701-19.45 8.107L8.119 176.9C-9.229 194.2 3.055 224 27.66 224zM292.3 288H27.66c-24.6 0-36.89 29.77-19.54 47.12l132.5 136.8C145.9 477.3 152.1 480 160 480c7.053 0 14.12-2.703 19.53-8.109l132.3-136.8C329.2 317.8 316.9 288 292.3 288z" />
                </svg>
              </a>
            </div>
          </th>
          <th scope="col" className="py-3 px-6"></th>
        </tr>
      </thead>
      <tbody>
        {table.map((row) => (
          <tr
            key={row.name}
            className="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            <th
              scope="row"
              className="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
            >
              {row.name}
            </th>
            <td className="py-4 px-6">{row.date}</td>
            <td className="py-4 px-6">{row.type}</td>
            <td className="py-4 px-6">{row.summarize}</td>
            <td className="py-4 px-6">
              <button
                type="button"
                className="mr-2 font-medium text-green-600 dark:text-green-500 hover:underline"
              >
                Download
              </button>
              <button
                type="button"
                onClick={() => setShowEditModal(true)}
                className="mr-2 font-medium text-blue-600 dark:text-blue-500 hover:underline"
              >
                Edit
              </button>
              {showEditModal && (
                <EditModal setOpenEditModal={setShowEditModal} />
              )}
              <button
                type="button"
                className="font-medium text-red-600 dark:text-red-500 hover:underline"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Table;
