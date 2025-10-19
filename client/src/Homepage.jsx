import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate } from "react-router-dom";
import NavBar from './NavBar';
import { fetchAuthSession } from 'aws-amplify/auth';
import { Spinner } from '@/components/ui/spinner';
import ScrollToTopButton from './ScrollToTopButton';
import { useState, useEffect } from "react";

async function getAllChapters(updateChaptersFunc) {
    const session = await fetchAuthSession();
    const idToken = session.tokens?.idToken;
    const payload = idToken?.payload;
    const userId = payload?.sub;

    try {
      const response = await fetch(`https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/chapters?uid=${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        } 
      });

      let data = await response.json();
      setGettingChapters(false);
      updateChaptersFunc(data.chapters);

    } catch (error) {
      console.log("Error" + error);
      throw error;
    }

}

export default function ChapterList() {

  const [creatingNewChapter, setCreatingNewChapter] = useState(false);
  const [chapters, setChapters] = useState([]);
  const [gettingChapters, setGettingChapters] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function run() {
      await getAllChapters(setChapters, setGettingChapters);
    }
    run();
  }, [])
  function handleCardClick(event) {
    let key = event.currentTarget.dataset.chapter;
    let number = event.currentTarget.dataset.number;
    navigate(`/chapter/${key}`, {state: {number: number}});  
  }

  async function createNewChapter() {

    let data = {}
    setCreatingNewChapter(true);
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      const response = await fetch('https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/new', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        } 
      });

      data = await response.json();
      
    } catch (error) {

      console.error('Error:', error);
      throw error;
    }

    console.log(data)
    let key = data["ch-key"];
    let number = data["ch-num"];
    navigate(`/survey/${key}`, {state: {number: number}});  
  }

  return (
    <>
      <NavBar />
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="mb-12">
            <h1 className="text-4xl font-bold text-slate-900 mb-2">My Chapters</h1>
          </div>
          <div className="flex flex-col gap-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {!gettingChapters && (chapters.map((card) => (
                <Card key={card["ch-num"]} data-chapter={card["ch-key"]} data-number={card["ch-num"]} className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleCardClick}>
                  <CardHeader>
                    <CardTitle className="text-xl">Chapter {card["ch-num"]}</CardTitle>
                  </CardHeader>
                </Card>
              )))}
              {gettingChapters && (
                <div className="flex w-svw gap-6">
                  <p className="text-xl lg:text-2xl font-bold">Getting Chapters ...</p>
                  <Spinner className="h-12 w-12"/>
                </div>
              )}
            </div>
            <div className="flex gap-6">
              <Button className="text-white font-semibold py-2 px-6 rounded-lg
                                transform transition duration-300 ease-in-out
                                hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                                active:scale-95 active:bg-amber-700 cusror-pointer w-fit" 
                      disabled={creatingNewChapter}
                      onClick={createNewChapter}>
                        Start a New Chapter!
                </Button>
              {creatingNewChapter && (
                <div className="flex justify-center place-items-center">
                  <Spinner className="h-6 w-6"/>
                </div>
                )}
            </div>
          </div>
        </div>

        <ScrollToTopButton />
      </div>
    </>
  );
}