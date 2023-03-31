import React from 'react';
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