import { useEffect, useState } from "react";
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { useLocation, useParams } from 'react-router-dom'
import { fetchAuthSession } from 'aws-amplify/auth';
import NavBar from "./NavBar";
import ScrollToTopButton from "./ScrollToTopButton";
import TextToSpeechBtn from "./TextToSpeech";

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
  const [gettingEnd, setGettingEnd] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [showEnd, setShowEnd] = useState(false);
  const { state } = useLocation();
  const chapterNum = state.number;
  const params = useParams();

  function getFormattedText(text) {
    const paragraphLength = 5;

    console.log(`Text: ${text}`)
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
      let key = params["chKey"]
      let data = await getChapterIntro(key);
      setIntro(data.body.content);
      setOptions(data.body.options);
      let endData = await getChapterEnd(key);
      if (Object.keys(endData.body).length === 0) {
        setShowOptions(true);
      } else {
          setChoice(endData.body.choice);
          setEnd(endData.body.content);
          setShowEnd(true);
      }
    }
    run();
  }, []);

  async function handleOptionClick(option) {
    
    let key = params["chKey"]
    setShowOptions(false);
    setGettingEnd(true);
    await makeChapterEnd(option, key);
    let data = await getChapterEnd(key);
    console.log(data);
    setGettingEnd(false);
    setChoice(data.body.choice);
    setEnd(data.body.content);
    setShowEnd(true);
  };

  return (
    <>
      <NavBar/>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8 flex flex-col items-center justify-center">
        <div className="max-w-2xl w-full">
          <div className="flex items-center gap-6 mb-6">
            <h1 className="text-4xl font-bold text-slate-900">Chapter {chapterNum}</h1>
            <TextToSpeechBtn text={intro}/>
          </div>
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
                    className="w-full text-white font-semibold px-4 py-8 sm:px-6 rounded-lg
                  transform transition duration-300 ease-in-out
                hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                  active:scale-95 active:bg-amber-700 cursor-pointer
                  text-sm sm:text-base lg:text-lg
                  whitespace-normal break-words"
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

          {gettingEnd && (
            <div className="flex flex-col justify-center place-items-center gap-6">
              <Spinner className="h-12 w-12"/>
            </div>
            )}

          <ScrollToTopButton />
        </div>
      </div>
    </>
  );
}

export default Chapter;