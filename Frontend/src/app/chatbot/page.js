"use client";

import useGenerateAnswer from "@/hooks/GenerateAnswer";

import { FaArrowRight } from "react-icons/fa";

export default function Chatbot() {
  const {
    handleClick,
    isStreaming,
    answer,
    prompt,
    setPrompt,
    chats,
    isLoading,
  } = useGenerateAnswer();

  return (
    <div className="flex flex-col justify-center min-h-screen min-w-full items-center text-white">
      {chats?.map((e, i) => {
        return (
          <div key={i} className="flex flex-col w-[80vw] my-7">
            <div className="font-bold text-3xl">{e.prompt}</div>
            <div className="rounded-lg w-[80vw] p-5 h-auto bg-[#1E1E1E] m-8">
              {e.answer}
            </div>
            <hr></hr>
          </div>
        );
      })}

      {isStreaming && (
        <div className="w-[80vw] rounded-lg p-5 h-auto bg-[#1E1E1E] m-8 ">
          {answer}
        </div>
      )}

      

      {isLoading && (
        <div
          className="loader border-t-2 rounded-full border-gray-500 bg-gray-300 animate-spin
aspect-square w-8 my-9 flex justify-center items-center text-yellow-700"
        ></div>
      )}

      <form disabled = {isLoading || isStreaming} className="flex justify-between border-2 border-orange-500 w-[70vw] h-[5vw] rounded-lg">
        <input
          onChange={(e) => setPrompt(e.target.value)}
          value={prompt}
          className="bg-transparent focus:outline-none w-full ml-4"
          placeholder="Enter your prompt"
        />

        <button
          onClick={handleClick}
          disabled={prompt.trim().length === 0 || isStreaming || isLoading}
          className=" disabled:opacity-20 overflow-hidden duration-100 active:scale-95 mr-5"
        >
          <FaArrowRight className="h-8 w-8  text-[#F37022] rounded-full duration-200 hover:text-white hover:bg-orange-500" />
        </button>
      </form>
    </div>
  );
}
