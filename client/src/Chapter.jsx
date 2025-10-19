import { useEffect, useState } from "react";
import { Button } from '@/components/ui/button';
import { useLocation, useParams } from 'react-router-dom'
import NavBar from "./NavBar";
import ScrollToTopButton from "./ScrollToTopButton";

async function getChapterIntro(key) {
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      const response = await fetch(`https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/intro?ch-key=${key}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        } 
      });

      return await response.json();
    } catch (error) {

      console.error('Error:', error);
      throw error;
    }
}

async function makeChapterEnd(option, key) {
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      await fetch(`https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/end`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          "ch-key": key,
          "choice": option 
        })
      });
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
}

async function getChapterEnd(key) {
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      let response = await fetch(`https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/end?ch-key=${key}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      return await response.json()
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
}

function Chapter() {
  const [intro, setIntro] = useState("");
  const [end, setEnd] = useState("");
  const [options, setOptions] = useState([]);
  const [choice, setChoice] = useState("");
  const [showOptions, setShowOptions] = useState(false);
  const [showEnd, setShowEnd] = useState(false);
  const { state } = useLocation();
  const chapterNum = state.number;
  const params = useParams();

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
    async function run () {
      let key = params["key"]
      let data = await getChapterIntro(key);
      setIntro(data.content);
      setOptions(data.options);
    }
    run();
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
    setIntro(introData.content);
    setOptions(introData.options);
    /*
    // Get end data. If end data returns a 404, then we will show the options
    let endData = {}
    let showOptions = false;
    if (Object.keys(endData).length === 0) {
      showOptions = true;
    } else {
      setEnd(endData.content);
      setChoice(endData.option);
    }

    setShowOptions(showOptions);
    setShowEnd(!showOptions);
    */
  }, []);

  async function handleOptionClick(option) {
    
    setShowOptions(false);
    await makeChapterEnd(option, key);
    let data = getChapterEnd(key);
    setChoice(data.option);
    setEnd(data.content);

    let endData = {
      ch_key: "my-random-key",
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
    }
    setEnd(endData.content);
    setShowEnd(true);
  };

  return (
    <>
      <NavBar/>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8 flex flex-col items-center justify-center">
        <div className="max-w-2xl w-full">
          <h1 className="text-left text-4xl font-bold text-slate-900 mb-8">Chapter {chapterNum}</h1>
          <div className="text-left text-xl lg:text-2xl [word-spacing:0.1em] leading-relaxed text-slate-900 mb-16">
            {getFormattedText(intro)}
          </div>

          {showOptions && (
            <div className="flex flex-col items-center gap-12 mb-8">
              <div className="flex flex-wrap gap-8 justify-center">
                {options.map((option, index) => (
                  <Button
                    key={index}
                    onClick={() => handleOptionClick(option)}
                    className="text-white font-semibold py-2 px-6 rounded-lg
                              transform transition duration-300 ease-in-out
                              hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                              active:scale-95 active:bg-amber-700 cusror-pointer"
                  >
                    {option}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {choice.length > 0 && (
            <div className="text-2xl word-spacing:0.1em] text-center mb-8 text-slate-700 animate-fade-in">
              You chose: <span className="font-bold text-slate-900">{choice}</span>
            </div>
          )}

          {showEnd && (
            <div className="text-left text-xl lg:text-2xl [word-spacing:0.1em] leading-relaxed text-slate-900 mb-16">
              {getFormattedText(end)}
            </div>
          )}

          <ScrollToTopButton />

        </div>
      </div>
    </>
  );
}

export default Chapter;