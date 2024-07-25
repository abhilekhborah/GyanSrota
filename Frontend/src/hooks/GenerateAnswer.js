import { useState, useRef } from "react";
import axios from "axios";

import examples from "@/app/chatbot/examples";

export default function useGenerateAnswer() {
  const [isLoading, setIsLoading] = useState(false);

  const [isStreaming, setIsStreaming] = useState(false);

  const [chats, setChats] = useState([]);

  const [prompt, setPrompt] = useState("");

  const [answer, setAnswer] = useState("");

  let i = useRef(-10);
  let intervalId = useRef(null);

  const handleClick = async (e) => {
    e.preventDefault();

    setIsLoading(true);

    let response = await axios.post("http://127.0.0.1:5000/ask", {
      prompt: prompt,
    });

    setIsLoading(false);

    setIsStreaming(true);
    //setting the value of i to -10, to start from the beginning of the string
    i.current = -10;

    //Splitting the long string into individual characters
    let reply = response.data.answer.split("");

    //Setting interval to stream the answer
    intervalId.current = setInterval(() => {
      //setting the messages to the first 10 characters
      setAnswer((prev) => {
        const nextChunk = reply.slice(i.current, i.current + 10).join("");

        return prev + nextChunk;
      });

      //incrementing the value of i, to get the next 10 characters
      i.current = i.current + 10;

      if (i.current > reply.length) {
        clearInterval(intervalId.current);
        setIsStreaming(false);
        setChats((prev) => [...prev, { prompt, answer: response.data.answer }]);
        setPrompt("");
        setAnswer("");
      }
    }, 20);
  };

  return {
    handleClick,
    isStreaming,
    answer,
    prompt,
    setPrompt,
    setAnswer,
    chats,
    isLoading,
  };
}
