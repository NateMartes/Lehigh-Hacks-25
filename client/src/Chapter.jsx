import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import QuestionList from "./Questions"


function Chapter() {

  const [intro, setIntro] = useState("");
  const [chapterNum, setChapterNum] = useState(-1);
  const [options, setOptions] = useState([]);
  const [choice, setChoice] = useState(0);
  const [end, setEnd] = useState("");

  const params = useParams();

  useEffect(() => {

    let chKey = params.chKey
    // Get chapter intro
    let introData =  {
      "ch_key": chKey,
      "content": "I am the intro of chapter " + chKey + "\n Lore",
      "options": [
        "Do option A",
        "Do option B",
        "Do option C"
      ]
    }

    setIntro(introData.content);
    setOptions(introData.options);

  }, [])
  
  return (
    <div className="p-4">
        <h1 className="text-4xl font-bold text-slate-900 mb-2">Chapter {chapterNum}</h1>
        <div className="text-2xl text-slate-900">
          <p>{intro}</p>
        </div>
    </div>
  )
}

export default Chapter