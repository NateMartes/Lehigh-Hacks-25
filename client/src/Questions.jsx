import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { fetchAuthSession } from 'aws-amplify/auth';
import NavBar from './NavBar';

async function makeQuestions(key) {
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      await fetch('https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          "ch-key": key
        })
      });
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
}

async function getQuestions(key) {
    console.log("getQuestions Called")
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      const response = await fetch(`https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/questions?ch-key=${key}`, {
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

async function createIntro(questions, key) {
    try {
      const token = (await fetchAuthSession()).tokens.idToken;
      await fetch(`https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/intro`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          "questions": questions,
          "ch-key": key
        })
      });
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
}

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
  const [creatingIntro, setCreatingIntro] = useState(false);

  const params = useParams();
  const key = params.chKey;
  const navigate = useNavigate();
  const { state } = useLocation();

  useEffect(() => {
    async function run() {
        await makeQuestions(key);
        let data = await getQuestions(key);
        console.log(data);
        setQuestions(data.questions);
    }
    run();
  }, [])

  async function handleAnswer(answer) {

    const updatedAnswers = {
      ...answers,
      [currentIndex]: answer,
    };

    setAnswers(updatedAnswers);

    if (currentIndex < questions.length - 1) {
      setTimeout(() => {
        setCurrentIndex(currentIndex + 1);
      });

    } else {
        let key = params.chKey;
        let answeredQuestions = questions.map((q, index) => {
          console.log(q)
          console.log(index)
          return {
            "question-id": q["question-id"],
            "answer": updatedAnswers[index]
          }
        })
        console.log(answeredQuestions)
        setCreatingIntro(true);
        await createIntro(answeredQuestions, key);
        navigate(`/chapter/${key}`, {state: {number: state.number}});
    }
  };

  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <>
      <NavBar/>
      {(questions.length > 0 && !creatingIntro)  && (<div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
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
                question={questions[currentIndex]["content"]}
                onAnswer={handleAnswer}
                answered={answers[currentIndex] !== undefined}
              />
          </div>
        </div>
      </div>)}

      {(questions.length == 0) && (
        <div className="flex flex-col justify-center place-items-center h-svh gap-6">
          <p className="text-xl lg:text-2xl font-bold">Getting Reflections ...</p>
          <Spinner className="h-12 w-12"/>
        </div>
        )}

      {creatingIntro && (
        <div className="flex flex-col justify-center place-items-center h-svh gap-6">
          <p className="text-xl lg:text-2xl font-bold">Creating a New Chapter For You ...</p>
          <Spinner className="h-12 w-12"/>
        </div>
        )}
    </>
  );
}