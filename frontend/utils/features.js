const features = [
  {
    svgPath:
      "M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z",
    name: "Count of Attendees",
    desc: "Parse the transcript to figure out many attendees were there in the meeting.",
  },
  {
    svgPath: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
    name: "Time Duration",
    desc: "Parse the transcript to figure out the time duration of the meeting.",
  },
  {
    svgPath:
      "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    name: "Summary",
    desc: "Parse the Transcript to figure out and most importantly produce a gist/summary of the meeting.",
  },
  {
    svgPath:
      "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z",
    name: "Actionable Items",
    desc: "Parse the Transcript to figure out and list the action items if they are specifically called out.",
  },
  {
    svgPath:
      "M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z",
    name: "Speech-to-Text",
    desc: "Incase where Transcript is not available, we will additionally provide help in converting the Speech to Text.",
  },
  {
    svgPath:
      "M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    name: "Modifications",
    desc: "The gist or summary may not be exactly right but can give autosuggestions for the organizer to fill in certain details.",
  },
];

export default features;
