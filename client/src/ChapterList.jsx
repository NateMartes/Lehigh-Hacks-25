import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate } from "react-router-dom";

export default function ChapterList() {

  const navigate = useNavigate();

  function handleCardClick(event) {
    let key = event.currentTarget.dataset.chapter;
    let number = event.currentTarget.dataset.number;
    navigate(`/survey/${key}`, {state: {number: number}});  
  }

  function createNewChapter() {
    
    // Create new chapter and get back a key
    let chpaterData = {
      "ch_key": "a-brand-new-key",
      "number": 12345
    }

    let key = chpaterData.ch_key
    let number = chpaterData.number 
    navigate(`/survey/${key}`, {state: {number: number}});
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">Lehigh Hacks</h1>
          <p className="text-lg text-slate-600">Therapy through Create-Your-Own-Adventure Storytelling</p>
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
          <Button className="bg-gray-400 hover:bg-gray-600 w-fit" onClick={createNewChapter}>Create a New Chapter</Button>
        </div>
      </div>
    </div>
  );
}