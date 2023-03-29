import React from 'react';


// export async function Api(transcript) {
//   const response = await fetch('http://localhost:5000/summarize', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ transcript }),
//   });
//   const data = await response.json();
//   return data.summary;
// }

// export default Api;

import axios from 'axios';

export async function Api(transcript) {
  try {
    const response = await axios.post('http://127.0.0.1:5000/summarize', {
      transcript,
    });
    return response.data.summary;
  } catch (error) {
    console.error(error);
    throw error;
  }
}