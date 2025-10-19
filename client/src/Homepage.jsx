import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate } from "react-router-dom";
import NavBar from './NavBar';
import ScrollToTopButton from './ScrollToTopButton';

export default function ChapterList() {

  const navigate = useNavigate();

  function handleCardClick(event) {
    let key = event.currentTarget.dataset.chapter;
    let number = event.currentTarget.dataset.number;
    navigate(`/chapter/${key}`, {state: {number: number}});  
  }

  async function createNewChapter() {
    try {
      const response = await fetch('https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/new', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const chapterData = await response.json();
      
      const key = chapterData.ch_key;
      const number = chapterData.number;
      
      navigate(`/survey/${key}`, { state: { number: number } });
    } catch (error) {
      console.error('Error creating new chapter:', error);
      // Handle error appropriately (show toast, alert, etc.)
    }
  }

  const cards = [
    {
      number: 1,
      ch_key: 'abc',
    },
    {
      number: 2,
      ch_key: 'abcd',
    },
    {
      number: 3,
      ch_key: 'abcde',
    },
  ];

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
              {cards.map((card) => (
                <Card key={card.number} data-chapter={card.ch_key} data-number={card.number} className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleCardClick}>
                  <CardHeader>
                    <CardTitle className="text-xl">Chapter {card.number}</CardTitle>
                  </CardHeader>
                </Card>
              ))}
            </div>
            <Button className="text-white font-semibold py-2 px-6 rounded-lg
                              transform transition duration-300 ease-in-out
                              hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                              active:scale-95 active:bg-amber-700 cusror-pointer w-fit" 
                    onClick={createNewChapter}>
                      Start a New Chapter!
              </Button>
          </div>
        </div>

        <ScrollToTopButton />
      </div>
    </>
  );
}