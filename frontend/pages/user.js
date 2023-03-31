import React from "react";
import TranscriptSummarize from "../userComponents/TranscriptSummarize";
import SpeechSummarize from "../userComponents/SpeechSummarize";
import Table from "../userComponents/Table";
import Pagination from "../userComponents/Pagination";

function user() {
  return (
    <section className="dashboard bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col justify-center py-8 px-4 mx-auto max-w-screen-xl sm:py-16 lg:px-6">
        <div className="overflow-x-auto overflow-y-hidden relative">
          <div className="grid grid-cols-2 gap-4">
            <TranscriptSummarize></TranscriptSummarize>
            <SpeechSummarize></SpeechSummarize>
          </div>
          <Table></Table>
          <Pagination></Pagination>
        </div>
      </div>
    </section>
  );
}

export default user;
