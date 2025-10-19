# Therapy through Create-Your-Own-Adventure Storytelling
### Lehigh University Hackathon 2025 – Mental Health & Wellness Track

## Overview
We believe storytelling can heal. **Therapy through Create-Your-Own-Adventure Storytelling** transforms interactive fiction into a form of self-reflection and emotional care.
Instead of static mindfulness apps, our platform engages users in a **personalized story world** that reflects their emotional state and encourages awareness and curiosity.

When users log in, they answer a short series of yes/no screening questions—simple, non-invasive prompts that help gauge their current mood. Based on their responses, the system dynamically generates a **narrative chapter** starring a character they can read, relate to, and emotionally project onto.

As the story unfolds, users interact through pre-generated dialogue prompts—selecting thoughts, emotions, or actions that gently guide both the narrative direction and emotional insight.

Our goal: create a space that feels like reading a story—but secretly feels like being heard.

---

## Key Features
- Adaptive Story Generation – Each chapter tailors its theme and tone to user responses.
- Interactive Prompts – Users make decisions through emotional or narrative options, creating self-reflective micro-choices.
- Character Mirroring – The main character reflects the user’s mood and growth, allowing for projection and empathy.
- Private and Safe – All personal data is stored securely in DynamoDB with anonymous session identifiers—no personal identifiers required.
- Scalable Cloud Architecture – Fully serverless design for accessibility, performance, and low cost.

---

## Tech Stack

| Layer | Technologies Used | Purpose |
|-------|-------------------|----------|
| **Frontend** | React, Tailwind CSS, shadcn/ui | Smooth, modern UI for immersive storytelling |
| **Backend** | Python (FastAPI), AWS Lambda, API Gateway | Serverless backend for adaptive logic and API orchestration |
| **AI & Story Engine** | Claude (Anthropic) via AWS Bedrock | Contextual narrative generation and emotional adaptation |
| **Database** | DynamoDB | Stores user session data and narrative progression |
| **Middleware / SDKs** | AWS Boto3 | Secure communication and orchestration between services |

### Architecture Summary
1. User logs in and answers screening questions.
2. API Gateway triggers a Python-based AWS Lambda function that processes responses.
3. The Lambda function calls Claude (via AWS Bedrock) to generate adaptive story content.
4. Responses and user data persist in DynamoDB for continuity.
5. The React frontend renders the generated chapter with smooth UI transitions via shadcn and Tailwind, enabling branching prompts and real-time interaction.

---

## What Makes It Innovative
- Emotion-Responsive Narrative Therapy: Bridges the gap between entertainment and mental health reflection.
- Serverless AI Design: Built entirely on AWS Lambda and Bedrock for cost-effective scalability—no traditional backend servers.
- Safe Self-Expression: Encourages introspection without diagnostics, ensuring accessibility and privacy.
- Hackathon-Optimized Implementation: Modular architecture with fully deployable AWS stack and lightweight React frontend.

---

## Challenges We Overcame
- Translating emotional data from simple yes/no responses into nuanced narrative tones.
- Balancing creativity with emotional sensitivity and avoiding prescriptive “therapy talk.”
- Integrating Claude (Anthropic) through AWS Bedrock and managing latency in real time.
- Designing an interface that feels like a storybook rather than a questionnaire.

---

## What’s Next
- Collaborate with therapists to add guided coping paths and emotional safety checks.
- Expand to mobile (React Native) for accessibility and on-the-go reflection.
- Introduce mood progression visualization through narrative arcs.
- Build persistent characters that evolve alongside the user’s choices and emotions.

---

## Team
Created by a team of developers and storytellers from **Wilkes University** for **Lehigh University Hackathon 2025**.
We believe that healing doesn’t always come from advice—sometimes, it begins with a story that understands you.
