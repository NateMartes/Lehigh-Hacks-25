import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import NavBar from './NavBar';

function Question({ question, onAnswer, answered }) {
  return (
    <Card className="bg-white">
      <CardContent className="pt-6">
        <p className="text-lg font-medium text-slate-900">{question}</p>

        {!answered && (
          <div className="flex gap-3 mt-6">
            <Button
              onClick={() => onAnswer(false)}
              className="flex-1 text-white font-semibold py-2 px-6 rounded-lg
                              transform transition duration-300 ease-in-out
                              hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                              active:scale-95 active:bg-amber-700 cusror-pointer"
            >
              No
            </Button>
            <Button
              onClick={() => onAnswer(true)}
              className="flex-1 text-white font-semibold py-2 px-6 rounded-lg
                              transform transition duration-300 ease-in-out
                              hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                              active:scale-95 active:bg-amber-700 cusror-pointer"
            >
              Yes
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function QuestionList() {
  const [answers, setAnswers] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [questions, setQuestions] = useState([]);

  const params = useParams();
  const navigate = useNavigate();
  const { state } = useLocation();

  useEffect(() => {

    // Get questions for new chapter

    setQuestions([
        'Do you enjoy coding?',
        'Is JavaScript your favorite language?',
        'Do you like working in teams?',
        'Have you used React before?',
        'Do you prefer frontend development?',
    ])

  }, [])

  function handleAnswer(answer) {

    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: answer,
    }));

    if (currentIndex < questions.length - 1) {
      setTimeout(() => {
        setCurrentIndex(currentIndex + 1);
      });

    } else {
        let key = params.chKey;
        navigate(`/chapter/${key}`, {state: {number: state.number}});
    }
  };

  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <>
      <NavBar/>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-900 mb-2">Reflection</h1>
            
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div
                className="bg-amber-500 h-2 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-sm text-slate-600 mt-2">
              Question {currentIndex + 1} of {questions.length}
            </p>
          </div>

          <div className="mb-8">
              <Question
                question={questions[currentIndex]}
                onAnswer={handleAnswer}
                answered={answers[currentIndex] !== undefined}
              />
          </div>
        </div>
      </div>
    </>
  );
}