### *Lehigh University Hackathon 2025 – Mental Health & Wellness Track*

<<<<<<< HEAD
## 💭 Overview
We believe that storytelling can heal. **Therapy through Create-Your-Own-Adventure Storytelling** transforms interactive fiction into a form of self-reflection and emotional care.
Instead of traditional journaling or static mindfulness apps, our platform engages users in a **personalized story world** that reflects their emotional state and gently encourages awareness, curiosity, and hope.
=======
Therapy through Create-Your-Own-Adventure Storytelling
>>>>>>> 5226923ed43de3775bfdb34d2b54ef8f1efa0d14

When users log in, they answer a short series of **yes/no screening questions**—simple, non-invasive prompts that help gauge their current mood. Based on their responses, the system dynamically generates a **narrative chapter** starring a character they can read, relate to, and emotionally project onto. The story entertains, but also resonates.

As the story unfolds, the user can **interact through pre-generated dialogue prompts**—selecting thoughts, emotions, or actions that gently guide both narrative direction and emotional insight.

Our goal: create a space that *feels like reading a story—but secretly feels like being heard.*

---

## 🧠 Key Features
- 🌈 **Adaptive Story Generation** – Each chapter tailors its theme and tone to user responses.
- 💬 **Interactive Prompts** – Users make decisions through emotional or narrative options, creating self-reflective micro-choices.
- 🪞 **Character Mirroring** – The main character reflects the user’s mood and growth, allowing for projection and empathy.
- 🔒 **Private and Safe** – All personal data is stored securely in DynamoDB with anonymous session identifiers—no personal identifiers required.
- ☁️ **Scalable Cloud Architecture** – Fully serverless design for accessibility, performance, and low cost.

---

## 🧰 Tech Stack

| Layer | Technologies Used | Purpose |
|-------|-------------------|----------|
| **Frontend** | React, Tailwind CSS, shadcn/ui | Smooth, modern UI for immersive storytelling |
| **Backend** | AWS Lambda, API Gateway | Serverless microservices for adaptive logic |
| **AI & Story Engine** | AWS Bedrock (Claude / Titan models) | Contextual narrative generation & emotional adaptation |
| **Database** | DynamoDB | Stores user session data and narrative progression |
| **Middleware / SDKs** | AWS Boto3 | Secure communication and orchestration between services |

🧩 **Architecture Summary**
1. User logs in → answers screening questions.
2. API Gateway triggers a **Lambda function** that interprets responses.
3. Lambda queries **Bedrock** for story content tailored to emotional patterns.
4. Responses and session data persist in **DynamoDB** for continuity.
5. React frontend renders the generated chapter with smooth UI transitions via **shadcn** and **Tailwind**, enabling branching prompts and real-time interaction.

---

## 💡 What Makes It Innovative
- **Emotion-Responsive Narrative Therapy:** Bridges the gap between entertainment and mental health reflection.
- **Serverless AI Design:** Built entirely on AWS Lambda and Bedrock for cost-effective scalability—no traditional backend servers.
- **Safe Self-Expression:** Encourages introspection *without diagnostics*, ensuring accessibility and privacy.
- **Hackathon-Friendly Implementation:** Modular architecture with fully deployable AWS stack and lightweight React frontend.

---

## 🧭 Challenges We Overcame
- Translating emotion data from simple yes/no responses into nuanced narrative tones.
- Balancing creativity with emotional sensitivity and avoiding prescriptive “therapy talk.”
- Integrating AWS Bedrock with Lambda via Boto3 under tight latency constraints.
- Designing an interface that *feels like a storybook, not a survey form.*

---

## 🌱 What’s Next
- Collaboration with therapists to add guided coping paths and emotional safety checks.
- Expansion into mobile (React Native) for accessibility and on-the-go reflection.
- Data visualization of mood progression through story arcs.
- Enhanced world-building with persistent characters that evolve with the user.

---

## 💖 Team
Created by a team of developers and storytellers from **Wilkes University** for **Lehigh University Hackathon 2025**.
We believe that healing doesn’t always come from advice—sometimes, it begins with a story that understands you.
