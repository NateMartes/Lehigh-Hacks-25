import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Button } from '@/components/ui/button';
import NavBar from "./NavBar";

function Chapter() {
  const [intro, setIntro] = useState("");
  const [end, setEnd] = useState("");
  const [options, setOptions] = useState([]);
  const [choice, setChoice] = useState("");
  const [showOptions, setShowOptions] = useState(false);
  const [showEnd, setShowEnd] = useState(false);
  const { state } = useLocation();
  const chapterNum = state.number;

  function getFormattedText(text) {
    const paragraphLength = 5;

    const sentences = text.split('.').map(s => s.trim()).filter(Boolean);

    const paragraphs = [];
    for (let i = 0; i < sentences.length; i += paragraphLength) {
      const chunk = sentences.slice(i, i + paragraphLength).join('. ');
      paragraphs.push(chunk.endsWith('.') ? chunk : chunk + '.');
    }

    return (
      <>
        {paragraphs.map((paragraph, idx) => (
          <p className="mb-4" key={idx}>{paragraph}</p>
        ))}
      </>
    );
  }


  useEffect(() => {
    let chKey = "ch1";
    let introData = {
      ch_key: chKey,
      content: `Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.`,
      options: [
        "Do option A",
        "Do option B",
        "Do option C"
      ]
    };

    // Get end data. If end data returns a 404, then we will show the options
    let endData = {
      /*
      ch_key: chKey,
      content: `Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.Welcome to the world of coding! Learning React is one of the best ways to build modern web applications.
                React allows developers to create reusable UI components, making development faster and easier to maintain.
                With a bit of practice, you'll be building interactive and dynamic user interfaces in no time.`,
      option: "Do option A"
      */
    }

    setIntro(introData.content);
    setOptions(introData.options);

    let showOptions = false;
    if (Object.keys(endData).length === 0) {
      showOptions = true;
    } else {
      setEnd(endData.content);
      setChoice(endData.option);
    }

    setShowOptions(showOptions);
    setShowEnd(!showOptions);
  }, []);

  function handleOptionClick(option) {
    setChoice(option);
  };

  return (
    <>
      <NavBar/>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8 flex flex-col items-center justify-center">
        <div className="max-w-2xl w-full">
          <h1 className="text-left text-4xl font-bold text-slate-900 mb-8">Chapter {chapterNum}</h1>
          <div className="text-left text-2xl [word-spacing:0.1em] leading-relaxed text-slate-900 mb-16">
            {getFormattedText(intro)}
          </div>

          {showOptions && (
            <div className="flex flex-col items-center gap-12 mb-8">
              <div className="flex gap-8 justify-center">
                {options.map((option, index) => (
                  <Button key={index} onClick={() => handleOptionClick(option)}>{option}</Button>
                ))}
              </div>
            </div>
          )}

          {showEnd && (
            <div className="text-left text-2xl [word-spacing:0.1em] leading-relaxed text-slate-900 mb-16">
              {getFormattedText(end)}
            </div>
          )}

          {choice.length > 0 && (
            <div className="text-center mt-8 text-lg text-slate-700 animate-fade-in">
              You selected: <span className="font-bold text-slate-900">{choice}</span>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default Chapter;