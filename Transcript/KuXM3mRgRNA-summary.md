# Stop paying for video editors — do this instead

- Video: https://www.youtube.com/watch?v=KuXM3mRgRNA
- Creator: Hasan Aboul Hasan
- Duration: 6:28
- Note: Detailed transcript summary, not a verbatim reproduction.

## Timestamped summary

- **0:00–0:52:** The creator claims the example video was edited end-to-end with Claude and code, including animations, simulated screen recordings, music, sound effects, thumbnail, and upload automation. The only recorded element is the presenter.
- **0:52–1:12:** He offers the code project for free and frames it as a complete editing engine rather than a silence-cutting demo.
- **1:12–2:18:** Step 1 is cleaning the raw recording. AssemblyAI transcribes it; a Claude skill removes silence, filler words, and bad takes. He argues this edit must be accurate because later stages depend on its timing.
- **2:18–3:14:** Step 2 generates visuals. Claude creates motion graphics, a simulated VS Code interface, cursor movement, clicks, page changes, and changing URLs instead of conventional screen recordings.
- **3:14–3:38:** Step 3 applies voice isolation and audio cleanup.
- **3:38–4:19:** Step 4 adds background music and places sound effects against exact narration timestamps.
- **4:19–4:41:** Assets—including effects, screens, images, and logos—are stored in a reusable library. The claimed benefit is that later videos become faster and cheaper.
- **4:41–5:04:** Step 5 generates three title-and-thumbnail pairs for YouTube testing and is intended to learn from prior performance.
- **5:04–5:31:** Paid dependencies mentioned are AssemblyAI, ElevenLabs, and Nano Banana. The creator estimates roughly $3–$4 to edit a video, excluding development time, subscriptions, failures, and human review.
- **5:31–6:01:** Step 6 performs automated quality checks for broken cuts, undesirable words, and audio/video drift, then uploads through the YouTube API.
- **6:01–6:28:** The creator asks for feedback, promotes the open-source GitHub project, and links a paid AI-building course.

## Business assessment

- Useful as a possible production accelerator, not proof of a profitable channel.
- The $3–$4 claim needs a controlled test measuring API usage, retries, rendering, storage, setup, and human QA.
- Strongest idea: reusable assets and skills reduce marginal production cost over time.
- Main risks: generated visuals may look generic, automated cuts may damage pacing, and unattended upload increases quality and policy risk.
- We should test this workflow on one pilot before adopting the full stack.
